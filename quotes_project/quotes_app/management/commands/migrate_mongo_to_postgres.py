from django.core.management.base import BaseCommand
from quotes_app.models import Author as PgAuthor, Quote as PgQuote, Tag as PgTag
from mongo_models import Author as MongoAuthor, Quote as MongoQuote  # (модели из ДЗ-8)
from mongoengine import connect
import configparser


class Command(BaseCommand):
    help = 'Migrates data from MongoDB to PostgreSQL'

    def handle(self, *args, **options):
        config = configparser.ConfigParser()
        config.read('config.ini')

        authors = MongoAuthor.objects()
        for author in authors:
            PgAuthor.objects.get_or_create(
                fullname=author.fullname,
                born_date=author.born_date,
                born_location=author.born_location,
                description=author.description
            )
        self.stdout.write(self.style.SUCCESS('Authors migrated successfully.'))

        quotes = MongoQuote.objects()
        for quote in quotes:
            tags = []
            for tag_name in quote.tags:
                t, created = PgTag.objects.get_or_create(name=tag_name)
                tags.append(t)

            author = PgAuthor.objects.get(fullname=quote.author.fullname)

            PgQuote.objects.create(
                quote=quote.quote,
                author=author
            ).tags.set(tags)
        self.stdout.write(self.style.SUCCESS('Quotes and tags migrated successfully.'))
