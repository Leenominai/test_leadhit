import re
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Настройка логгера
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define validation functions for phone, date, and email
def validate_phone(phone):
    phone_pattern = re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$')
    return bool(re.match(phone_pattern, phone))


def validate_date(date):
    date_pattern1 = re.compile(r'^\d{2}.\d{2}.\d{4}$')
    date_pattern2 = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(re.match(date_pattern1, date) or re.match(date_pattern2, date))


def validate_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(re.match(email_pattern, email))


def validate(field_type, value):
    if field_type == "date":
        return validate_date(value)
    elif field_type == "phone":
        return validate_phone(value)
    elif field_type == "email":
        return validate_email(value)
    # Добавьте другие типы по мере необходимости
    elif field_type == "text":
        # Валидация текста (пример: всегда валиден)
        return True
    else:
        # Неизвестный тип, считаем невалидным
        return False


def typeify_fields(input_data):
    types_priority = ["date", "phone", "email", "text"]
    types = {}

    for field, value in input_data.items():
        for field_type in types_priority:
            if validate(field_type, value):
                types[field] = field_type
                break

    return types


@app.route('/get_form', methods=['POST'])
def get_form():
    # Логирование полученных данных
    input_data = request.form.to_dict()
    logger.info(f"Received input data: {input_data}")

    # Логирование типизации полей
    field_types = typeify_fields(input_data)
    logger.info(f"Field types: {field_types}")

    return jsonify(field_types)


if __name__ == '__main__':
    app.run(debug=True)
