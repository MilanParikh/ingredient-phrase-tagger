FROM ubuntu:16.04
LABEL maintainer="Michael Lynch <michael@mtlynch.io>"

ARG BUILD_DATE
ENV VCS_URL https://github.com/mtlynch/ingredient-phrase-tagger.git
ARG VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="$VCS_URL" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.schema-version="1.0.0-rc1"

ADD . ingredient-phrase-tagger

ARG CRFPP_REPO=https://github.com/mtlynch/crfpp.git

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y build-essential git python2.7 python-pip

RUN git clone "$CRFPP_REPO" && \
    cd crfpp && \
    ./configure && \
    make && \
    make install && \
    echo "/usr/local/lib" > /etc/ld.so.conf.d/local.conf && \
    ldconfig && \
    cd ..

RUN cd ingredient-phrase-tagger && \
    python setup.py install && \
    cd ..

# Clean up.
RUN rm -rf /var/lib/apt/lists/* && \
    rm -Rf /usr/share/doc && \
    rm -Rf /usr/share/man && \
    apt-get autoremove -y && \
    apt-get clean

WORKDIR /app
