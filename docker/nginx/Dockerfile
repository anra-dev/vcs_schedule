FROM nginx

ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

COPY ./default.conf /etc/nginx/conf.d/default.conf