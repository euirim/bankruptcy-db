import csv

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from bankruptcy.cases.models import Case

class Command(BaseCommand):
    help = 'Records durations of all cases in database to CSV file.'
    def handle(self, *args, **options):
        # get durations in list of lists (with start date)
        highest_case_id = Case.objects.last().id
        print(highest_case_id)

        with open('./data/case_durations.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['date_filed', 'duration'])

            print('Writing durations.')
            for case_idx in range(highest_case_id):
                print(case_idx)
                try:
                    case = Case.objects.get(id=case_idx)
                except ObjectDoesNotExist:
                    continue

                duration = case.get_duration()

                if case.date_filed is None:
                    continue

                writer.writerow([case.date_filed, duration])
            