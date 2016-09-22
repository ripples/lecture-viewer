#!/usr/bin/env bash

OS_NAME=$(uname -s)
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P) # So we're at the script location

if [ -f ../.env ]; then
  echo "File .env already exists!"
  read -r -p "Would you like to create a new one? [y/N] " create
  create=$(echo "$create" | tr '[:upper:]' '[:lower:]')   # to lower
  if [[ ${create} =~ ^(yes|y)$ ]]; then
    rm ../.env
    touch ../.env
  else
    exit
  fi
fi

read -r -p "Enter a password for the database. Defaults to 'banana': " mysql_root_pw
: ${mysql_root_pw:=banana}
read -r -p "Enter a location for media directory relative to the root directory. Defaults to '/media/lecture_viewer': " host_media_dir
: ${host_media_dir:=/media/lecture_viewer}
read -r -p "Enter a custom signing key (not suggested). Defaults to 32 character random string: " signing_key

if [ "$OS_NAME" == Linux ]; then
  UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
else
  UUID=$(cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 32)
fi
: ${signing_key:=${UUID}}

echo "Generating .env file"
cat > ../.env <<- env_file
SIGNING_KEY=${signing_key}

# lv-db
MYSQL_ROOT_PASSWORD=${mysql_root_pw}
MYSQL_DATABASE=lecture_viewer
MYSQL_HOSTNAME=lv-db
MYSQL_USER=root

# lv-media
HOST_MEDIA_DIR=${host_media_dir}
IMAGE_MEDIA_DIR=/media
MEDIA_SERVER_PORT=5000

# lv-server
API_VERSION=v1

### Temporary until I think of a good solution
SEMESTER=S16
env_file

if [ ! -d ../.env ]; then
  echo "${host_media_dir} not found, creating directory"
  sudo mkdir -p ${host_media_dir}
fi
