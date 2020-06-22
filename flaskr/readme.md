# Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Endpoints

GET '/actors'
- Fetches a dictionary of actors 
- Request Arguments: None
- Returns: An object with actors, success, total_actors as key:value pairs. 
{
  "actors": [
    {
      "age": 55.0,
      "gender": "Male",
      "id": 60,
      "name": "Aamir Khan "
    },
    {
      "age": 40.0,
      "gender": "Male",
      "id": 62,
      "name": "Shahid Kapoor"
    },
    {
      "age": 35.0,
      "gender": "Female",
      "id": 63,
      "name": "Kajal Aggarwal"
    }
  ],
  "success": true,
  "total_actors": 3
}

POST '/actors'
- Add actor to database
- Request Arguments: name, age, gender
- Returns: An object with created, success as key:value pairs.
{
  "created": {
    "age": 40.0,
    "gender": "Male",
    "id": 64,
    "name": "Ajay Devgan"
  },
  "success": true
}

PATCH '/actors/<int:actor_id>'
- Update actor to database
- Request Arguments: id, data to be updated - name, age, gender
- Returns: An object with actor, success as key:value pairs.
{
  "actor": {
    "age": 62.0,
    "gender": "Male",
    "id": 60,
    "name": "Aamir Khan "
  },
  "success": true
}

DELETE '/actors/<int:actor_id>'
- Delets actor form database
- Request Arguments: actor id
- Returns: An object with deleted, success  as key:value pairs. 
{
  "deleted": 63,
  "success": true
}

GET '/movies'
- Fetches a dictionary of movies 
- Request Arguments: None
- Returns: An object with movies, success, total_movies as key:value pairs. 
{
  "movies": [
    {
      "id": 2,
      "release_date": "Mon, 21 May 2018 00:00:00 GMT",
      "title": "Life of a Pie"
    },
    {
      "id": 4,
      "release_date": "Mon, 21 May 2018 00:00:00 GMT",
      "title": "Rabta"
    }
  ],
  "success": true,
  "total_movies": 2
}

POST '/movies'
- Add movie to database
- Request Arguments: title, release_date(YYYY-MM-DD)
- Returns: An object with created, success as key:value pairs.
{
  "created": {
    "id": 20,
    "release_date": "Wed, 16 May 2012 00:00:00 GMT",
    "title": "3 Idiots"
  },
  "success": true
}

PATCH '/movies/<int:movie_id>'
- Update movie to database
- Request Arguments: id, data to be updated - title, release_date
- Returns: An object with movie, success as key:value pairs.
{
  "movie": {
    "id": 20,
    "release_date": "Wed, 16 May 2012 00:00:00 GMT",
    "title": "3 Idiots"
  },
  "success": true
}

DELETE '/movies/<int:movie_id>'
- Delets movie form database
- Request Arguments: movie id
- Returns: An object with deleted, success as key:value pairs.
{
  "deleted": 63,
  "success": true
}

## Testing
To run the tests, run
```
python test_app.py
```