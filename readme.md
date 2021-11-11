Wagtail Space
=============

Wagtail Space is a Wagtail event hosted by Four Digits in Arnhem, The Netherlands.

We like others to organise Wagtail Space events as well.

If you like to organise a Wagtail meet up, sprint or conference you may use the Wagtail Space name, graphics and website!

What we propose:

    - Name your Wagtail event: 'Wagtail Space [CityName]'. Eg: 'Wagtail Space Philadelphia'.
    - Notify Four Digits and get a subdomain (philadelphia.wagtail.space)
    - We list your event on [wagtail.space](https://wagtail.space)
    - Provide hosting yourself (supply an ip address)
    - Notify Wagtail Core team of your event plans


Install
-------

Clone this repo:

    git clone git@github.com:wagtail/wagtailspace-us.git


Create a Python 3.6 environment and install Python packages:

    python3 -m venv .venv/
    source .venv/bin/activate
    pip install -r requirements.txt


Configure your database. Copy and edit local.py. (secret key and database credentials).

    cp wagtailspace/settings/local.py.example wagtailspace/settings/local.py
    vi wagtailspace/settings/local.py


Migrate and create a user:

    python manage.py migrate
    python manage.py createsuperuser

Build front-end:

    npm install -g yarn
    yarn
    yarn build

Runserver:

    python manage.py runserver


Frontend
--------

Install NodeJS (last tested with version 14). Then install yarn with:

    npm install -g yarn

Install project packages:

    yarn

Run the development web server. This should be run in tandem with Django runserver.

    yarn start


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


Deploying on CodeRed Cloud
--------------------------

Build the frontend locally:

    git pull origin master
    yarn build

Copy the code and static assets to the server using SFTP (credentials can be
accessed through CodeRed dashboard at https://app.codered.cloud/)

    cat codered-deploy.txt | sftp wagtailspace-us@wagtailspace-us.codered.cloud

From the CodeRed Dashboard > Websites > Deployment tab click
**Redeploy Production** which will reinitialize the runtime with the new code
(and automatically runs pip install, collectstatic, migrate, etc.).
