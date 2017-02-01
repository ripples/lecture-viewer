from .defaults import defaults

_windows_defaults = {
    "HOST_MEDIA_DIR": "C:\\Users\\{}\\Documents\\lecture_viewer_media".format(getuser())
}

defaults = {**defaults, **_windows_defaults}
