FROM python:3.9-slim as base
ARG FUNCTION_DIR="/home/app/"
WORKDIR ${FUNCTION_DIR}
RUN apt-get update && apt-get install -y \
  git wget unzip build-essential
COPY requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt


FROM base as tests
COPY requirements-dev.txt /home/app/requirements-dev.txt
RUN pip install -r requirements-dev.txt


FROM base as app
RUN pip install awslambdaric
# We build in github and this file isn't there.
# TODO: in the deployment sync this file first before building
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
COPY get_model.sh /home/app/get_model.sh
RUN /home/app/get_model.sh
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

COPY app/ /home/app/app
COPY config/ /home/app/config

