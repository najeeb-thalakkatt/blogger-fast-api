# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/blog

# Copy the current directory contents into the container at /usr/src/app
COPY ./blog /usr/src/blog

# Install any needed packages specified in requirements.txt
COPY ./blog/requirements.txt /usr/src/blog/
RUN pip install --no-cache-dir -r requirements.txt

# Copy alembic.ini to the working directory
COPY ./blog/alembic.ini /usr/src/blog/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME=blog.main

# Run the application
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--reload"]
