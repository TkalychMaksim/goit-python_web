
FROM python:3.10


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app


COPY Pipfile Pipfile.lock ./


RUN pipenv install --deploy --system


COPY . .


CMD ["pipenv", "run", "python", "bot.py"]
