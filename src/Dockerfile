FROM python:3.10.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt install -y netcat=1.10-46 \
  && pip install --upgrade pip \
  && pip install poetry==1.2.2

COPY ./src/pyproject.toml ./src/poetry.lock ./

ARG DEV_DEPS=False

RUN poetry config virtualenvs.create false
RUN if [ $DEV_DEPS = True ] ; then \
  poetry install --no-interaction --no-ansi ; else \
  poetry install --no-dev --no-interaction --no-ansi ; fi

COPY . .

RUN chmod 777 /usr/src/app/src/entrypoint.sh
ENTRYPOINT ["/usr/src/app/src/entrypoint.sh"]