FROM node:10-stretch-slim as client-builder

WORKDIR /app/frontend
COPY ./frontend/package.json /app/frontend
COPY ./frontend/yarn.lock /app/frontend
RUN yarn && yarn cache clean --force
COPY . /app
RUN yarn build_prod
WORKDIR /app

# Python build stage
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # for spaCy
  && apk add g++ gfortran \
  # for pdf2image
  && apk add poppler-utils \
  # microsoft fonts
  && apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f

RUN addgroup -S django \
    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

# Install Spacy Models
# RUN python -m spacy download en_core_web_lg

# Install NLTK corpus
# RUN python -m nltk.downloader words brown

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start
COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower
COPY --from=client-builder /app /app


RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
