FROM node:10-stretch-slim

WORKDIR /app

COPY ./frontend/package.json /app
COPY ./frontend/yarn.lock /app

RUN yarn && yarn cache clean --force

ENV PATH ./node_modules/.bin/:$PATH
