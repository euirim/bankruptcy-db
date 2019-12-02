import json
import logging
import os
import csv
import sys
import glob
import multiprocessing as mp

from django.core.management.base import BaseCommand, CommandError

from utils.coherence import CoherenceDetector
from utils.entities import get_ppl_and_orgs, agg_across_entities

if not os.path.exists('./logs'):
    os.makedirs('./logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='./logs/gen_doc_entities_total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='./logs/gen_doc_entities_errors.log', mode='a')
errorsLog.setLevel(logging.WARNING)
errorsLog.setFormatter(total_formatter)

logger = logging.getLogger('gen_doc_entities')
logger.addHandler(console)
logger.addHandler(errorsLog)


def get_doc_id_from_fn(doc_fn):
    return int(doc_fn.split('_')[-1])


def worker(doc):
    doc_fn = doc
    # initialize coherence detector
    cd = CoherenceDetector()
    doc_id = get_doc_id_from_fn(doc_fn)
    logger.info(f'Reading doc {doc_id}.')
    text = None
    try:
        with open(doc_fn, 'r') as f:
            text = f.read()
        if not text or not cd.check_coherence(text):
            return 0
    except Exception as err:
        logger.error(f'Reading doc {doc_id} failed. Reason: {err}')
        return 1

    # extract entities
    try:
        # get entities from text
        ppl, orgs = get_ppl_and_orgs(text)

        people = [a[0] for a in sorted(ppl.items(), key=lambda x: x[1], reverse=True)]
        organizations = [a[0] for a in sorted(orgs.items(), key=lambda x: x[1], reverse=True)]
    except Exception as err:
        logger.error(
            f'Entity extraction failed (doc={doc_id}). Reason: {err}'
        )
        return 1

    return doc_id, people, organizations


class Command(BaseCommand):
    help = 'Maps doc IDs to entities in the documents.'
    def handle(self, *args, **options):
        OCR_OUTPUT_DIR = './data/ocr_nysb'
        
        docs = [fn for fn in glob.glob(f'{OCR_OUTPUT_DIR}/*')]

        num_failed = 0
        num_processed = 0
        num_incoherent = 0
        p = mp.Pool(max(mp.cpu_count() // 2, 1))  # divide by 2 to save memory
        with open('./data/doc_to_entities.csv', 'w', newline='') as f: 
            # tab separated with minimal quotes
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            writer.writerow(['doc_id', 'people', 'organizations'])
            for result in p.imap_unordered(worker, docs):
                num_processed += 1
                if result == 1:
                    num_failed += 1
                    continue
                elif result == 0:
                    num_incoherent += 1
                    continue
                
                writer.writerow([result[0], result[1], result[2]])

                logger.info(f'Processed {num_processed} / {len(docs)}, with {num_failed} failed and {num_incoherent} incoherent so far.')

        logger.info(f'Finished generating entities. {num_failed} / {len(docs)} failed.')
        logger.info('All done!')
