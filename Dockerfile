FROM tiangolo/uwsgi-nginx:python3.7

ARG release
ENV RELEASE=$release

RUN yes | pip install --no-cache-dir pipenv
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN apt-get update && apt-get install -y gcc libpq-dev musl-dev gettext

RUN pipenv install --system --deploy

# Setting up app and custom configurations
COPY . /app/

RUN mkdir static && mkdir media

VOLUME /app/static
VOLUME /app/media

COPY .docker/uwsgi.ini /app

HEALTHCHECK --interval=1m --timeout=3s \
    CMD curl -H 'X-HealthCheck: check' -f "http://localhost/" || exit 1
