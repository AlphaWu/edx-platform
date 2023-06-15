"""
Management Command to delete a v1 library.
"""
import json

from cms.djangoapps.contentstore.views.library import library_blocks_view
from django.core.management.base import BaseCommand
from opaque_keys.edx.keys import CourseKey
from opaque_keys.edx.locator import LibraryLocator
from xmodule.modulestore.django import modulestore

class Command(BaseCommand):
    """
    Delete a MongoDB backed v1 library

    Example usage:
        $ ./manage.py cms delete_library '<library ID>'
    """

    help = 'Delete a MongoDB backed course'

    def add_arguments(self, parser):
        parser.add_argument(
            'library_key',
            help='ID of the library to delete.',
        )

    def handle(self, *args, **options):
        try:
            library_key = str(options['library_key'], 'utf8')
        # May already be decoded to unicode if coming in through tests, this is ok.
        except TypeError:
            library_key = str(options['library_key'])

        print(f'"****** In management command to delete library {library_key}. Looking for libraries ...')
        store = modulestore()
        if not hasattr(store, 'get_libraries'):
            print ("###### This modulestore does not support get_libraries() ######")
        libraries = store.get_libraries()  # BIS DEBUG deliberately crossing wires (course instead of lib)
        for lib in libraries:
            print(f'####### found library {lib.display_name}')
            self._display_library(lib.location.library_key)
        print("****** Done searching ******")



    def _display_library(self, library_key):
        """
        Displays single library
        """
        print(f"****** Looking for block info on {str(library_key)} library")
        # library_key = CourseKey.from_string(library_key_string)
        if not isinstance(library_key, LibraryLocator):
            print("Non-library key passed to content libraries API.")  # Should never happen due to url regex
            exit(0)

        library = modulestore().get_library(library_key)
        if library is None:
            print("Library not found", str(library_key))
            exit(0)

        response_format = 'json'
        json_info = library_blocks_view(library, 'delete_library management command', response_format).data
        print(json.dumps(json_info))
        print("****** Done looking for block info ******")
