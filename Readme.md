# Some Api project

Some test api project with Django and DRF

## Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

    ```bash
    git clone git@github.com:lukaszjagodzinski/test_api.git
    cd test_api
    ```

2. Build the Docker image:

    ```bash
    docker-compose build
    ```

3. Run the Docker containers:

    ```bash
    docker-compose up
    ```

The application should now be accessible at [http://localhost:8000/](http://localhost:8000/).

## Running Tests

To run the tests, use the following command:

```bash
docker-compose run web make test