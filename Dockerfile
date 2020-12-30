FROM ubuntu:latest

# provide setup-file
ARG setupfile=https://github.com/firemodels/fds/releases/download/FDS6.7.5/FDS6.7.5_SMV6.7.15_lnx.sh

# download FDS
ADD $setupfile /root/

# set environment variables
ENV FDSBINDIR=/root/FDS/FDS6/bin
ENV impihome=/root/FDS/FDS6/bin/INTEL
ENV PATH=$FDSBINDIR:$impihome/bin:$PATH
ENV FI_PROVIDER_PATH=$impihome/prov
ENV LD_LIBRARY_PATH=/usr/lib64:$impihome/lib:$LD_LIBRARY_PATH

# set execution rights, run setup script, remove setup script and unessential data
RUN chmod +x /root/*.sh && \
    /root/*.sh y && \
    rm /root/*.sh && \
    mv /root/FDS/FDS6/bin /root/FDS/ && \
    rm -rf /root/FDS/FDS6/* && \
    mv /root/FDS/bin /root/FDS/FDS6/

# set workdir for fds-simulation
WORKDIR /workdir


RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN apt-get -y update 
RUN apt-get -y install python3-pip
RUN apt-get -y install curl
RUN pip3 install --upgrade pip

RUN apt-get -y update
RUN apt-get -y install git
RUN pip3 install rasterio
RUN pip3 install numpy
ENV LANG en_US.utf8
RUN git clone https://github.com/tjschweitzer/geotif2fds.git
COPY FDS6.7.5_SMV6.7.15_lnx.sh ./

