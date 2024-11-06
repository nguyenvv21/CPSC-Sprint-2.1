# start by pulling the python image
FROM python:3.8-alpine

# set working directory
WORKDIR /app

# copy the requirements file into the Docker image
COPY requirements.txt /app/requirements.txt

# Install build dependencies and runtime dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

# install the dependencies and packages in the requirements file
RUN python -m pip install --no-cache-dir --disable-pip-version-check --requirement /app/requirements.txt

# copy gunicorn config and application files
COPY gunicorn-cfg.py /app/
COPY . /app/

# Remove build dependencies to reduce image size
RUN apk del .tmp-build-deps

EXPOSE 5005

# configure the container to run gunicorn
CMD ["gunicorn", "--config", "/app/gunicorn-cfg.py", "run:app"]