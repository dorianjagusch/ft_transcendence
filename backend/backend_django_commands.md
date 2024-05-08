## To access the backend container
`docker exec -it backend_c sh`
or go to Docker dashboard and go to backend_c and its exec tab

## To view backend development server logs
Go to Docker dashboard and go to backend_c and its logs tab

## To empty the backend database
#### (extremely useful when running Postman REST api tests multiple times)
*in container, run:* `python manage.py flush --no-input` 
