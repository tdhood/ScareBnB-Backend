 To install:
 In terminal: git clone 'URL'

    Go to directory location of clone in terminal

    Create a virtual environment:
    Terminal: python3 -m venv [preferred name for virtual environment]

    Start virtual environment!
    Terminal: source bin/activate/[preferred name for virtual environment]

    Install requirements;
    Terminal: pip install -r requirements.txt

To seed database:
In terminal: psql scarebnb -f scarebnb.sql
or
In terminal: python3 seed.py