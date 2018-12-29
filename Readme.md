# A stencil Flask based REST API template for Mongodb#
## Description ##
A simple implementation of CRUD for Mongodb using Flask and json API.
### Supported functions ###
* CREATE - Register user
* STORE - Store a record in the DB
* READ/GET - Get record from the DB
* DELETE - Delete record from the DB
## Prerequisites ##
* Python3
* Flask
* mongodb running either local (default localhost:27017) or mlab , etc.
* pymongo

## Running the server ##
```
> ./runme

```
## Testing API services ##
```
> ./test.py

## Stopping the server ##
Hit control-C to quit the server