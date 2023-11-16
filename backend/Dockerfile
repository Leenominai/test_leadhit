FROM python:3.11

RUN pip3 install --upgrade pip && pip3 install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["python", "app.py"]
