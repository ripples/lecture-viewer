import os
import subprocess
from binascii import hexlify

defaults = {}


def _configure_defaults():
    global defaults
    p = subprocess.Popen(["docker-machine", "ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    docker_toolbox = not bool(p.stderr.read())

    defaults = {
        "SIGNING_KEY": hexlify(os.urandom(32)).decode(),
        "NODE_ENV": "development",
        "MYSQL_ROOT_PASSWORD": "banana",
        "MAILER_USER": None,
        "MAILER_PASSWORD": None,
        "CLIENT_BASE_URL": "http://{}".format(p.stdout.read().decode("utf-8") if docker_toolbox else "localhost"),
        "USERS_CSV_PATH": "users.csv",
        "SCHOOL_LOGO_PATH": "logo.png",
    }


_configure_defaults()
