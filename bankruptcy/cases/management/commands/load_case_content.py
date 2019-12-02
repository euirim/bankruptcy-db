import json
import logging
import os

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError

from bankruptcy.cases.models import Case, DocketEntry, Document
from utils.case import Case as CaseObj, DocketEntry as DocketEntryObj, Document as DocumentObj
from utils.coherence import CoherenceDetector
from utils.entities import get_ppl_and_orgs, agg_across_entities

if not os.path.exists('./logs'):
    os.makedirs('./logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='./logs/case_content_total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='./logs/case_content_errors.log', mode='a')
errorsLog.setLevel(logging.WARNING)
errorsLog.setFormatter(total_formatter)

logger = logging.getLogger('load_case_content')
logger.addHandler(console)
logger.addHandler(errorsLog)


class Command(BaseCommand):
    help = 'Loads and processes case content from text and JSON files into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Use all data instead of just the sample.',
        )

    def handle(self, *args, **options):
        OCR_OUTPUT_DIR = 'data/ocr_nysb'
        FORM_DATA_FILENAME = 'data/form_data_nysb.json'

        cases = Case.objects.all()

        # initialize coherence detector
        cd = CoherenceDetector()

        num_cases = len(cases)
        num_cases_failed = 0
        for case_idx, case in enumerate(cases):
            logger.info(f'(Case {case_idx} / {num_cases}) Loading content.')
            try:
                # add case creditor entities
                try:
                    form_data = None
                    with open(FORM_DATA_FILENAME, 'r') as f:
                        form_data = json.load(f)

                    case.creditors.set(*(form_data.get(str(case.id), [[]])[0]))
                except Exception as err:
                    logger.error(
                        f'(Case {case_idx} / {num_cases}) Failed to add creditor info to case. Explanation: {err}'
                    )

                docs = []
                for de in case.docket_entries.all():
                    docs += de.documents.all()

                ppl_set = {}
                org_set = {}
                for doc in docs:
                    # try to get doc text from file
                    try:
                        ocr_fn = f'{doc.docket_entry.case.recap_id}_{doc.docket_entry.recap_id}_{doc.recap_id}'
                        ocr_path = os.path.join(OCR_OUTPUT_DIR, ocr_fn)
                        if not os.path.exists(ocr_path):
                            logger.debug(
                                f'(Case {case_idx} / {num_cases}) File corresponding to doc {doc.id} does not exist.'
                            )
                            continue

                        with open(ocr_path, 'r') as f:
                            text = f.read()
                    except Exception as err:
                        logger.error(
                            f'(Case {case_idx} / {num_cases}) Failed to get doc {doc.id}\'s text. Explanation: {err}'
                        )
                        continue

                    # check if text is coherent. if not, continue loop
                    try:
                        if not cd.check_coherence(text):
                            logger.debug(f'(Case {case_idx} / {num_cases}) Text not coherent (doc={doc.id}). Skipping.')
                            continue
                    except Exception as err:
                        logger.error(
                            f'(Case {case_idx} / {num_cases}) Coherence detection failed (doc={doc.id}). Reason: {err}'
                        )
                        continue

                    try:
                        # get entities from text
                        ppl, orgs = get_ppl_and_orgs(text)
                        ppl_set[doc.id] = ppl
                        org_set[doc.id] = orgs

                        # save entities in doc model
                        people = [a[0] for a in sorted(ppl.items(), key=lambda x: x[1], reverse=True)]
                        organizations = [a[0] for a in sorted(orgs.items(), key=lambda x: x[1], reverse=True)]
                        doc.people.set(*people)
                        doc.organizations.set(*organizations)
                        total = people + organizations
                        doc.entities.set(*total)
                        doc.save()
                    except Exception as err:
                        logger.error(
                            f'(Case {case_idx} / {num_cases}) Entity extraction failed (doc={doc.id}). Reason: {err}'
                        )
                # consolidate case document entities and add
                people = agg_across_entities(ppl_set)
                organizations = agg_across_entities(org_set)
                case.people.set(*people)
                case.organizations.set(*organizations)
                case.entities.set(*(people + organizations))
                case.save()

            except Exception as err:
                num_cases_failed += 1
                logger.error(f'(Case {case_idx} / {num_cases}) Loading case content failed. Explanation: {err}')

        logger.info(
            f'Finished loading content. Loaded {num_cases - num_cases_failed} / {num_cases} cases successfully.')
