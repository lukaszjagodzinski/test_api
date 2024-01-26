# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /code
WORKDIR /code

# Copy only the Pipfile and Pipfile.lock to the container
COPY requirements.txt /code/

# Install Pipenv and project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Run collectstatic during the build process
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]