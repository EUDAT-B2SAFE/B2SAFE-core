FROM centos:7

RUN yum update -y && \
    yum install -y \
    rsync wget less emacs make cmake gcc gcc-c++

RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    rpm --import https://packages.irods.org/irods-signing-key.asc && \
    wget -qO - https://packages.irods.org/renci-irods.yum.repo | \
    tee /etc/yum.repos.d/renci-irods.yum.repo

RUN yum install -y \
    sudo \
    which \
    python-jsonschema \
    python-psutil \
    python-pytest \
    python-requests \
    python-pip \
    python-behave \
    python-devel  \
    openssl-devel \
    fuse-libs \
    lsof \
    openssl \
    perl-JSON \
    authd \
    postgresql \
    postgresql-odbc\
    unixODBC \
    boost-devel \
    libcurl-devel \
    supervisor \
    rpm-build \
    rpm-devel \
    rpmlint \
    rpmdevtools \
    coreutils \
    diffutils \
    patch

COPY ci/app/odbcinst.ini /etc/odbcinst.ini

################################################################################
#
# irods
#
################################################################################
RUN yum install -y irods-externals-boost1.60.0-0-1.0-1 \
                   irods-externals-avro1.7.7-0 \
                   irods-externals-clang-runtime3.8-0 \
                   irods-externals-clang3.8-0 \
                   irods-externals-cmake3.5.2-0 \
                   irods-externals-cppzmq4.1-0 \
                   irods-externals-epm4.2-0 irods-externals-imagemagick7.0.3-0 \
                   irods-externals-jansson2.7-0 \
                   irods-externals-json3.0.1-0 \
                   irods-externals-libarchive3.1.2-0 \
                   irods-externals-libarchive3.3.2-0 \
                   irods-externals-qpid-with-proton0.34-0 \
                   irods-externals-redis4.0.8-0 \
                   irods-externals-zeromq4-14.1.3-0 \
                   irods-devel irods-externals-autoconf5ad3567c-0 \
                   irods-externals-libs3a30e55e8-0-1.0-1 \
                   irods-server-4.2.6 \
                   irods-database-plugin-postgres-4.2.6 \
                   irods-icommands%VERSION-4.2.6 \
                   irods-rule-engine-plugin-audit-amqp-4.2.6 \
                   irods-rule-engine-plugin-python-4.2.6 \
                   irods-runtime-4.2.6 \
                   irods-server-4.2.6 && \
                   pip install --upgrade pip && \
                   pip install python-irodsclient flask flask_restful pytest

################################################################################
#
# irods setup preparation
#
################################################################################
RUN useradd -rm -d /var/lib/irods irods
RUN mkdir -m 777 /src
# setup script from previous version
ADD ci/app/4.2/setup_answers.txt /app/setup_answers.txt
ADD ci/app/4.2/setup_irods.sh /app/setup_irods.sh
ADD ci/app/4.2/restart_irods.sh /app/restart_irods.sh
ADD ci/app/4.2/surfsara-irods.repo /etc/yum.repos.d/surfsara-irods.repo
ADD ci/app/irods_environment.json /root/.irods/irods_environment.json
ADD ci/app/sleep.sh /app/sleep.sh
ADD ci/app/wait_for_pg.sh /app/wait_for_pg.sh
ADD ci/app/create_rpm.sh /app/create_rpm.sh
ADD ci/app/update_install.py /app/update_install.py
ADD scripts/tests/requirements.txt /app/test-requirements.txt

RUN pip install -r /app/test-requirements.txt
RUN yum install -y msi-persistent-id.x86_64

# install B2HANDLE
RUN pip install b2handle

CMD ["/app/setup_irods.sh"]
