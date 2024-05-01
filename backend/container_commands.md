# To access the postgres container
docker exec -it postgres_c sh

## To access the database via postgres server
psql -U postgres -d djangoDb

## To list tables
\dt

## To list rows in the UserManagement_user table
SELECT * from "UserManagement_user";

# To access the backend container
docker exec -it backend_c sh

## To run python tests for backend
python manage.py test
