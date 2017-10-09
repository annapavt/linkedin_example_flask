FROM python:2.7-slim
MAINTAINER Anna Bankirer <anna.bankirer@aidoc.com>

ENV INSTALL_PATH /linkedin
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000


CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "linkedin.app:create_app()"
