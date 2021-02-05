# pull official base image
FROM python:3.8

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN python -m pip install --upgrade pip
COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# test requirements
CMD  gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
