FROM centos:7

RUN yum update -y && \
    yum install -y python-setuptools \
        rpm-build \
        git

RUN git clone https://github.com/EUDAT-B2SAFE/B2HANDLE.git /opt/B2HANDLE

WORKDIR /opt/B2HANDLE
ADD build.sh /opt/B2HANDLE/build.sh

CMD /opt/B2HANDLE/build.sh


