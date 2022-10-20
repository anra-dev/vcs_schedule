from django.core.management.commands.migrate import Command

from utils import db


class Command(Command):
    def handle(self, *args, **options):
        db.database_ready("default", maximum_wait=15)
        super().handle(*args, **options)