FROM staphb/abricate:1.0.1-insaflu-220727
# https://github.com/StaPH-B/docker-builds/tree/master/abricate
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&\
    apt-get -y --no-install-recommends install software-properties-common curl &&\
    add-apt-repository ppa:deadsnakes/ppa -y &&\
    apt-get -y --no-install-recommends install python3.10 python3.10-venv &&\
    apt-get clean

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

ENV VIRTUAL_ENV=/opt/abri_annotate_venv
RUN python3.10 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U fire pandas biopython==1.79

# install vibr_annotate
RUN pip install git+https://github.com/MrTomRod/abri-annotate

WORKDIR /data
