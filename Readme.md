# Django Project with Docker

This repository contains a Django social Medeia app that uses Docker to manage local and production environments. It provides Docker Compose files for both development and production setups.

<video width="320" height="240" controls>
  <source src="./screenshots/threats .mp4" type="video/mp4">
</video>

## Table of Contents

- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Production Setup](#production-setup)
- [Environment Variables](#environment-variables)
- [Additional Configuration](#additional-configuration)
  - [Static and Media Files](#static-and-media-files)
  - [Reverse Proxy with Nginx](#reverse-proxy-with-nginx)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Conclusion](#conclusion)

## Project Setup

### Prerequisites

Before setting up the project, make sure you have the following installed:

- Docker (and Docker Compose if it's not bundled with Docker)
- Git
- Python (optional, but useful for testing outside Docker)

Clone the repository to your local machine:

```sh
git clone https://github.com/jck-bit/Threats.git
```

### Local Development Setup

This setup uses Docker Compose to run the application with all the required services in containers (PostgreSQL for the database and Django for the web application). Here’s how to get started.

#### 1. Build and Start the Containers

Make sure you're in the project directory where `docker-compose.yml` is located. Then, run the following command to start the services for local development:

```sh
docker-compose up --build
```

move to the project directory

```sh
 cd Threats
```

This will:

- Build the Docker images for your application.
- Start the Django app and PostgreSQL database.
- Expose the app on `http://localhost:8000` by default.

#### 2. Run Migrations

Once the containers are running, run Django migrations to set up the database:

```sh
docker-compose exec web python manage.py migrate
```

#### 3. Access the App

Open your browser and visit `http://localhost:8000` to see your Django application running locally.

#### 4. Optional: Creating a Superuser

If you need to create a superuser for Django's admin interface, run the following command:

```sh
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create the superuser account, then log in at `http://localhost:8000/admin`.

### Production Setup

For production, we use a separate `docker-compose-deploy.yml` file. This setup uses Nginx as a reverse proxy and separates the app, database, and static files. The following steps will guide you through deploying the app.

#### 1. Prepare the Environment Variables

Create a `.env` file or set the environment variables in your terminal for production, for example:

```env
DB_NAME=mydb
DB_USER=myuser
DB_PASS=mypassword
SECRET_KEY=mysecretkey
ALLOWED_HOSTS=yourdomain.com
```

Make sure these values are consistent between the local and production environments.

#### 2. Deploy the Containers

To deploy the project using Docker Compose, run the following:

```sh
docker-compose -f docker-compose-deploy.yml up --build -d
```

This will:

- Build the images for the app, database, and proxy.
- Start the services in detached mode.
- Expose the app via port 80 through Nginx.

#### 3. Run Migrations for Production

Once the app is running in production, make sure to run migrations:

```sh
docker-compose -f docker-compose-deploy.yml exec app python manage.py migrate
```

#### 4. Access the App

After deployment, the app will be accessible via the domain you set in `ALLOWED_HOSTS`. You can now visit your app through `http://yourdomain.com`.

## Environment Variables

The project uses the following environment variables for both development and production environments. You can define them in `.env` files or directly in your `docker-compose.yml` files.

| Variable             | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| `DB_NAME`            | The name of the PostgreSQL database.                                |
| `DB_USER`            | The PostgreSQL username.                                            |
| `DB_PASS`            | The PostgreSQL password.                                            |
| `SECRET_KEY`         | A secret key for Django (make sure it's unique).                    |
| `ALLOWED_HOSTS`      | Comma-separated list of allowed hosts (e.g., localhost, 127.0.0.1). |
| `POSTGRES_COLLATION` | PostgreSQL collation setting (default is `en_US.UTF-8`).            |

## Additional Configuration

### Static and Media Files

Both development and production setups handle static files and media files differently.

- **Development**: The `docker-compose.yml` configuration serves static files through Django's built-in development server.
- **Production**: The `docker-compose-deploy.yml` setup uses Nginx to serve static files from the `/vol/static` volume, which is built by Django's `collectstatic` command.

To collect static files in production:

```sh
docker-compose -f docker-compose-deploy.yml exec app python manage.py collectstatic
```

This will collect static files and store them in the appropriate volume, which is mounted by the Nginx service for serving.

### Reverse Proxy with Nginx

In production, Nginx acts as a reverse proxy in front of the Django application. The proxy is set up in the `docker-compose-deploy.yml` file.

- Nginx listens on port 80 and forwards requests to the Django application, which runs on port 8000 inside the container.
- The proxy ensures that traffic is properly routed and also serves static files.

If you make any changes to the Nginx configuration, make sure to rebuild the proxy service:

```sh
docker-compose -f docker-compose-deploy.yml up --build proxy
```

## Running Tests

To run tests inside the Docker container, use the following command:

```sh
docker-compose exec web python manage.py test
```

This will execute your Django tests inside the app container.

## Troubleshooting

### Common Issues

- **Database Connection Error**:

  - Ensure that the `DB_HOST` in `settings.py` is set to the correct value (`db` in Docker Compose).
  - Ensure that the `db` service is running and healthy.

- **Static Files Not Serving**:

  - Make sure you’ve run `python manage.py collectstatic` in production to collect static files.
  - In development, ensure that `DEBUG=True` in your `settings.py` to serve static files via Django.

- **Port Already in Use**:
  - If port 8000 or port 80 is already being used by another service, you can change the exposed ports in `docker-compose.yml` or `docker-compose-deploy.yml`.

## Conclusion

This project uses Docker Compose to set up a local development environment and a production-ready environment for your Django app. You can easily switch between local development and production deployment by using the appropriate `docker-compose.yml` file.

Let me know if you need any further clarifications or run into any issues.