# Base image of python
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Update and install dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y curl

# Install poppler-utils
RUN apt-get install -y poppler-utils

# Install pip packages
RUN pip install --upgrade pip