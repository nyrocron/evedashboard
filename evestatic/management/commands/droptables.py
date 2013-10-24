from django.core.management import call_command
from django.core.management.base import NoArgsCommand
from django.db import connection
from django.db.models import get_app, get_models

class Command(NoArgsCommand):
    args = ''
    help = 'Drops all tables of the evestatic app'

    def handle_noargs(self, **options):
        self._drop_app_tables('evestatic')

    def _drop_app_tables(self, app_name):
        app = get_app(app_name)
        cursor = connection.cursor()
        for model in get_models(app):
            table_name = model._meta.db_table
            self.stdout.write("Dropping table %s..." % table_name)
            cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        self.stdout.write("Done dropping tables of app %s." % app_name)
