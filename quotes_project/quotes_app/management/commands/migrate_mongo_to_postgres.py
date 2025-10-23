import configparser
from pathlib import Path
from django.core.management.base import BaseCommand
from mongoengine import connect

try:
    from quotes_app.models import Author as PgAuthor, Quote as PgQuote, Tag as PgTag
except ModuleNotFoundError:
    import sys
    from pathlib import Path as _Path
    _PROJECT_DIR = _Path(__file__).resolve().parent.parent.parent.parent  # quotes_project directory (contains quotes_app)
    sys.path.insert(0, str(_PROJECT_DIR))
    from quotes_app.models import Author as PgAuthor, Quote as PgQuote, Tag as PgTag


try:
    from mongo_models import Author as MongoAuthor, Quote as MongoQuote
except ImportError:
    raise ImportError(
        "Не найден файл 'mongo_models.py'. "
        "Пожалуйста, скопируйте ваш 'models.py' из ДЗ-8 в корень Django-проекта "
        "и переименуйте его в 'mongo_models.py'."
    )


class Command(BaseCommand):
    help = 'Migrates data from MongoDB to PostgreSQL'

    def handle(self, *args, **options):


        # Ищем config.ini рядом с manage.py (в папке quotes_project)
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        config_path = BASE_DIR / 'config.ini'

        if not config_path.exists():
            self.stdout.write(self.style.ERROR(
                f"Файл 'config.ini' не найден по пути: {config_path}. "
                "Скопируйте его из ДЗ-8 в корень проекта (рядом с manage.py)."
            ))
            return

        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            mongo_uri = config.get('DB', 'URI')
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.stdout.write(self.style.ERROR(
                "В файле 'config.ini' не найдена секция [DB] или опция 'URI'."
            ))
            return


        connect(host=mongo_uri, ssl=True)

        self.stdout.write(self.style.SUCCESS('Успешно подключились к MongoDB Atlas.'))

        self.stdout.write('Начинаем миграцию авторов...')
        mongo_authors = MongoAuthor.objects()
        for author in mongo_authors:
            # get_or_create предотвращает создание дубликатов
            PgAuthor.objects.get_or_create(
                fullname=author.fullname,
                born_date=author.born_date,
                born_location=author.born_location,
                description=author.description
            )
        self.stdout.write(self.style.SUCCESS(f'Миграция авторов ({mongo_authors.count()}) завершена.'))

        self.stdout.write('Начинаем миграцию цитат и тегов...')
        mongo_quotes = MongoQuote.objects()
        for quote in mongo_quotes:
            tags = []
            if quote.tags:
                for tag_name in quote.tags:
                    t, created = PgTag.objects.get_or_create(name=tag_name)
                    tags.append(t)

            try:
                author_obj = PgAuthor.objects.get(fullname=quote.author.fullname)
            except PgAuthor.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"Автор {quote.author.fullname} не найден в PostgreSQL. Пропуск цитаты."
                ))
                continue

            pg_quote, created = PgQuote.objects.get_or_create(
                quote=quote.quote,
                author=author_obj
            )
            if created:
                pg_quote.tags.set(tags)

        self.stdout.write(self.style.SUCCESS(f'Миграция цитат ({mongo_quotes.count()}) завершена.'))