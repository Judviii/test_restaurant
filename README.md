# Library Service API

## Introduction
Performing a test task:
- A company needs an internal service for its employees to help them
to make a decision about choosing a place for lunch. Each restaurant will upload the menu daily via API to the system.
- Employees will vote for the menu before going out for lunch in the mobile application
for which you need to implement a backend. 
- There are users who have not updated the app to the latest version have not updated the application to the latest version, and the backend must support both
versions. The mobile app always sends the build version in the headers
## Installation

### Prerequisites
Before you can run this project, make sure you have the following installed:

- Python 3.11 or higher
- pip (Python package installer)
- Docker

### Running the API with Docker
```shell
    git clone https://github.com/Judviii/test_restaurant.git
    cd test_restaurant

    # create an .env file in the root directory of project, use env.sample as example.

    docker-compose build
    docker-compose up
```
- API will be available at http://127.0.0.1:8000/
- Swagger documentation will be available at http://127.0.0.1:8000/docs
- Run tests: `docker-compose run app sh -c "pytest"`;
- Run flake8: `docker-compose run app sh -c "flake8"`;
