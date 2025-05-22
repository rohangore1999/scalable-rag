# taking base image of python
FROM python:latest

# Install poppler-utils
RUN apt-get update
RUN apt-get install -y poppler-utils

# setting the working directory, and "cd" to it
WORKDIR /app

# copying the requirements.txt file to docker's root folder
COPY requirements.txt requirements.txt

# copying the app folder to docker's app(working dir) folder
COPY app/ /app/app/

# installing the dependencies
RUN pip install -r requirements.txt

# changing the shell to bash and running server
CMD ["/bin/sh", "-c", "python -m app.main"]

# to build docker file -> `docker build -t scalable-rag .`
# to debug docker file -> `docker run -it scalable-rag sh`
# to run docker file and map docker's port 8000 to host's port 8000 -> `docker run -it -p 8000:8000 scalable-rag`