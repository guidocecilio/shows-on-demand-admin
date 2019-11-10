Shows on-demand service
======================= 

Notice that this is a Microservice that is part of the Shows on Demand service and it in an early stage

Installation
------------

### From sources

#### Clone the Project
```bash
$ git clone https://github.com/guidocecilio/shows-on-demand-admin.git
```

Run the app using docker-compose
```bash
$ docker-compose up
```

## Initializing the Database and seeding the data
```bash
$ docker exec -it admin-service bash
```
```bash
$ python manage.py initialize_db
```

## Troubleshooting

### Initializing the database
If there are no migrations at the moment you could use the followig Flask command
```bash
$ flask init db stamp head
``` 