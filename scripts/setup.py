#!/usr/bin/env python3

from pathlib import Path
from binascii import hexlify
import os
import sys
import shutil

os.chdir(os.path.dirname(sys.argv[0]))
env_file = Path("../.env")


def prompt(text):
    response = input(text)
    if response == "y":
        return True
    else:
        return False

if env_file.exists():
    print("File .env already exists!")
    if prompt("Would you like to create a new one? [y/N]"):
        env_file.unlink()
        env_file.touch()
    else:
        sys.exit(0)

mysql_root_pw = input("Enter a password for the database. Defaults to 'banana': ") or "banana"

host_media_dir = Path(
    input("Enter a location for media directory relative to the root directory. Defaults to '/media/lecture_viewer': ")
    or "/media/lecture_viewer"
).expanduser()
if not (host_media_dir.exists() and host_media_dir.is_dir()):
    print("{} not found, creating directory".format(host_media_dir))
    os.system("sudo mkdir -p {}".format(host_media_dir))

signing_key = input("Enter a custom signing key (not suggested). Defaults to 64 character random string: ")
if not signing_key:
    signing_key = hexlify(os.urandom(32)).decode()

school_logo = Path(input("Enter a location for school logo relative to the root directory: ")).expanduser()
if school_logo.is_file():
    shutil.copy(str(school_logo), "../lv-client/client/src/images/logo.png")
else:
    print("WARNING: school logo file does not exist")

users_csv_path = Path(
    input("Enter a location for users csv path relative to {}, previously provided directory: "
          .format(host_media_dir))).expanduser()
if not Path("../lv-media", users_csv_path).is_file():
    print("WARNING: users csv file does not exist")
    users_csv_path = ""

print("Generating .env file")
env_file.write_text("""SIGNING_KEY={signing_key}

# lv-db
MYSQL_HOSTNAME=lv-db
MYSQL_ROOT_PASSWORD={mysql_root_pw}
MYSQL_DATABASE=lecture_viewer
MYSQL_USER=root

# lv-media
MEDIA_HOSTNAME=lv-media
HOST_MEDIA_DIR={host_media_dir}
MEDIA_SERVER_PORT=5000
USERS_CSV_PATH={users_csv_path}

# lv-server
SERVER_HOSTNAME=lv-server
API_VERSION=v1

# lv-client
CLIENT_HOSTNAME=lv-client
SCHOOL_LOGO_PATH={school_logo}
""".format(signing_key=signing_key, mysql_root_pw=mysql_root_pw, host_media_dir=host_media_dir,
           users_csv_path=users_csv_path, school_logo=school_logo))
