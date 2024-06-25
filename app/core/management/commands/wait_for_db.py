"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
# Error django throws when the database is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """Entry point for command."""
        # writes message to the screen
        self.stdout.write("Waiting for database...")
        db_up = False  # assume db is not up
        while db_up is False:
            try:
                # if database isn't ready, we will throw an exception
                self.check(databases=['default'])
                db_up = True  # Once db is ready, we stop the database
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)  # stop for 1 second before we try again

        self.stdout.write(self.style.SUCCESS('Database available!'))
