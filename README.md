## Jump To
- [Startup Instructions](#startup-instructions)
- [Future Ideas](#future-product-ideas)

## Objective 

Develop a web-app that uses weather data using Open Weather API that:
- showcases user centric design 
- showcases ability to work around technical challenges 

### Asumptions

#### Users
The consumer of this web-app can be one of the following:
- People (interact with frontend): 
    - internal consultant working on a deal (ex. tourism or agricultural)
    - someone from advanced analytics group
    - someone wanting to understand what weather data is available
- Other Apps (only backend): 
    - another application consuming our backend APIs for the weather data 

#### API

We are only allowed to use the two mentioned APIs + Geocoding API mentioned in the docs

#### Descoped for Assessment Purposes
- Authentication on endpoints 
- Creating a proper front-end design system / shared css mixins etc
- User log-in capability 
- Backend and frontend unit/integration testing
- Obervability considerations like logging

## Product
### User Stories
#### MVP Stories
- Search by City functionality
    - As a user, I would like to be presented with options to see the right city, to get acurrate data
    - As a user, I would like to search weather data by city, to view current weather, weather icon, lat and long of city
    - As a user, I would like to select multiple cities, to get bulk data
- Historic Weather info
    - As a user, I would like to see the historic weather data of my selected cities.
- Raw Json
    - As a user, I want to view the raw API output as JSON, to explore it
- Excel Download
    - As a user, I would like to download all my data in well named excel/csv sheet
- Data View
    - As a user I would like to search/filter and sort on different attributes
- API users
    - As another app, I would like to have clean documentation and error status codes
    - As another app, I would like to use an /health endpoint to ensure my service is up and running


### Future (Product) Ideas 
Future Ideas should be iterated on based on user signal and where we want to shape the product.
All of the descoped best practices should be worked on.

Small
- Implement endpoints to get historic and current weather only a single city to reduce number of API calls
- Show additional data like sunrise, sunset etc based on user needs
- Allow users to select fields they want as part of the excel
- Allow users to estimate and see the cost of the data (based on API costs)
- Use Google's autocomplete to help user find city vs. having multiple selection

Medium
- Store per-user preferences
- Have a notion of "saved filters / segments"
- Export data using other export formats 
- Deep link different search results for easy sharability
- Incorporate User Session data like click events etc (tools like Fullstory) for better iterations
- Show graphs / charts + Weather insights that are frequently needed.

Large
- Prewritten AI generated email summaries of data downlaoded / selected
- Show how and what data was used in other similar deals
- Use LangChain to give users ability to interact with and gain insight from excel data like chatgpt
- Show Weather insights and live trails
    - Decide if this is a data play or insights play or both

## Engineering 
### Tooling
For this project, we are using:
- [FastAPI](https://fastapi.tiangolo.com/) for our backend (Python)
- [Lit](https://lit.dev/) for our frontend (Typescript)
- [Docker](https://www.docker.com/products/docker-desktop/) for local set-up
- [AWS](https://aws.amazon.com/) Deploying using AWS Beanstalk and EC2 (Future State: Automated CI/CD pipeline)

### Startup Instructions
```sh
# If using docker, add your OpenWeather API Key in docker-compose.yaml
OPENWEATHER_API_KEY= # Add your API key
```
and then run

```sh
docker compose up

# NOTE: You may encounter a transient sqlalchemy error - 
 "sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "db" (172.25.0.2), port 5432 failed: Connection refused"
# To fix it, don't stop docker, just go to any file and hit save to reload the api server
```
FastAPI docs - navigate to `http://127.0.0.1:8000/docs`

PgAdmin - navigate to `http://localhost:5050/login?next=%2F`

```sh
# If not, start up postgres, and create a .env file in the root here to add your env vars:
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=weather_app_db
DB_PORT=5432
OPENWEATHER_API_KEY= # Add your API key 
```

and run
```sh
uvicorn app.main:app --reload --host 0.0.0.0
```

