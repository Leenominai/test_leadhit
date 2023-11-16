import requests
import json
import logging


logging.basicConfig(level=logging.INFO)


base_url = "http://127.0.0.1:5000/get_form"


test_data = [
    {"user_email": "john.doe@example.com", "user_phone": "+7 123 456 78 90"},
    {"publication_date": "2022-01-15", "letter": "Some text"},
    {"user_phone": "+7 123 456 78 90", "user_email": "jane.smith@example.com"},
    {"user_email": "invalid_email", "user_phone": "+7 123 45"},
    {"date": "15.01.2022", "text": "Some text"},
    {"phone": "+1 (555) 123-4567", "email": "jane.smith@company.co"},
    {"custom_field": "Some text with !@#$%^&*()_+"},
    {"text_field": "A longer piece of text with multiple words"},
    {"html_field": "<p>This is a paragraph.</p><br><p>Another paragraph.</p>"}
]


for data in test_data:
    """
    Отправляет тестовые данные на сервер по заданному URL и анализирует ответ.

    :param test_data: Список словарей с тестовыми данными для отправки.
    :param base_url: URL-адрес сервера, куда отправляются тестовые данные.
    :return: None
    """
    logging.info(f"Входящие данные: {data}")
    response = requests.post(base_url, data=data)

    logging.info(f"Обработанные данные: {response.content}")

    if response.headers['Content-Type'] == 'application/json':
        try:
            result = response.json()
            logging.info(f"Окончательный вывод: {result}")
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка декодирования JSON-ответа: {e}")
    else:
        logging.error("Неподдерживаемый тип содержимого ответа. Ожидаемый: 'application/json'.")

    logging.info("\n" + "=" * 50 + "\n")
