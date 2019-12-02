from io import BytesIO
import logging
import os

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from utils.case import Case as CaseObj, DocketEntry as DocketEntryObj, Document as DocumentObj
from bankruptcy.cases.models import Case, DocketEntry, Document
from django.core.files import File

if not os.path.exists('./logs'):
    os.makedirs('./logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='./logs/total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='./logs/errors.log', mode='a')
errorsLog.setLevel(logging.WARNING)
errorsLog.setFormatter(total_formatter)

logger = logging.getLogger('load_case_data')
logger.addHandler(console)
logger.addHandler(errorsLog)


def get_obj_if_exists(obj, model):
    """
    Return object of given model in database if it exists. Otherwise, return False.
    """
    try:
        existing_obj = model.objects.get(recap_id=obj.get_id())
        return existing_obj
    except ObjectDoesNotExist:
        return False
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned
    except:
        raise UnknownError


class UnknownError(Exception):
    pass


class CaseParseError(Exception):
    pass


class GetCaseError(Exception):
    pass


class CaseAPIError(Exception):
    pass


class CaseModelActionFailure(Exception):
    pass


class DocketEntryModelActionFailure(Exception):
    pass


class DocModelActionFailure(Exception):
    pass


class DocDownloadFailed(Exception):
    pass


class GetEntryError(Exception):
    pass


class GetDocError(Exception):
    pass


class Count:
    def __init__(self, count=0, loaded=0, failed=0, failed_unknown=0):
        self.count = count
        self.loaded = loaded
        self.failed = failed
        self.failed_unknown = failed_unknown


class Stats:
    def __init__(self, num_cases):
        self.case = Count(count=num_cases)
        self.entry = Count()
        self.doc = Count()


class Command(BaseCommand):
    help = 'Loads case data from JSON files into database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Use all data instead of just the sample.',
        )

    def handle(self, *args, **options):
        DATA_LOCATION = 'data/samples'
        if options['all']:
            DATA_LOCATION = 'data/total'

        logger.info('Loading case data into the database...')
        case_files = []
        for file in os.listdir(DATA_LOCATION):
            if file.endswith('.json'):
                case_files.append(os.path.join(DATA_LOCATION, file))

        # Load case -> creditor JSON.

        num_cases = len(case_files)
        stats = Stats(num_cases)
        for case_num, fn in enumerate(case_files):
            # Creating/updating case object with fields that
            # are not docket entry dependent
            try:
                try:
                    case = CaseObj(fn)
                except:
                    raise CaseParseError("Parsing case failed.")

                # Build case fields for django model interaction
                try:
                    case_args = {
                        'id': case.get_id(),
                        'name': case.get_case_name(),
                        'recap_id': case.get_id(),
                        'pacer_id': case.get_pacer_id(),
                        'date_filed': case.get_date_filed(),
                        'date_created': case.get_date_created(),
                        'date_terminated': case.get_date_terminated(),
                        'date_blocked': case.get_date_blocked(),
                        'jurisdiction': case.get_jurisdiction(),
                        'chapter': case.get_chapter(),
                        'data': case.get_raw_data(),
                    }
                except:
                    stats.case.failed_unknown += 1
                    raise CaseAPIError("Creating case argument object failed.")

                # update or create case
                try:
                    caseModelObject, created = Case.objects.update_or_create(**case_args)
                except Exception as err:
                    raise CaseModelActionFailure(f"Case model update/create failed. Explanation: {err}")

            except Exception as err:
                logger.error(f'Case {case_num} / {num_cases} Failed.\n Explanation: "{err}"')
                stats.case.failed += 1
                continue  # this is mission critical stuff, so ignore case if there is failure

            # add case docket entries
            stats.entry.count += len(case.get_entries())
            for entry in case.get_entries():
                try:
                    try:
                        entry_args = {
                            'id': entry.get_id(),
                            'recap_id': entry.get_id(),
                            'date_filed': entry.get_date_filed(),
                            'date_created': entry.get_date_created(),
                            'description': entry.get_description(),
                            'case': caseModelObject,
                        }
                    except:
                        raise CaseAPIError("Creating entry argument object failed.")

                    # update or create docket entry
                    try:
                        entryModelObject, created = DocketEntry.objects.update_or_create(**entry_args)
                    except Exception as err:
                        raise DocketEntryModelActionFailure(f"DocketEntry model update/create failed. Explanation: {err}")

                    stats.doc.count += len(entry.documents)
                    for doc in entry.documents:
                        try:
                            try:
                                doc_args = {
                                    'id': doc.get_id(),
                                    'recap_id': doc.get_id(),
                                    'pacer_id': doc.get_pacer_id(),
                                    'doc_type': doc.get_type(),
                                    'is_sealed': doc.is_sealed(),
                                    'is_available': doc.is_available(),
                                    'file_url': doc.get_file_url(),
                                    'description': doc.get_description(),
                                    'text': doc.text,
                                    'docket_entry': entryModelObject,
                                }
                            except:
                                raise CaseAPIError("Creating doc argument object failed.")

                            # update or create document
                            try:
                                docModelObject, created = Document.objects.update_or_create(**doc_args)
                            except Exception as err:
                                raise DocModelActionFailure(f"Document model update/create failed. Explanation: {err}")

                            # add thumbnail
                            try:
                                thumbnail = doc.get_thumbnail()
                                if thumbnail is not None:
                                    blob = BytesIO()
                                    thumbnail.save(blob, 'JPEG')
                                    docModelObject.preview.save(f'{doc.get_id()}.jpg', File(blob), save=False)
                                    docModelObject.save()
                            except Exception as err:
                                logger.warning(
                                    f'(Case {case_num} / {num_cases}) Getting thumbnail for doc {doc.get_id()} failed.\n Explanation: {err}'
                                )

                        except Exception as err:
                            stats.doc.failed += 1
                            logger.warning(
                                f'(Case {case_num} / {num_cases}) Processing doc {doc.get_id()} failed.\n Explanation: {err}'
                            )
                            continue

                        stats.doc.loaded += 1

                except Exception as err:
                    stats.entry.failed += 1
                    logger.warning(
                        f'(Case {case_num} / {num_cases}) Processing entry {entry.get_id()} failed.\n Explanation: {err}'
                    )
                    continue
                
                stats.entry.loaded += 1

            stats.case.loaded += 1
            logging.info('Case {0} / {1} Reviewed. (id: {2})'.format(case_num, num_cases, case.get_id()))

        final_case_msg = f'Cases Loaded: {stats.case.loaded} / {num_cases}  |  Cases Failed: {stats.case.failed}  |  Number of Failures with Unknown Explanations: {stats.case.failed_unknown}'
        final_entries_msg = f'Entries Loaded: {stats.entry.loaded} / {stats.entry.count}  |  Entries Failed: {stats.entry.failed}  |  Number of Failures with Unknown Explanations: {stats.entry.failed_unknown}'
        final_docs_msg = f'Docs Loaded: {stats.doc.loaded} / {stats.doc.count}  |  Docs Failed: {stats.doc.failed}  |  Number of Failures with Unknown Explanations: {stats.doc.failed_unknown}'

        self.stdout.write(self.style.SUCCESS(final_case_msg))
        self.stdout.write(self.style.SUCCESS(final_entries_msg))
        self.stdout.write(self.style.SUCCESS(final_docs_msg))
