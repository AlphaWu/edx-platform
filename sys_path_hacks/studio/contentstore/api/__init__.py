from sys_path_hacks.warn import warn_deprecated_import

warn_deprecated_import('cms.djangoapps', 'contentstore.api')

from cms.djangoapps.contentstore.api import *
