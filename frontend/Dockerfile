FROM node:lts-alpine

# install simple http server for serving static content
RUN npm install -g http-server

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY min-example/ /usr/src/app

RUN npm install
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]

#CMD [ "npm" "run" "dev"]
#EXPOSE 5173