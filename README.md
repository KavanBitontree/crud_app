# FastAPI Backend with Auth and CRUD Routes

This backend provides FastAPI routes for user signup/login plus the existing car and fuel-entry CRUD APIs. It can run with SQLite for local MVP usage or PostgreSQL via `DATABASE_URL`.

## Features

### Authentication
- Create users with `POST /signup`
- Log in with `POST /login`
- Store salted PBKDF2 password hashes
- Return a bearer JWT token on successful login

### Car Management
- Create, read, update, and delete car records
- Store car details (brand, model, year)

### Fuel Entry Tracking
- Log fuel entries for each car (liters, kilometers, timestamp)
- Calculate fuel efficiency/mileage based on historical data
- Track fuel history per vehicle

### API Endpoints

#### Auth Routes
- `POST /signup` - Create a new user
- `POST /login` - Authenticate a user and return a JWT bearer token

#### Car Routes (`/cars`)
- `POST /cars/create_car` - Create a new car
- `GET /cars/get_all_cars` - Retrieve all cars
- `GET /cars/get_car_by_id/{car_id}` - Get a specific car
- `PUT /cars/update_car_by_id/{car_id}` - Update all car fields
- `PATCH /cars/patch_car_by_id/{car_id}` - Partial car update
- `DELETE /cars/delete_car_by_id/{car_id}` - Delete a car

#### Fuel Entry Routes (`/fuel_entries`)
- `POST /fuel_entries/create_fuel_entry` - Create a fuel entry
- `GET /fuel_entries/get_all_fuel_entries` - Get all fuel entries
- `GET /fuel_entries/get_fuel_entries_by_car_id/{car_id}` - Get fuel entries for a specific car
- `GET /fuel_entries/get_latest_mileage_by_car_id/{car_id}` - Calculate latest mileage for a car
- `DELETE /fuel_entries/delete_fuel_entry_by_id/{fuel_entry_id}` - Delete a fuel entry

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+
- **SQLAlchemy**: SQL toolkit and Object Relational Mapping (ORM) for Python
- **PostgreSQL**: Powerful, open-source relational database
- **Pydantic**: Data validation and parsing library
- **Alembic**: Database migration tool
- **pgAdmin4**: PostgreSQL administration and management platform

## Docker Setup

### Starting PostgreSQL with Docker
To run PostgreSQL using Docker:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=cars \
  -p 5432:5432 \
  postgres:latest
```

### Starting pgAdmin4 with Docker
To run pgAdmin4 for database management:

```bash
docker run -d \
  --name pgadmin \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin123 \
  -p 5050:80 \
  dpage/pgadmin4
```

After starting pgAdmin4, access it at `http://localhost:5050` and connect to your PostgreSQL database using:
- Host: localhost
- Port: 5432
- Username: postgres
- Password: admin123

## Environment Configuration

Configuration is read from environment variables, optionally loaded from a local `.env` file:

```
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
DB_ECHO=false
```

For PostgreSQL, set `DATABASE_URL=postgresql://postgres:admin123@localhost:5432/cars`.

## Dependencies

The project uses the following main dependencies:
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- alembic
- python-dotenv
- pytest
- httpx

## Database Migrations

This application uses Alembic for database migrations. Run migrations with:

```bash
alembic upgrade head
```

To create new migrations:

```bash
alembic revision --autogenerate -m "Description of changes"
```

## Running the Application

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

Swagger/OpenAPI docs are available at `http://localhost:8000/docs`.

## Running Tests

```bash
pytest
```
