from sys_path_hacks.warn import warn_deprecated_import

warn_deprecated_import('cms.djangoapps', 'contentstore.admin')

from cms.djangoapps.contentstore.admin import *
