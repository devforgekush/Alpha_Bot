"""Audify.utils package initializer.

This module provides lightweight, guarded re-exports of commonly used
utility symbols so plugins that do `from Audify.utils import X` continue
to work without introducing circular imports at package import time.

Each import is guarded with try/except to keep the package importable
in minimal environments (for example during static checks or on
resource-constrained build servers). Missing re-exports will be None
or absent from __all__.
"""

__all__ = []

# Helper to attempt an import and register it in __all__ if present
def _try(name, import_from):
	try:
		module = __import__(import_from, fromlist=[name])
		obj = getattr(module, name)
		globals()[name] = obj
		__all__.append(name)
	except Exception:
		# keep missing symbols absent to avoid breaking imports
		globals()[name] = None

# Re-export formatter helpers
_try('get_readable_time', 'Audify.utils.formatters')
_try('seconds_to_min', 'Audify.utils.formatters')
_try('time_to_seconds', 'Audify.utils.formatters')
_try('int_to_alpha', 'Audify.utils.formatters')
_try('alpha_to_int', 'Audify.utils.formatters')

# Re-export inline help panel functions
_try('help_pannel', 'Audify.utils.inline.help')
_try('help_pannel_page2', 'Audify.utils.inline.help')
_try('help_pannel_page3', 'Audify.utils.inline.help')

# Re-export extraction helpers
_try('extract_user', 'Audify.utils.extraction')

# Re-export decorator checks
_try('AdminRightsCheck', 'Audify.utils.decorators.admins')

# Re-export pastebin and channelplay helpers
_try('AudifyBin', 'Audify.utils.pastebin')
_try('get_channeplayCB', 'Audify.utils.channelplay')

# Note: other utilities can be added here as needed. Keep exports small
# to avoid importing heavy optional dependencies at package import time.
