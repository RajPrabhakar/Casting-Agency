# Casting Agency API

The Casting Agency models a company that is responsible for creating and managing actors, movies and characters.
Additionally, Characters will be assigned to Actors and Movies.

Hosted API URL: https://superhero-casting-agency.herokuapp.com/

## Available Endpoints

1. **Public Endpoints** - No token required - Will be able to view the list of available movies, actors and characters.
    ```bash
    GET / - list of tokens and public endpoints
    GET /movies - list of movies
    GET /actors - list of actors
    GET /characters - list of characters
    ```

2. **Casting Assistant** - token available in index - Will be able to access Public Endpoints + Details of specific movie, actor or character.
    ```bash
    GET /movies/<id> - specific movie details along with associated characters and actors
    GET /actors/<id> - specific actor details along with associated movies and characters
    GET /characters/<id> - specific character details along with associated movies and actors
    ```

3. **Casting Director** - token available in index - Will be able to access Casting Assistant Endpoints + Add/Delete Actors & Characters + Update Actors/Movies/Characters.
    ```bash
    PATCH /movies/<id> - update existing movie details
    POST /actors - add a new actor to the database
    PATCH /actors/<id> - update existing actor details
    DELETE /actors/<id> - delete a specific actor from database
    POST /characters - add a new character to the database
    PATCH /characters/<id> - update existing character details
    DELETE /characters/<id> - delete a specific character from database
    ```

4. **Executive Producer** - token available in index - Will be able to access Casting Director Endpoints + Add/Delete Movies.
    ```bash
    POST /movies - add a new movie to the database
    DELETE /movies/<id> - delete a specific movie from database
    ```

## Installation

```bash
gh repo clone RajPrabhakar/Casting-Agency
python -m venv venv
venv/Scripts/activate
cd casting-agency
pip install -r requirements.txt
python app.py
```

## API Documentation

### Endpoints

1. **GET /**
- description: list of tokens and public endpoints
- roles required: nil
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/'
```
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
2. **GET /movies**
- description: list of available movies
- roles required: nil
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/movies'
```
```bash
{
    "movies": [
        {
            "id": 1,
            "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg",
            "release_date": "Fri, 13 Dec 2013 00:00:00 GMT",
            "title": "The Hobbit: The Desolation of Smaug"
        }
    ],
    "success": true
}
```
3. **GET /actors**
- description: list of available actors
- roles required: nil
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/actors'
```
```bash
{
    "actors": [
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70",
            "name": "Benedict Cumberbatch"
        }
    ],
    "success": true
}
```
4. **GET /characters**
- description: list of available characters
- roles required: nil
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/characters'
```
```bash
{
    "characters": [
        {
            "artist_id": 1,
            "id": 1,
            "movie_id": 1,
            "name": "Bilbo Baggins"
        }
    ],
    "success": true
}
```
5. **GET /movies/<id>**
- description: detailed view of the requested movie
- roles required: Casting Assistant
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/movies/1' \
--header 'Authorization: Bearer eyJhb...'
```
```bash
{
    "movie": {
        "cast": [
            {
                "actor": {
                    "id": 1,
                    "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70",
                    "name": "Benedict Cumberbatch"
                },
                "character_id": 1,
                "character_name": "Bilbo Baggins"
            }
        ],
        "id": 1,
        "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg",
        "release_date": "Fri, 13 Dec 2013 00:00:00 GMT",
        "title": "The Hobbit: The Desolation of Smaug"
    },
    "success": true
}
```
6. **GET /actors/<id>**
- description: detailed view of the requested actor
- roles required: Casting Assistant
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/actors/1' \
--header 'Authorization: Bearer eyJhb...'
```
```bash
{
    "actor": {
        "age": 45,
        "gender": "male",
        "id": 1,
        "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70",
        "movies": [
            {
                "character_id": 1,
                "character_name": "Bilbo Baggins",
                "movie": {
                    "id": 1,
                    "poster": "https://images-na.ssl-images-amazon.com/images/I/91W-zEXbx8L._SL1400_.jpg",
                    "title": "The Hobbit: The Desolation of Smaug"
                }
            }
        ],
        "name": "Benedict Cumberbatch"
    },
    "success": true
}
```
7. **GET /characters/<id>**
- description: detailed view of the requested character
- roles required: Casting Assistant
```bash
curl --location --request GET 'https://superhero-casting-agency.herokuapp.com/characters/1' \
--header 'Authorization: Bearer eyJhb...'
```
```bash
{
    "character": {
        "actor_name": "Benedict Cumberbatch",
        "artist_id": 1,
        "id": 1,
        "movie_id": 1,
        "movie_title": "The Hobbit: The Desolation of Smaug",
        "name": "Bilbo Baggins"
    },
    "success": true
}
```
8. **POST /actors**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
curl --location --request POST 'https://superhero-casting-agency.herokuapp.com/actors' \
--header 'Authorization: Bearer eyJhb...' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Benedict Cumberbatch",
    "age": "45",
    "gender": "male",
    "image": "https://api.time.com/wp-content/uploads/2015/01/benedict-cumberbatch.jpg?w=824&quality=70"
}'
```
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: Casting Director
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: nil
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
1. **GET /**
- description: list of tokens and public endpoints
- roles required: nil
```bash
{
  "access_tokens": {
    "casting_assistant": "eyJhbGci...",
    "casting_director": "eyJhbGciO...",
    "executive_producer": "eyJhbGc..."
  },
  "available_links": {
    "actors": "/actors",
    "character": "/character",
    "movies": "/movies"
  },
  "success": true
}
```
