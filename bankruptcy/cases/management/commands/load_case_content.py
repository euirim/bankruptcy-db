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
    filename='../logs/case_content_total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='../logs/case_content_errors.log', mode='a')
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
        OCR_OUTPUT_DIR = 'data/ocr_results'

        # Store doc text and extract entities
        docs = Document.objects.all() 

        num_docs = len(docs)
        for i, doc in enumerate(docs):
            # try to get doc text from file
            try:
                ocr_fn = f'{doc.docket_entry.case.recap_id}_{doc.docket_entry.recap_id}_{doc.recap_id}'
                ocr_path = os.path.join(OCR_OUTPUT_DIR, ocr_fn)

            except Exception as err:
                logger.error(f'(Doc {i} / {num_docs}) Failed to get doc text. Explanation: {err}')

        cases = Case.objects.all()

        num_cases = len(cases)
        for i, case in enumerate(cases):
            try:
                # add case creditor entities
                pass
            except Exception as err:
                logger.error(f'(Case {i} / {num_cases}) Failed to add content to case. Explanation: {err}')


            # consolidate case document entities and add
