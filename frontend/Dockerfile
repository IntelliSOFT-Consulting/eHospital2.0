# syntax=docker/dockerfile:1.3
#--------------------------------------------
# Dev Stage - Assembles and Builds Frontend
#--------------------------------------------
FROM --platform=$BUILDPLATFORM node:lts-alpine as dev

ARG APP_SHELL_VERSION=next

RUN mkdir -p /app
WORKDIR /app

COPY spa-assemble-config.json .
COPY spa-build-config.json .
COPY /assets /app/assets

ARG CACHE_BUST
RUN npm install -g npm@11.0.0
RUN npx --legacy-peer-deps openmrs@${APP_SHELL_VERSION:-next} assemble --manifest --mode config --config spa-assemble-config.json --target ./spa
RUN npx --legacy-peer-deps openmrs@${APP_SHELL_VERSION:-next} build --build-config spa-build-config.json --target ./spa

# Copy the required files and echo
RUN echo "Copying required files ..." && \
    cp ./assets/ehospitallogo.jpg ./spa && \
    cp ./assets/ehospitallogo.png ./spa && \
    cp ./assets/primary-navigation.jpg ./spa && \
    cp spa-build-config.json ./spa

RUN if [ ! -f ./spa/index.html ]; then echo 'Build failed. Please check the logs above for details. This may have happened because of an update to a library that OpenMRS depends on.'; exit 1; fi

# Modify page title
RUN sed -i 's/<title>.*<\/title>/<title>eHospital<\/title>/' ./spa/index.html

#--------------------------------------------
# Runtime Stage - Published Image
#--------------------------------------------
FROM nginx:1.25-alpine

RUN apk update && \
    apk upgrade && \
    # add more utils for sponge and envsubst
    apk add --no-cache moreutils

# clear any default files installed by nginx
RUN rm -rf /usr/share/nginx/html/*

COPY startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=dev /app/spa /usr/share/nginx/html
COPY config.json /usr/share/nginx/html

CMD ["/usr/local/bin/startup.sh"]
