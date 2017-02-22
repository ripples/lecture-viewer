import os
import subprocess
from sys import exit
from binascii import hexlify

defaults = {}


def _configure_defaults():
    global defaults
    docker_toolbox = False
    try:
        p = subprocess.Popen(["docker-machine", "ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        docker_toolbox = not bool(p.stderr.read())
    except FileNotFoundError as e:
        try:
            subprocess.Popen(["docker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError as e:
            print("ERROR: Either docker or docker-toolbox must be installed and running")
            exit()

    defaults = {
        "SIGNING_KEY": hexlify(os.urandom(32)).decode(),
        "NODE_ENV": "development",
        "MYSQL_ROOT_PASSWORD": "banana",
        "MAILER_USER": "",
        "MAILER_PASSWORD": "",
        "CLIENT_BASE_URL": "http://{}".format(p.stdout.read().decode("utf-8").rstrip()
                                              if docker_toolbox else "localhost"),
        "SCHOOL_LOGO_PATH": "logo.png",
        "DEV_EMAIL": ""
    }


_configure_defaults()
