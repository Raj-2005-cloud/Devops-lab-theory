# Dockerfile Creation, Image Automation, and Docker Hub Sharing (Java Application)

## Objective

To create a Dockerfile for a Java application using Ubuntu 22.04, automate the creation of a Docker image using the Dockerfile, and share the image on Docker Hub.

---

## Tools and Technologies

- Docker
- Ubuntu 22.04
- OpenJDK 17
- Java
- Docker Hub

---

## Experiment Description

This experiment demonstrates the use of Docker to containerize a Java application. A Dockerfile is created to define the application environment, install required dependencies, compile the Java source code, and execute the application inside a container. The Docker image is built automatically using the Dockerfile and then shared through Docker Hub for portability and reuse.

---

## Dockerfile

```dockerfile
FROM ubuntu:22.04

RUN apt update && apt install -y openjdk-17-jdk

WORKDIR /home/app

COPY Hello.java .

RUN javac Hello.java

CMD ["java", "Hello"]
```

## Docker Hub Image Sharing

After successful image creation, the Docker image is tagged and pushed to Docker Hub. Storing the image on Docker Hub allows it to be accessed, shared, and deployed across different systems using Docker, supporting collaborative development and DevOps workflows.

## Workflow and Screenshots:

- #### Docker Image Build Process

  ![Build Java App](Screenshots\Screenshot 2026-02-06 124122.png)

- #### Java Application Running in Container

  ![Running](Screenshots/Screenshot 2026-02-06 124617.png)
  ![Running](Screenshots/Screenshot 2026-02-06 125121.png)
  ![Running](Screenshots/Screenshot 2026-02-06 130443.png)

- #### Docker Image Published on Docker Hub

![Running](Screenshots/Screenshot 2026-02-06 130518.png)
