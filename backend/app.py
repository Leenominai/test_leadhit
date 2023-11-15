import os
import re
import sys

from flask import Flask, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)

# Подключение к MongoDB
try:
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client.forms
    templates_collection = db.templates
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)


def validate_phone(phone):
    # Валидация телефона: формат +7 xxx xxx xx xx
    phone_pattern = re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$')
    return bool(re.match(phone_pattern, phone))


def validate_date(date):
    # Валидация даты: формат DD.MM.YYYY или YYYY-MM-DD
    date_pattern1 = re.compile(r'^\d{2}.\d{2}.\d{4}$')
    date_pattern2 = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(re.match(date_pattern1, date) or re.match(date_pattern2, date))


def validate_email(email):
    # Валидация email
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(re.match(email_pattern, email))


def process_form_data(data):
    processed_data = {}
    errors = {}

    for key, value in data.items():
        if key == "phone" and not validate_phone(value):
            errors[key] = "Invalid phone format"
        elif key == "date" and not validate_date(value):
            errors[key] = "Invalid date format"
        elif key == "email" and not validate_email(value):
            errors[key] = "Invalid email format"
        else:
            processed_data[key] = value

    return processed_data, errors


def get_form_name(form_data):
    for template in templates_collection.find():
        template_fields = set(template.keys()) - {"_id", "name"}
        form_fields = set(form_data.keys())
        if template_fields.issubset(form_fields):
            matching_fields = [field for field in template_fields if template[field] == form_data[field]]
            if set(matching_fields) == template_fields:
                return template["name"]

    # Если подходящей формы не найдено, типизируем поля на лету
    field_types = {
        field: "date" if validate_date(form_data[field]) else
               "phone" if validate_phone(form_data[field]) else
               "email" if validate_email(form_data[field]) else
               "text"
        for field in form_data
    }

    return field_types


@app.route('/get_form', methods=['POST'])
def get_form():
    try:
        form_data, errors = process_form_data(request.form.to_dict())
        if errors:
            return jsonify({"error": "Invalid form fields", "errors": errors}), 400

        result = get_form_name(form_data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
