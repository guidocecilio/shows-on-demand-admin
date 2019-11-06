# FROM python:3.6.1

# # install environment dependencies
# RUN apt-get update -yqq \
#   && apt-get install -yqq --no-install-recommends \
#     netcat wget \
#   && apt-get -q clean

# # RUN yum install -y wget
# RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64
# RUN chmod +x /usr/local/bin/dumb-init

# ENV WORKDIR=/usr/app
# ENV PYTHON_USER=ossuser

# RUN groupadd -g 1001 ${PYTHON_USER} && useradd -r -m -u 1001 -g ${PYTHON_USER} ${PYTHON_USER}

# RUN mkdir ${WORKDIR}

# COPY . ${WORKDIR}/

# RUN chown -R ${PYTHON_USER}:${PYTHON_USER} ${WORKDIR}

# USER ${PYTHON_USER}

# # Unlikely to change often, so separate step not to invalidate docker step cache
# # COPY requirements.txt /
# RUN pip3.6 install --user -r ${WORKDIR}/requirements.txt

# WORKDIR ${WORKDIR}
# RUN python3.6 setup.py develop --user

# ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
# CMD ["sh", "-c", "/home/${PYTHON_USER}/.local/bin/gunicorn --config src/admin/gunicorn_hooks.py --workers 4 --worker-class gevent --preload --timeout 5 --bind 0.0.0.0:$PORT --access-logfile - --log-file - admin.wsgi:app"]

FROM python:3.6.1

# install environment dependencies
RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
    netcat \
  && apt-get -q clean

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
ADD . /usr/src/app

RUN python3.6 setup.py develop --user

# run server
CMD ["sh", "./entrypoint.sh"]