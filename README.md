# Lecture Viewer
This repository is the parent of the [Lecture-Viewer](https://github.com/ripples/lecture-viewer) system developed by the [ripples team at UMass Amherst](https://github.com/ripples).

The purpose of the Lecture-Viewer system is that it is the front facing application for the [paol](https://github.com/ripples/paol) capturing system.
It allows for lectures recorded by paol to be viewed online in a consumable format.


### Getting Started
#### Docker
To get started, you first need to install docker. Instructions for installing docker can be found [here](https://docs.docker.com/engine/installation/).
After you have docker installed, you will need to install docker compose. Follow the instructions [here](https://docs.docker.com/compose/install/).


#### Clone Recursively
This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). In order to clone everything correctly, you have to clone recursively:
```
git clone --recursive https://github.com/ripples/lecture-viewer.git
```
or
```
git clone --recursive git@github.com:ripples/lecture-viewer.git
```
More useful commands for git submodules can be found in [Repository Maintenence](#repository-maintenance) below.


#### Environment File
This application uses environment variables to make it easier to deploy at different locations.
You can either run `scrips/setup.py` or you will need to create a file named `.env` in this directory for deployment to work properly.
An example file .env file is provided at `example.env`.

If you decide to run any services manually, make sure to use the same `.env` file.


### To Run (Production)
After your environment is all set up, simply run the following fill `scripts/prod_startup.sh` or the following commands:
```
docker-compose build
docker-compose up -d
```
Everything will be exposed on port 80!


### To Run (Development)
We made a development docker-compose file that can be used in some development scenarios.
It will keep the `lv-client/public/client`, all of `lv-server` and `lv-media` up to date.
To use this environment, run `scripts/dev_startup.sh` or run the following commands:
```
docker-compose -f docker-compose.yml -f docker-compose-development.yml build
docker-compose -f docker-compose.yml -f docker-compose-development.yml up
```
Everything will be exposed on port 80!


### Repository Maintenance
For those of you who are not using a GUI to interact with git, here are some useful commands:
 * After checking out a commit (for example git pull master), this updates your submodules
    ```
    git submodule update --recursive
    ```

 * If you checked out a commit and it added a new submodule, run this command before doing anything else. 
 It initializes the submodule so commands like the above one will work
    ```
    git submodule init
    ```

 * These commands will pull from master for each submodule
    ```
    git fetch --recurse-submodules
    git submodule foreach git pull origin master
    git pull
    ```


### Production Maintenance
Some tips on maintaining a production environment
 * Make sure you are very familiar with how docker works before doing anything
 * If a container is down you can start it up again via
    ```
    docker-compose <service name> -d
    ```
 * To update a container follow these steps
    * **_WARNING_**: Do not remove lv-db containers until [#53](/../../issues/53) has been resolved
    1. Kill the container: `docker kill <container id>`
    2. Remove the container `docker rm <container id>`
    3. Remove the image `docker rmi <image id>`
    4. Pull repository `git pull`
    5. Start container `docker-compose up <service name> -d`


### Troubleshooting
##### "Help! docker-compose says files are missing!"
9 times out of 10 this is due to not updating your submodules when changing commits. Assuming you did a recursive clone of this repo, just run:
```
git submodule update --recursive
```


##### "Help! docker-compose fails at npm install!"
You most likely are running docker on Mac or Windows and have recently switched internet connections. When you switch internet connections while your docker-machine is still running, it looses it's connection. Assuming your docker-machine is called default, run:
```
docker-machine restart default
```


##### "Help! I tried updating my submodules recursively but the submodule folder(s) are empty!"
When a new submodule is added to the system and you would like to pull it onto your machine, you must first init the submodule before you are able to update it.
```
git submodule init
git submodule update --recursive
```


##### "Help! When I try to build with docker, I get a `no space left on device` error!"
After a while docker can become cluttered with old containers, images, and volumes. You can remove some manually to get unblocked, or you can use some of the following commands to remove them in bulk. Be careful not to remove anything important!
```
# delete stopped containers
docker ps -a | awk '/Exited/ {print $1}' | xargs docker rm -v

# remove dangling images
docker rmi $(docker images -f "dangling=true" -q)

# remove all images
docker rmi $(docker images -q)

# remove dangling volumes
docker volume rm $(docker volume ls -qf dangling=true)
```
