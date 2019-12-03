import csv
import json
import logging
import os
import math

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError

from bankruptcy.cases.models import Case, DocketEntry, Document
from utils.case import Case as CaseObj, DocketEntry as DocketEntryObj, Document as DocumentObj

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


def get_top_percentile(ls, percentile, minimum):
    """
    Assumes descending order.
    """
    if len(ls) < minimum:
        return ls

    return ls[:max(math.floor(percentile / 100 * len(ls)), minimum)]

class Command(BaseCommand):
    help = 'Loads and processes case content from text and JSON files into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Use all data instead of just the sample.',
        )

    def handle(self, *args, **options):
        OCR_OUTPUT_DIR = './data/ocr_nysb'
        FORM_DATA_FILENAME = './data/form_data_nysb.json'
        ENTITY_DATA_FILENAME = './data/doc_to_entities.csv'
        MIN_ENTITY_THRESHOLD = 10


        # Add entities to documents
        num_entities_failed = 0
        num_entities_not_found = 0
        with open(ENTITY_DATA_FILENAME, 'r', newline='') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            i = 0
            for i, row in enumerate(reader):
                try:
                    # skip header
                    if i == 0:
                        continue

                    doc_id = row[0]
                    people = row[1]
                    organizations = row[2]

                    try:
                        doc = Document.objects.get(id=doc_id)
                    except Exception as err:
                        logger.error(f'Document {doc_id} not found. Reason: {err}')
                        num_entities_not_found += 1
                        continue

                    # Filter out top 10%
                    people = get_top_percentile(people, 20, MIN_ENTITY_THRESHOLD)
                    organizations = get_top_percentile(organizations, 20, MIN_ENTITY_THRESHOLD)

                    print(people)

                    doc.people.set(*people)
                    doc.organizations.set(*organizations)
                    total = people + organizations
                    doc.entities.set(*total)
                    doc.save()
                except Exception as err:
                    logger.error(f'(doc: {doc_id}) Can\'t load entities for doc. Reason: {err}')
                    num_entities_failed += 1
            
            print(f'Number of rows: {i}')

        logger.info(f'Num entities not found: {num_entities_not_found}, num entities failed: {num_entities_failed}')

        num_cases = Case.objects.all().count()
        highest_case_id = Case.objects.last()
        num_cases_failed = 0
        for case_idx in range(highest_case_id):
            try:
                case = Case.objects.get(id=case_idx)
            except ObjectDoesNotExist:
                continue

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

                    try:
                        # consolidate case document entities and add
                        case.people.add(*(doc.people))
                        case.organizations.add(*(doc.organizations))
                        case.entities.add(*(doc.entities))

                    except Exception as err:
                        logger.error(
                            f'(Case {case_idx} / {num_cases}) Entity agg failed (doc={doc.id}). Reason: {err}'
                        )
                case.save()

            except Exception as err:
                num_cases_failed += 1
                logger.error(f'(Case {case_idx} / {num_cases}) Loading case content failed. Explanation: {err}')

        logger.info(
            f'Finished loading content. Loaded {num_cases - num_cases_failed} / {num_cases} cases successfully.')
