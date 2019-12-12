import csv

from django.core.management.base import BaseCommand, CommandError

from bankruptcy.cases.models import Case

class Command(BaseCommand):
    help = 'Records durations of all cases in database to CSV file.'
    def handle(self, *args, **options):
        # get durations in list of lists (with start date)
        cases = Case.objects.all()

        with open('./data/case_durations.csv', mode='w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['date_filed', 'duration'])

            print('Writing durations.')
            for case in cases:
                duration = case.get_duration()

                if case.date_filed is None:
                    continue

                writer.writerow([case.date_filed, duration])
            