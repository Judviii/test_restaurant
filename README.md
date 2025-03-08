# Restaurant Menu Voting API

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
- API will be available at http://127.0.0.1:8001/
- Swagger documentation will be available at http://127.0.0.1:8001/docs
- Run tests: `docker-compose run app sh -c "pytest"`;
- Run flake8: `docker-compose run app sh -c "flake8"`;
## Notes on Implementation
- The API supports multiple client app versions (1.0 and 2.0) via middleware that checks the `App-Version` header. Currently, the logic is identical for all versions, but the structure allows for easy extension to add version-specific behavior if needed.
- **Important Note**: After the time was up, I realized that I hadn't implemented separate access for restaurants to upload menus. If I had more time, I would have reworked the `Employee` (User) model by adding the roles `restaurant_employee` and `company_employee` or `admin`|`user`, where the first role would allow menu uploads and the second role would allow voting. I am not making these changes to comply with the rules, but I am willing to discuss this solution.
