# coding: utf-8
from __future__ import unicode_literals, absolute_import

import sys

from fias.compat import BaseCommandCompatible
from .utils import trunc_index_table, fill_index_table, create_gin_index


class Command(BaseCommandCompatible):
    help = 'Configure Sphinx engine'
    usage_str = 'Usage: ./manage.py fias_suggest'

    arguments_dictionary = {
        "--rebuild-index": {
            "action": "store_true",
            "default": False,
            "dest": "rebuild",
            "help": "Rebuild GIN index for Full-Text search"
        },
    }

    def handle(self, *args, **options):
        rebuild = options.pop('rebuild')
        if rebuild:
            self.stdout.write('Truncate a table')
            trunc_index_table()
            self.stdout.write('Fill the table')
            fill_index_table()
            self.stdout.write('Create gin index')
            create_gin_index()
            self.stdout.write('Finish')

    def error(self, message, code=1):
        self.stderr.write(message)
        sys.exit(code)
