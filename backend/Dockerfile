FROM python:3.11

RUN pip3 install --upgrade pip && pip3 install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Копируем все остальные файлы
COPY . .

RUN chmod +x test_requests.sh
ENTRYPOINT ["./test_requests.sh"]

# Команда для запуска приложения
CMD ["bash", "-c", "python app.py & ./test_requests.sh"]
