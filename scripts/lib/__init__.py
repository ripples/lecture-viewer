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
    default = defaults.get(env) if env else ""
    prompt_text = "{} | Defaults to {}: ".format(text, default) if default and display_default else text

    result = (getpass(prompt_text) if password else input(prompt_text)) or default

    if with_path:
        result = Path(path.expanduser(str(Path(result))))

    if env:
        envs[env] = result
    return result


def setup():
    def setup_mailer():
        mailer_user = _request_input("Enter a gmail mailer username: ", env="MAILER_USER")
        mailer_password = _request_input("Enter a gmail mailer password: ", env="MAILER_PASSWORD", password=True)
        if not (mailer_user and mailer_password):
            print("WARNING: both a mailer username and password is needed to send emails")

    def setup_db():
        _request_input("Enter password for the database", env="MYSQL_ROOT_PASSWORD", password=True)

    def setup_media_dir():
        host_media_dir = _request_input(
            "Enter a location for media directory relative to the root directory.", env="HOST_MEDIA_DIR", with_path=True
        )
        users_dir = host_media_dir.joinpath('users')
        resources_dir = host_media_dir.joinpath('resources')
        inserted_users = users_dir.joinpath('inserted')

        if not (host_media_dir.exists() and host_media_dir.is_dir()):
            print("{} not found, creating directory".format(host_media_dir))
            makedirs(str(host_media_dir))
        if not (users_dir.exists() and users_dir.is_dir()):
            print("{} not found, creating directory".format(users_dir))
            makedirs(str(users_dir))
        if not (resources_dir.exists() and resources_dir.is_dir()):
            print("{} not found, creating directory".format(resources_dir))
            makedirs(str(resources_dir))
        if not (inserted_users.exists() and inserted_users.is_dir()):
            print("{} not found, creating directory".format(inserted_users))
            makedirs(str(inserted_users))

        return host_media_dir, users_dir, resources_dir

    def setup_resources_files(resources_dir):
        school_logo = resources_dir.joinpath(_request_input(
            "Enter a location for school logo path relative to resources directory '{}'".format(resources_dir),
            with_path=True, env="SCHOOL_LOGO_PATH"))
        if school_logo.is_file():
            shutil.copy((str(school_logo)), "./lv-client/client/src/images/logo.png")
        else:
            print("WARNING: school logo file does not exist")

        splash_screen = resources_dir.joinpath(_request_input(
            "Enter a location for splash screen path relative to resources directory '{}'".format(resources_dir),
            with_path=True, env="SPLASH_SCREEN_PATH"))
        if splash_screen.is_file():
            shutil.copy((str(school_logo)), "./lv-client/client/src/images/splash.jpg")
        else:
            print("WARNING: splash screen file does not exist")

    def setup_miscellaneous():
        envs["NODE_ENV"] = "production" if _prompt("Is this a production environment?") else defaults["NODE_ENV"]
        _request_input("Enter a custom signing key (not suggested). | Defaults to 64 character random string: ",
                       env="SIGNING_KEY", display_default=False)
        _request_input("Enter the host url for the Lecture Viewer.", env="CLIENT_BASE_URL")

    def setup_dev():
        _request_input("Enter dev email, this should be your umass email: ",
                       env="DEV_EMAIL", display_default=False)

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
    media_dir, users_dir, resources_dir = setup_media_dir()
    setup_resources_files(resources_dir)

    if envs["NODE_ENV"] == "development":
        setup_dev()

    print("Generating .env file")

    with env_file.open(mode="w") as file:
        formatted_file = """SIGNING_KEY={SIGNING_KEY}
NODE_ENV={NODE_ENV}
HOST_MEDIA_DIR={HOST_MEDIA_DIR}

# lv-db
MYSQL_HOSTNAME=lv-db
MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=lecture_viewer
MYSQL_USER=root

# lv-media
MEDIA_HOSTNAME=lv-media
MEDIA_SERVER_PORT=5000

# lv-server
SERVER_HOSTNAME=lv-server
SERVER_PORT=3000
API_VERSION=v1
MAILER_USER={MAILER_USER}
MAILER_PASSWORD={MAILER_PASSWORD}

# lv-client
CLIENT_HOSTNAME=lv-client
CLIENT_PORT=3000
CLIENT_BASE_URL={CLIENT_BASE_URL}
""".format(**envs)
        if envs["NODE_ENV"] == "development":
            formatted_file += """
DEV_EMAIL={DEV_EMAIL}
""".format(**envs)
        file.write(formatted_file)

    if not envs["NODE_ENV"] == "production" and not Path(media_dir, "F16").exists():
        mkdir(str(Path(media_dir, "F16")))
