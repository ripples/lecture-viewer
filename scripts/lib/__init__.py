from getpass import getpass
from pathlib import Path
from sys import platform, exit
from os import makedirs, mkdir, path
import shutil

env_file = Path(".env")
envs = {}
unix = False

if platform.startswith("linux") or platform == "darwin":
    from .unix_defaults import defaults

    defaults = defaults
    unix = True
elif platform == "win32":
    from .windows_defaults import defaults

    defaults = defaults


def _prompt(text):
    response = input(text + " [y/N]")
    if response == "y":
        return True
    else:
        return False


def _request_input(text, env=None, password=False, with_path=False, display_default=True):
    default = defaults[env] if env else None
    prompt_text = "{} | Defaults to {}: ".format(text, default) if default and display_default else text

    result = (getpass(prompt_text) if password else input(prompt_text)) or default

    if with_path:
        result = Path(path.expanduser(str(Path(result))))

    if env:
        envs[env] = result
    return result


def setup():
    def setup_mailer():
        if not (_request_input("Enter a gmail mailer username: ", env="MAILER_USER") and
                _request_input("Enter a gmail mailer password: ", env="MAILER_PASSWORD", password=True)):
            print("WARNING: both a mailer username and password is needed to send emails")

    def setup_db():
        _request_input("Enter password for the database", env="MYSQL_ROOT_PASSWORD", password=True)

    def setup_media_dir():
        host_media_dir = _request_input(
            "Enter a location for media directory relative to the root directory.", env="HOST_MEDIA_DIR", with_path=True
        )
        if not (host_media_dir.exists() and host_media_dir.is_dir()):
            print("{} not found, creating directory".format(host_media_dir))
            makedirs(str(host_media_dir))

        return host_media_dir

    def setup_media_files(host_media_dir):
        school_logo = host_media_dir.joinpath(_request_input(
            "Enter a location for school logo path relative to previously provided media directory '{}'".format(
                host_media_dir), env="SCHOOL_LOGO_PATH", with_path=True))

        if school_logo.is_file():
            shutil.copy((str(school_logo)), "./lv-client/client/src/images/logo.png")
        else:
            print("WARNING: school logo file does not exist")

        users_csv_path = _request_input(
            "Enter a location for users csv path relative to previously provided media directory '{}'".format(
                host_media_dir), env="USERS_CSV_PATH", with_path=True)
        if not host_media_dir.joinpath(users_csv_path).is_file():
            print("WARNING: users csv file does not exist")

    def setup_miscellaneous():
        envs["NODE_ENV"] = "production" if _prompt("Is this a production environment?") else defaults["NODE_ENV"]
        _request_input("Enter a custom signing key (not suggested). | Defaults to 64 character random string: ",
                       env="SIGNING_KEY", display_default=False)
        _request_input("Enter the host url for the Lecture Viewer.", env="CLIENT_BASE_URL")

    if env_file.exists():
        print("File .env already exists!")
        if _prompt("Would you like to create a new one?"):
            env_file.unlink()
            env_file.touch()
        else:
            exit(0)

    setup_miscellaneous()
    setup_mailer()
    setup_db()
    media_dir = setup_media_dir()
    setup_media_files(media_dir)
    print("Generating .env file")

    with env_file.open(mode="w") as file:
        file.write("""SIGNING_KEY={SIGNING_KEY}
NODE_ENV={NODE_ENV}

# lv-db
MYSQL_HOSTNAME=lv-db
MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=lecture_viewer
MYSQL_USER=root

# lv-media
MEDIA_HOSTNAME=lv-media
HOST_MEDIA_DIR={HOST_MEDIA_DIR}
MEDIA_SERVER_PORT=5000
USERS_CSV_PATH={USERS_CSV_PATH}

# lv-server
SERVER_HOSTNAME=lv-server
SERVER_PORT=3000
API_VERSION=v1
MAILER_USER={MAILER_USER}
MAILER_PASSWORD={MAILER_PASSWORD}

# lv-client
CLIENT_HOSTNAME=lv-client
CLIENT_BASE_URL={CLIENT_BASE_URL}
SCHOOL_LOGO_PATH={SCHOOL_LOGO_PATH}
""".format(**envs))

    if not envs["NODE_ENV"] == "production" and not Path(media_dir, "F16").exists():
        mkdir(str(Path(media_dir, "F16")))
