import requests
import json
import logging


logging.basicConfig(level=logging.INFO)


base_url = "http://127.0.0.1:5000/get_form"


test_data = [
    # Валидные данные, совпадение с известной формой
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


# Загрузка тестовой базы шаблонов форм из файла
for data in test_data:
    logging.info(f"Testing data: {data}")
    response = requests.post(base_url, data=data)

    # Выводим содержимое ответа для дальнейшего анализа
    logging.info(f"Response content: {response.content}")

    # Проверяем, что ответ содержит корректный JSON
    if response.headers['Content-Type'] == 'application/json':
        try:
            result = response.json()
            logging.info(f"Result: {result}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response: {e}")
    else:
        logging.error("Unexpected response content type. Expected 'application/json'.")

    logging.info("\n" + "=" * 50 + "\n")
