
# Description

# Tech Stack
- Docker
- React.js
- React-Bootstrap
- Django w/ DRF

# Setup

## Build + Deploy Frontend/Backend

-   Run the initial setup:
    `make docker_setup`
-   Create the migrations for `users` app:
    `make docker_makemigrations`
-   Run the migrations:
    `make docker_migrate`
-   Run the project:
    `make docker_up`

## Seed test data

- run `docker compose run --rm backend bash` to open an interactive shell
- run `python manage.py seed_data`

## Create admin user

- run `docker compose run --rm backend bash` to open an interactive shell (if not already in shell)
- run `python manage.py createsuperuser`

## Access django admin

- Navigate to `localhost:8000/admin`

## Access frontend

- Navigate to `localhost:8000`

## Run Tests

# What is needed to make this production ready?
If I was to further improve this app, I would
1. Allow the user to provide a list of urls, and run a celery scraping task for each url. I would create batch/task db entities to represent the status of the scraping batch/task, so the app can display previous scraping batches/tasks for a given set of urls.

# Feature improvements?

# TODO
- finish multi select component
- allow adding recipe once scraped
- update data model unique constraints, add url + lastupdated to recipe
- add header
- add unit tests
- add instructions to readme