# backend

Main backend app

## default.env

default configurations to be put in .env locally

before running webapp itself don't forget to start docker-compose with the database!

```bash
docker-compose up -d
```

if you want to recreate database for some reason, do this using docker-compose too

```bash
sudo docker-compose down -t1 --volumes
```

Then repeat first command.

To create db run "create db" from vscode debug;

To populate it run "initiate db";

To run application run "webapp";

## Contributing

- `make lint`
- `make test`
