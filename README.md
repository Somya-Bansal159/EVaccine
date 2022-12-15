# EVaccine
An Online Covid19 vaccine registration portal

Designed using HTML CSS JS Bootstrap, linked with MySQL framework using Django.

## To run the portal:
- Clone the repository using `git clone https://github.com/Somya-Bansal159/EVaccine/`
- Enter the EVaccine directory and create a virtual environment using `virtualenv .venv` command
- Run pip install -r requirements.txt
- Activate the virtualenv by `source .venv/bin/activate` and then install python dependencies using `pip install -r requirements.txt`
- Run the sql files to prepopulate the database.
- Run `python manage.py migrate` to setup your datatbase.
- Run `python manage.py createsuperuser` to setup initial superuser to access the admin panel.
