import logging
import os

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from utils.case import CaseObj, DocketEntryObj, DocumentObj
from bankruptcy.cases.models import Case, DocketEntry, Document


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='../logs/total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='../logs/errors.log', mode='a')
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
                    raise CaseParseError

                # check if case exists
                try:
                    caseModelObject = get_obj_if_exists(case, Case)
                except MultipleObjectsReturned:
                    raise GetCaseError("Multiple objects returned.")
                except:
                    stats.case.failed_unknown += 1
                    raise GetCaseError("Failed for unknown reason.")

                # Build case fields for django model interaction
                try:
                    case_args = {
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
                if caseModelObject:
                    try:
                        caseModelObject.update(**case_args)
                    except:
                        stats.case.failed_unknown += 1
                        raise CaseModelActionFailure("Case model update failed.")
                else:
                    try:
                        caseModelObject = Case.objects.create(**case_args)
                    except:
                        stats.case.failed_unknown += 1
                        raise CaseModelActionFailure("Case model create failed.")
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
                            'recap_id': entry.get_id(),
                            'date_filed': entry.get_date_filed(),
                            'date_created': entry.get_date_created(),
                            'description': entry.get_description(),
                            'case': caseModelObject,
                        }
                    except:
                        raise CaseAPIError("Creating entry argument object failed.")

                    try:
                        entryModelObject = get_obj_if_exists(entry, DocketEntry)
                    except MultipleObjectsReturned:
                        raise GetEntryError("Multiple objects returned.")
                    except:
                        stats.entry.failed_unknown += 1
                        raise GetEntryError("Failed for unknown reason.")

                    # update or create docket entry
                    if entryModelObject:
                        try:
                            entryModelObject.update(**entry_args)
                        except:
                            stats.entry.failed_unknown += 1
                            raise DocketEntryModelActionFailure("DocketEntry model update failed.")
                    else:
                        try:
                            entryModelObject = DocketEntry.objects.create(**entry_args)
                        except:
                            stats.entry.failed_unknown += 1
                            raise DocketEntryModelActionFailure("DocketEntry model create failed.")

                    stats.doc.count += len(entry.documents)
                    for doc in entry.documents:
                        try:
                            try:
                                doc_args = {
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

                            try:
                                docModelObject = get_obj_if_exists(doc, Document)
                            except MultipleObjectsReturned:
                                raise GetDocError("Multiple objects returned.")
                            except:
                                stats.doc.failed_unknown += 1
                                raise GetDocError("Failed for unknown reason.")

                            # update or create document
                            if docModelObject:
                                try:
                                    docModelObject.update(**doc_args)
                                except:
                                    stats.doc.failed_unknown += 1
                                    raise DocModelActionFailure("Document model update failed.")
                            else:
                                try:
                                    docModelObject = Document.objects.create(**doc_args)
                                except:
                                    stats.entry.failed_unknown += 1
                                    raise DocModelActionFailure("Document model create failed.")

                            # extract entities from doc

                            # extract creditors from doc (if in provided JSON)

                            # consolidate creditors and entities, and add them as tags to doc

                        except Exception as err:
                            stats.doc.failed += 1
                            logger.warning(
                                f'(Case {case_num} / {num_cases}) Processing doc {doc.get_id()} failed.'
                            )
                            continue

                        stats.doc.loaded += 1

                except Exception as err:
                    stats.entry.failed += 1
                    logger.warning(
                        f'(Case {case_num} / {num_cases}) Processing entry {entry.get_id()} failed.'
                    )
                    continue

                stats.entry.loaded += 1

            stats.case.loaded += 1
            logging.info('Case {0} / {1} Reviewed. (id: {2})'.format(case_num, num_cases, case.get_id()))

        final_msg = f'Cases Loaded: {stats.case.loaded} / {num_cases}  |  Cases Failed: {stats.case.failed}  |  Number of Failures with Unknown Explanations: {stats.case.failed_unknown}'

        self.stdout.write(self.style.SUCCESS(final_msg))
