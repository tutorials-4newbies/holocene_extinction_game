# What is this
A tribute to the Extinctathon game as described in [Orxy and Crake](https://www.oryxandcrake.co.uk/)

>Adam named the living animals, MaddAddam names the dead ones

You can read more about the current ongoing Holocene extinction, that might be rightly called the 
[anthropocene extinction](https://storymaps.arcgis.com/stories/73ab69fedac54685ae837562e3389d13)

## Technology

Django + drf + django-filter
DB in postgresql
Django configurations for settings file
Common practice middlewares (timezones, querycount)

## setup
## Setup for development

1. Python virtual environment:   
We are using poetry to manage the projects dependencies.   
   **Install Poetry** - https://python-poetry.org/docs/#installation
        

2. Get the code:    
Clone this project    
   ```bash
   # with https   
   git clone https://github.com/tutorials-4newbies/holocene_extinction_game.git
   # with ssh
   git clone git@github.com:tutorials-4newbies/holocene_extinction_game.git
   ```
   

3. Install dependencies:    
enter projects directory and install dependencies using Poetry. Poetry will look for pyproject.toml file
    ```
    cd holocene_extinction_game
    poetry install
    ```
   And enter the virtual env created by Poetry:
   ```
   poetry shell
   ```
   
---
### From this point in the setup you should run the commands while you are inside the virtual env / poetry shell 

---

4. Database:    
We are currently using postgres. You need to set up a user,
   * After you have installed postgres, enter postgres cli client:    
   ```
   sudo su - postgres
   psql
   ```
   * create a database, a user and a role
    ```
    CREATE DATABASE holocene_extinction_game_db;
    CREATE USER holocene_extinction_game_user WITH PASSWORD 'holocene_extinction_game_pass';
    ALTER ROLE holocene_extinction_game_user SET client_encoding TO 'utf8';
    GRANT ALL PRIVILEGES ON DATABASE holocene_extinction_game_db TO holocene_extinction_game_user;
    ALTER ROLE holocene_extinction_game_user CREATEDB;
   ```
   * to exit postgres cli:   
   `Ctrl+D`
   
     and then exit superuser shell   
   `exit`
    * Now you can migrate the data:
   ```   
   python manage.py migrate   
   ```   

5. Create a superuser for yourself to start working
    ```
    python manage.py createsuperuser 
   ```

6. Run the dev server
    ```
   python manage.py runserver
   ```
 
### tests

```bash
poetry run python manage.py test
```

## Setup for use in local environment as a "black box"
e.g when you work on the frontend

```bash
docker-compose up
```
First run would be quite long because of docker building

