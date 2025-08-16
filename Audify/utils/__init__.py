"""
Audify.utils package initializer.

Avoid importing submodules at package-import time to prevent circular
imports when other packages import specific submodules (e.g.:
`from Audify.utils.formatters import seconds_to_min`). Import
submodules directly where needed (for example: `from Audify.utils.formatters import ...`).

This file intentionally does not import submodules to keep imports lazy and safe.
"""

# Optional: list available submodules for tooling/introspection
__all__ = [
	"channelplay",
	"database",
	"decorators",
	"extraction",
	"formatters",
	"inline",
	"pastebin",
	"sys",
	"imposterdb",
]
