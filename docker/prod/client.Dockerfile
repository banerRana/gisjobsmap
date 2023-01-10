# base image
FROM node:12.2.0-alpine as build

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY . /usr/src/app/
# COPY package.json /usr/src/app/package.json
# COPY package-lock.json /usr/src/app/package-lock.json

RUN npm config set unsafe-perm true
RUN npm install
RUN npm install react-scripts@3.2.0 -g
RUN npm run build


# production environment
FROM nginx:1.23.3-alpine

COPY --from=build /usr/src/app/build /etc/nginx/html