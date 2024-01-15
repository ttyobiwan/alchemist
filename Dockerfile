FROM python:3.11.3-slim-buster as base

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

# Install necessary soft
RUN apt-get update \
    && apt-get install -y netcat curl git make gcc postgresql python3-dev libpq-dev \
    && apt-get clean

FROM base as dev

ENV DEVELOPMENT=1

# Copy & install dependencies
COPY ./requirements ./requirements
RUN pip install -r ./requirements/dev.txt

COPY . .

CMD ["bash", "scripts/run.sh"]
