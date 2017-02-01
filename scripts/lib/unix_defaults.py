from .defaults import defaults

_unix_defaults = {
    "HOST_MEDIA_DIR": "/media/lecture_viewer",
}

defaults = {**defaults, **_unix_defaults}
