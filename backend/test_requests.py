import requests

# URL вашего приложения
base_url = "http://localhost:5000"


# Пример тестового запроса с данными формы
def test_form_request():
    url = f"{base_url}/get_form"

    # Данные формы в виде словаря
    form_data = {
        "f_name1": "john.doe@example.com",
        "f_name2": "+7 123 456 78 90"
        # Добавьте другие поля формы по мере необходимости
    }

    # Отправка POST-запроса с данными формы
    response = requests.post(url, data=form_data)

    # Вывод результата запроса
    print(f"Response Status Code: {response.status_code}")
    print("Response Content:")
    print(response.text)


# Вызываем функцию для выполнения тестового запроса
test_form_request()
