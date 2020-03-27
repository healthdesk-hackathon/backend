# Django template
![coverage](https://git.smartfactory.ch/web-template/template-django/badges/develop/coverage.svg)

## Add the in-docker Python interpreter in Pycharm

_Note: You might need to go through this procedure first since Catalina: https://stackoverflow.com/questions/58371028/pycharm-cant-create-remote-python-interpreter-using-docker-compose/58379351#58379351_

- Go to `preferences -> project -> project interpreter`
- Add a new interpreter
- In the interpreter creation dialog, click the  `Docker compose` option
- Select the `docker-compose.dev.yml` at the root of the project
- Select the `dev_backend` service if not automatically selected

Regarding new packages installation, for now the only option is to rebuild the container when it happens with the following command (after running the pipenv command outside of the container):

```bash
# In the backend
docker-compose -f ../docker-compose.dev.yml build --no-cache
```

In order to run the management commands, you can use in Pycharm `Tools -> Run manage.py task` or `Alt-R`.
You can safely use this way to create the new migration files, since this is a mounted volume.

Note that the python console will be as well run in the docker container. You can check the containers in the `Service` tab at the bottom

In order to allow the backend to accept redirection from the proxy, you'll need to set the host to `0.0.0.0` in the Run configuration, then you are good to go.

### Tips

- With this setup the terminal won't automatically open in the correct environment anymore. If you need to run something in the terminal, you will have to run it in the container
- This should not happen often, since you can use `Alt+R` in order to run a manage.py command, and the python console opens in the docker container directly

## Setup

You are not supposed to clone this project manually. You should instead enable the `django` part during the `template-core` setup. What follows next should still be done.

The only thing you need to do after having created/cloned is copying the `.env.example` file to `.env`. 

Please note that Docker is not needed on development environment.

## Deployment

When deploying for the first time through the CI job, you will be asked to finish your setup 
directly on the server (see [here](https://git.smartfactory.ch/web-template/template-core#setup-1)).

For this template, you will indeed need to customize the `backend/.env.testing` and `backend/.env.prod
files` (depending on the type of deployment you are doing; create both if you want to have both production and testing on the same server) 
in order to suit your setup. If they don't exist, create them by copying and renaming `backend/.env.example`

## Features

- Django Rest Framework
- Auto generated Swagger doc
- JWT authentication enabled
- User already overrided, as advised by Django docs
- Completely dockerized
- CI ready -> testing + image build + push on repo registry. Deployment process is handled by `template-core`
- `template-core` compatible. Use `./setup.sh enable django` to add it.
- Unit testing with Pytest already setup
- Virtual environment managed with pipenv

## Coverage

You can get the coverage badge for the whole project by using this url:

```
https://git.smartfactory.ch/<group>/<project>/badges/master/coverage.svg
```

If you want the coverage badge only for the backend, you can simply specify the job, as follow:

```
https://git.smartfactory.ch/<group>/<project>/badges/master/coverage.svg?job=backend-test-application
```

Note: In this example, the branch master is used, but develop has a badge as well.
