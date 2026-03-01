# Docker Configuration

This document provides information about setting up and using Docker for this project.

## Prerequisites

- Ensure you have Docker installed on your machine. You can download it from [Docker's official site](https://www.docker.com/products/docker-desktop).

## Building the Docker Image

To build the Docker image for the FastAPI application, navigate to the root of the project directory and run:

```sh
docker build -t my-fastapi-app .
```

Replace `my-fastapi-app` with your desired image name.

## Running the Docker Container

After building the Docker image, you can run the container with:

```sh
docker run -p 8000:8000 my-fastapi-app
```

- The `-p 8000:8000` flag maps port 8000 of the Docker container to port 8000 of the host machine, allowing the FastAPI app to be accessed via `http://localhost:8000`.

## Stopping the Docker Container

Find the container ID with:

```sh
docker ps
```

Stop the running container using:

```sh
docker stop <container_id>
```

## Accessing the Application

Once the Docker container is running, the FastAPI application is accessible at `http://localhost:8000`. You can access the automatically generated API documentation at `http://localhost:8000/docs`.

## Common Docker Commands

- **List all images**: `docker images`
- **Remove an image**: `docker rmi <image_id>`
- **List all running containers**: `docker ps`
- **List all containers (including stopped)**: `docker ps -a`
- **Remove a container**: `docker rm <container_id>`

## Troubleshooting

- **Docker Daemon Issues**: Ensure Docker Daemon is running. This is often the root cause of issues when running Docker commands.
- **Port Conflicts**: Ensure the chosen port is not in use by other applications.

## Further Reading

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
