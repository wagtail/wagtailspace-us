Wagtail Space US
================

Code for website at: https://us.wagtail.space/, currently hosted on [CodeRed Cloud](https://www.codered.cloud/).


Backend
-------

Clone this repo:

    git clone git@github.com:wagtail/wagtailspace-us.git


Create a **Python 3.8** environment and install Python packages:

    python3 -m venv .venv/
    source .venv/bin/activate
    pip install -r requirements.txt


Install **Postgres 15** and configure a local database. Copy and edit local.py:

    cp wagtailspace/settings/local.py.example wagtailspace/settings/local.py


Migrate and create a user:

    python manage.py migrate
    python manage.py createsuperuser

Runserver:

    python manage.py runserver


Frontend
--------

Install **NodeJS 14**. Then install yarn with:

    npm install -g yarn

Install project packages:

    yarn

Then build the frontend:

    yarn build

Run the development web server. This should be run in tandem with Django runserver.

    yarn start


Deploying on CodeRed Cloud
--------------------------

The https://us.wagtail.space/ site is currently hosted with [CodeRed Cloud](https://www.codered.cloud/).

**NOTE:** the site will auto-deploy from the master branch on GitHub. However, if you need to manually deploy for some reason, follow the steps below.

Ensure the latest code is committed and pushed to master. Build the frontend locally:

    git pull origin master
    yarn build

Install the CodeRed deployment tool `pip install cr`. Get an API key from https://app.codered.cloud/

    cr deploy wagtailspace-us --token "your_api_key"


Deploying (Generic)
-------------------

Build the frontend locally and copy the results to the server:

    git pull origin master
    yarn build
    scp wagtailspace/static user@server.tld:/path/to/wagtailspace/wagtailspace
    scp config-prd-stats.json user@server.tld:/path/to/wagtailspace

On the server:

    pip install -r requirements.txt
    python manage.py collectstatic
    python manage.py migrate

Restart.
