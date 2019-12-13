from django.core.management.base import BaseCommand, CommandError

from bankruptcy.cases.models import Case, DocketEntry, Document

class Command(BaseCommand):
    help = 'Consolidate entities'

    def handle (sself, *args, **options):
        cases = Case.objects.all()
        case_count = cases.count()
        for i, case in enumerate(cases.iterator(chunksize=10)):
            print(f'Consolidating case {i} / {case_count}.') 
            for de in case.docket_entries.all():
                for doc in de.documents.all():
                    case.entities.add(*(doc.entities.names()))
