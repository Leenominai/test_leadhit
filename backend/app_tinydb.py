import json
import re
import logging
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('templates_db.json')
templates_table = db.table('templates')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_templates_from_file(file_path):
    """
    Загружает шаблоны форм из JSON-файла.

    :param file_path: Путь к JSON-файлу с шаблонами форм.
    :return: Список словарей с шаблонами форм.
    """
    logger.info(f"Загрузка БД из файла с шаблонами форм: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            templates = json.load(file)
            logger.info(f"Загрузка БД из файла с шаблонами форм прошла успешно")
        return templates
    except FileNotFoundError:
        logger.error(f"Ошибка: Файл с шаблонами {file_path} не найден")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON-файла: {file_path}")
        return []


def insert_templates_into_db(templates):
    """
    Вставляет шаблоны форм в TinyDB, предварительно проверяя их отсутствие.

    :param templates: Список словарей с шаблонами форм.
    """
    for template in templates:
        # Проверка наличия данных в базе перед вставкой
        if not templates_table.contains(Query().name == template['name']):
            templates_table.insert(template)


test_templates = load_templates_from_file('test_templates.json')
insert_templates_into_db(test_templates)
logger.info(f"Полученная БД из файла: {test_templates}")


def validate_phone(phone):
    """
    Проверяет валидность формата телефонного номера.

    :param phone: Строка с телефонным номером.
    :return: True, если формат телефонного номера валиден, иначе False.
    """
    phone_pattern = re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$')
    return bool(re.match(phone_pattern, phone))


def validate_date(date):
    """
    Проверяет валидность формата даты.

    Поддерживаемые форматы: 'dd.mm.yyyy' и 'yyyy-mm-dd'.

    :param date: Строка с датой.
    :return: True, если формат даты валиден, иначе False.
    """
    date_pattern1 = re.compile(r'^\d{2}.\d{2}.\d{4}$')
    date_pattern2 = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(re.match(date_pattern1, date) or re.match(date_pattern2, date))


def validate_email(email):
    """
    Проверяет валидность формата электронной почты.

    :param email: Строка с адресом электронной почты.
    :return: True, если формат электронной почты валиден, иначе False.
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(re.match(email_pattern, email))


def validate(field_type, value):
    """
    Проверяет валидность значения в соответствии с указанным типом.

    :param field_type: Тип поля ('date', 'phone', 'email', 'text' и т.д.).
    :param value: Значение поля для проверки.
    :return: True, если значение валидно, иначе False.

    Примечания:
    Валидация текста -: всегда валиден.
    Неизвестный тип - считаем невалидным.
    """
    if field_type == "date":
        return validate_date(value)
    elif field_type == "phone":
        return validate_phone(value)
    elif field_type == "email":
        return validate_email(value)
    elif field_type == "text":
        return True
    else:
        return False


def typeify_fields(input_data):
    """
    Определяет типы полей входных данных.

    :param input_data: Словарь с входными данными.
    :return: Словарь, где ключи - имена полей, значения - их типы.
    """
    types_priority = ["date", "phone", "email", "text"]
    types = {}

    for field, value in input_data.items():
        for field_type in types_priority:
            if validate(field_type, value):
                types[field] = field_type
                break

    return types


def find_matching_template(field_types, templates):
    """
    Ищет шаблон, соответствующий заданным типам полей.

    :param field_types: Словарь с типами полей.
    :param templates: Список шаблонов для проверки.
    :return: Имя найденного шаблона или None, если подходящих шаблонов не найдено.
    """
    logger.info(f"Проверка шаблонов: данные для проверки: {field_types}")

    for template in templates:
        logger.info(f"Проверка шаблонов: проверяем шаблон {template}")

        form_fields = [
            (field, field_types[field])
            for field in field_types
        ]
        template_fields = [
            (field, template.get(field))
            for field in template
            if field != "name"
        ]

        logger.info(f"Проверка шаблонов: поля формы: {form_fields}")
        logger.info(f"Проверка шаблонов: поля шаблона: {template_fields}")

        if all(
            (field, field_type) in template_fields
            for field, field_type in form_fields
        ):
            logger.info(f"Проверка шаблонов: найден подходящий шаблон: {template['name']}")
            return template['name']

    logger.info(f"Проверка шаблонов: подходящих шаблонов не найдено")
    return None


@app.route('/get_form', methods=['POST'])
def get_form():
    """
    Обрабатывает POST-запрос, определяя соответствующий шаблон формы.

    :return: JSON-ответ с именем найденного шаблона или типами полей, если шаблон не найден.
    """
    input_data = request.form.to_dict()
    logger.info(f"Полученные данные: {input_data}")

    templates = db.table('templates')

    field_types = typeify_fields(input_data)
    logger.info(f"Переформатированные данные: {field_types}")

    matching_template = find_matching_template(field_types, templates)

    if matching_template:
        return jsonify(matching_template)
    else:
        return jsonify(field_types)


if __name__ == '__main__':
    app.run(debug=True)
