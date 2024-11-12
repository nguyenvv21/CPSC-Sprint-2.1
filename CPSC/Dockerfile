# start by pulling the python image
FROM python:3.8-alpine

COPY ./requirements.txt /requirements.txt
# Install build dependencies and runtime dependencies
WORKDIR /
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

# install the dependencies and packages in the requirements file
RUN python -m pip install --no-cache-dir --disable-pip-version-check --requirement /requirements.txt

# copy gunicorn config and application files
COPY . /

# Remove build dependencies to reduce image size
RUN apk del .tmp-build-deps

EXPOSE 5005

# configure the container to run gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
