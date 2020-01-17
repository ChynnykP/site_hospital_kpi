FROM python:3.7.1

LABEL Author="Chynnyk Petro"
LABEL E-mail="chynnyk@vivaldi.net"
LABEL version="0.0.1b"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "application.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

COPY . /app/

# RUN pip install --upgrade pip && \
#     pip install pipenv && \
#     pipenv install --dev --system --deploy --ignore-pipfile

# ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0