## Local Repository Setup (Ubuntu 20.04)

- Clone git repository
- Open bash terminal
- Install PostgreSQL 13.x
- Ensure following package dependencies are met:  ``sudo apt install python3 python3-pip python3-dev python3-venv gcc libpq-dev``
- Create empty database in PostgreSQL with any name: For eg. ``captureatrip_db``
- Create virtualenv: ``python3 -m venv env``
- Activate virtualenv: ``source env/bin/activate``
- Copy **.env.example** in captureatrip_project directory and paste it with name **.env**.
- Add required data to env file: Set SECRET_KEY, Database credentials created in **above** steps, sandbox email, JWT Token validity. **S3 file storage config** is not required when running locally. 
- Install python dependencies: ``pip install -r requirements/common.txt``
- Install wheel: ``pip install wheel``
- Install extra dependencies: ``pip install ./email-management-appcode-0.0.1.tar.gz`` **(Refer zip file)**
- Create Database migrations: ``python3 manage.py makemigrations``
- Migrate Database: ``python3 manage.py migrate``
- Create local superuser: ``python3 manage.py createsuperuser``. This will create the user to login to Django admin.
- Seed initial data from fixtures: ``python3 manage.py loaddata */fixtures/*.json``.
- Run development server: **Ctrl+F5** or ``python3 manage.py runserver``
- That's it! Project will now be accessible on **[http://localhost:8000](http://localhost:8000)**
- Django admin will be accessible on **[http://localhost:8000/superadmin](http://localhost:8000/superadmin)**

## Create Admin User for backend
- Login to Django admin
- Open Users Table
- Add User > Enter Username and Password > Save.