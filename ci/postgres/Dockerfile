FROM ubuntu:16.04

# basic system
RUN apt-get update &&\
    apt-get install -y \
    lsb-release \
    sudo \
    wget \
    less \
    patch \
    apt-transport-https \
    dnsutils \
    python-software-properties software-properties-common \
    postgresql postgresql-client postgresql-contrib \
    odbc-postgresql \
    emacs

# postgres
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker &&\
    psql --command "CREATE USER irods WITH PASSWORD 'test';" &&\
    psql --command 'CREATE DATABASE "ICAT";' &&\
    psql --command 'GRANT ALL PRIVILEGES ON DATABASE "ICAT" TO irods;'
USER root
RUN mkdir /app
RUN echo '#!/bin/bash' > /app/run_postgres.sh && \
    echo 'service postgresql start' >> /app/run_postgres.sh && \
    echo '/usr/lib/postgresql/9.5/bin/pg_isready' >> /app/run_postgres.sh && \
    echo 'tail -f /var/log/postgresql/postgresql-9.5-main.log' >> /app/run_postgres.sh && \
    chmod a+x /app/run_postgres.sh
EXPOSE 5432

CMD ["/app/run_postgres.sh"]



