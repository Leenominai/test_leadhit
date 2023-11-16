import requests
import json
import logging


logging.basicConfig(level=logging.INFO)

base_url = "http://localhost:5000"


def test_form_request(form_data):
    url = f"{base_url}/get_form"
    response = requests.post(url, data=form_data)

    # Получаем ожидаемый ответ из тестовой базы
    with open("test_templates.json", "r") as file:
        templates = json.load(file)

    # Сравниваем ответ веб-приложения с ожидаемым ответом
    for template in templates:
        if set(form_data.keys()) == set(template.keys()):
            return template["name"]

    # # Если не найдено совпадений, типизируем поля на лету
    # return {field: type(form_data[field]) for field in form_data}

    # Если не найдено совпадений, типизируем поля на лету
    field_types = {field: type(form_data[field]) for field in form_data}

    # Проверяем, соответствуют ли типы полей требованиям какой-либо формы
    for template in templates:
        if all(
            isinstance(field_value, template.get(field, {}).get("type"))
            for field, field_value in field_types.items()
        ):
            return template["name"]

    # Если ни одна форма не соответствует требованиям
    return field_types


# Примеры тестовых данных
test_data = [
    # Валидные данные, совпадение с известной формой
    {"email": "john.doe@example.com", "phone": "+7 123 456 78 90"},
    {"date": "2022-01-15", "text": "Some text"},
    {"phone": "+7 123 456 78 90", "email": "jane.smith@example.com"},
    {"email": "invalid_email", "phone": "+7 123 45"},
    {"date": "15.01.2022", "text": "Some text"},
    {"phone": "+1 (555) 123-4567", "email": "jane.smith@company.co"},
    {"custom_field": "Some text with !@#$%^&*()_+"},
    {"text_field": "A longer piece of text with multiple words"},
    {"html_field": "<p>This is a paragraph.</p><br><p>Another paragraph.</p>"}
]

# Загрузка тестовой базы шаблонов форм из файла
for data in test_data:
    result = test_form_request(data)
    print(f"Входные данные: {data}")
    print(f"Выходные данные: {result}")
