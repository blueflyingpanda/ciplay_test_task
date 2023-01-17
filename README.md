# Test task CIPLAY

## Quick start
Start database in Docker container
```
docker run --name ciplay_db -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
docker cp sql_scripts/create_db.sql ciplay_db:/docker-entrypoint-initdb.d/create_db.sql
docker cp sql_scripts/procedures.sql ciplay_db:/docker-entrypoint-initdb.d/procedures.sql
docker exec -u postgres ciplay_db psql postgres postgres -f docker-entrypoint-initdb.d/create_db.sql
docker exec -u postgres ciplay_db psql postgres postgres -f docker-entrypoint-initdb.d/procedures.sql
```
Start API in Docker container
```
make start
```
---
## Usage

After starting the project (see Quick start section) you can access endpoints documentation by visiting

http://**host**:**port**/docs  (Example http://127.0.0.1:8000/docs)

Alternatively you can look at endpoint examples at **endpoints.http**

---
## Configurations

All the configurations for RestAPI are stored in rest.ini