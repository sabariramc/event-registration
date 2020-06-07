# EVENT REGISTRATION #

Event registration is a web app for management registering for events.

### Pre-requisite ###

The app is build with
- Python 3.8
- React
- Mysql 8.0

### Set up instructions ###

- Create python virtual environment and activate it
- Install `requirement.txt`
- Install `mysql-server 8.0` and run it
- Create a user in `mysql server` and execute the script at `dbmodel/db_file.sql`
- Update the mysql connection configuration in `.env`
- Update media folder path in the `.env`
- Go to `client` folder 
    - run `npm install`
    - run `npm build`
- Run either `startserver.py` or `runflask.sh`, flask server will run at `localhost:8888`
- `http://localhost:8888` will show you a default react app page
- `http://localhost:8888/event/api` is the base url for Restful APIs
- `GET http://localhost:8888/event/api/registration` will lise the registration
- `GET http://localhost:8888/event/api/registration/<reg_id>` will get data of a single registration
- `POST http://localhost:8888/event/api/registration` will create a registration
    * Content-Type : `multipart/form-data`
    * Form Fields:
        + full_name 
        + id_card - id_card image file
        + mobile_number
        + email_address
        + registration_type - Allowed values [SELF, GROUP, CORPORATE, OTHERS]
        + no_of_ticket
        