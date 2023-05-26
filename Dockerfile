FROM python:3.11.3-slim-buster

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

FROM base as dev

# Install necessary soft
RUN apt-get update \
    && apt-get install -y netcat curl git make gcc postgresql python3-dev libpq-dev \
    && apt-get clean

ENV DEVELOPMENT=1

# Copy & install dependencies
COPY ./requirements ./requirements
RUN pip install -r ./requirements/dev.txt

COPY . .

CMD ["bash", "scripts/run.sh"]
