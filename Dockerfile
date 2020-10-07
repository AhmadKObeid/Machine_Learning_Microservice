FROM python:3.6-slim

LABEL MAINTANER Your Name "ahmadkobeid96@gmail.com"

# We copy just the requirements.txt first to leverage Docker cache
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py","./model.sav"]