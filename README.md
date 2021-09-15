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
- list of tokens and public endpoints
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