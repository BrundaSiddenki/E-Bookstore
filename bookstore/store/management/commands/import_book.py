import csv
from django.core.management.base import BaseCommand
from store.models import Book

class Command(BaseCommand):
    help = 'Import books from sample_books.csv'

    def handle(self, *args, **kwargs):
        with open('sample_books.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                Book.objects.create(
                    title=row['title'],
                    author=row['author'],
                    description=row['description'],
                    price=row['price']
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully imported {count} books.'))
