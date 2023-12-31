# Web-приложение для определения заполненных форм

## Описание ТЗ

Перед получением информации о выполненном проекте предлагаю ознакомиться с подробной информацией о целях проекта:

<details>
  <summary>Открыть</summary>

### Описание задания:

В базе данных хранится список шаблонов форм.

Шаблон формы, это структура, которая задается уникальным набором полей, с указанием их типов.

Пример шаблона формы:

```
{
    "name": "Form template name",
    "field_name_1": "email",
    "field_name_2": "phone"
}
```
Всего должно поддерживаться четыре типа данных полей:
1. email
2. телефон
3. дата
4. текст

Все типы кроме текста должны поддерживать валидацию. Телефон передается в стандартном формате +7 xxx xxx xx xx, дата передается в формате DD.MM.YYYY или YYYY-MM-DD.

Имя шаблона формы задается в свободной форме, например MyForm или Order Form.
Имена полей также задаются в свободной форме (желательно осмысленно), например user_name, order_date или lead_email.

На вход по урлу /get_form POST запросом передаются данные такого вида:
f_name1=value1&f_name2=value2

В ответ нужно вернуть имя шаблона формы, если она была найдена.
Чтобы найти подходящий шаблон, нужно выбрать тот, поля которого совпали с полями в присланной форме. Совпадающими считаются поля, у которых совпали имя и тип значения. Полей в пришедшей форме может быть больше чем в шаблоне, в этом случае шаблон все равно будет считаться подходящим. Самое главное, чтобы все поля шаблона присутствовали в форме.

Если подходящей формы не нашлось, вернуть ответ в следующем формате:

```
{
    f_name1: FIELD_TYPE,
    f_name2: FIELD_TYPE
}
```
Где FIELD_TYPE это тип поля, выбранный на основе правил валидации, проверка правил должна производиться в следующем порядке дата, телефон, email, текст.

В качестве базы данных рекомендуем использовать tinyDB, вместе с исходниками задания должен поставляться файл с тестовой базой, содержащей шаблоны форм. Но если сможете поднять и использовать контейнер Docker с MongoDB - это будет отличное решение, однако оно может отнять у вас много времени и не является обязательным.

Также в комплекте должен быть скрипт, который совершает тестовые запросы. Если окружение приложения подразумевает что-то выходящее за рамки virtualenv, то все должно быть упаковано в Docker контейнеры или таким способом, чтобы не приходилось ставить дополнительные пакеты и утилиты на машине. Все необходимые действия для настройки и запуска приложения должны находится в файле README.

Версия Python остается на ваш выбор. Мы рекомендуем использовать версию 3.6 и выше.

### Входные данные для веб-приложения:

Список полей со значениями в теле POST запроса.

### Выходные данные:

Имя наиболее подходящей данному списку полей формы, при отсутствии совпадений с известными формами произвести типизацию полей на лету и вернуть список полей с их типами.

</details>

## О выполненном проекте FormInspector

Этот проект представляет собой веб-приложение, созданное для эффективного анализа и определения заполненных форм. Проект построен на Flask и MongoDB, предоставляя удобный интерфейс для обработки данных, сопоставления с шаблонами и динамической типизации.

### Важными особенностями проекта являются:

- **MongoDB для хранения данных**: Проект использует MongoDB для эффективного хранения и извлечения данных, обеспечивая быстрый доступ к шаблонам форм.

- **Динамическая типизация**: В случае отсутствия совпадений с известными формами, приложение осуществляет динамическую типизацию полей, предоставляя пользователю актуальные и точные данные.

- **Легкость интеграции с MongoDB**: Пользователи могут легко интегрировать проект с существующими базами данных MongoDB, что делает его гибким и настраиваемым.

- **Логгирование для отслеживания действий**: FormCraftsman внедряет четкое логгирование, которое фиксирует ключевые действия приложения, обеспечивая прозрачность и отслеживание работы системы.

- **Автоматизация с pre-commit**: В проекте реализован pre-commit, автоматизирующий проверку кода на соответствие стандартам перед каждым коммитом. Это обеспечивает единообразие кода и улучшает его качество.

### Используемый стек

- **Python**: Версия 3.11
- **MongoDB с использованием PyMongo**: Версия 4.6.0 - Для эффективного хранения и извлечения данных.
- **tinydb**: Версия 4.8.0 - Для работы с локальной базой данных.
- **flask**: Версия 3.0.0 - Легковесный веб-фреймворк для Python.
- **requests**: Версия 4.6.0 - Для взаимодействия с веб-запросами.
- **python-dotenv**: Версия 1.0.0 - Загрузка переменных окружения из файлов .env для конфигурации.
- **pre-commit**: Версия 3.5.0 - Автоматическая проверка и форматирование кода перед коммитом

### Внешнее ПО и другие инструменты

- **PyCharm**: Интегрированная среда разработки Python.
- **Docker**: Контейнеризация приложения и зависимостей для легкого развертывания.
- **Postman**: Инструмент для тестирования и проверки функциональности API.
- **Git**: Система контроля версий для отслеживания изменений в коде, обеспечивает управление кодовой базой и совместную работу над проектом.

## Локальный запуск приложения (используя Docker и MongoDB)

Для этого необходимо выполнить следующие шаги:

### Установка и настройка внешнего ПО:
- Docker: Если у вас ещё не установлен Docker, следуйте инструкциям на официальном сайте Docker для вашей операционной системы: https://docs.docker.com/get-docker/. После установки убедитесь, что Docker Daemon запущен.
- Docker Compose: Установите Docker Compose, если он ещё не установлен. Docker Compose используется для управления многоконтейнерными приложениями. Инструкции по установке можно найти здесь: https://docs.docker.com/compose/install/

### Запуск приложения:
- Клонирование репозитория
```
git clone git@github.com:Leenominai/test_leadhit.git
```
- Переход в рабочую папку приложения
```
cd backend
```
- Настройка файлов окружения: Создайте файл окружения .env в корне вашего проекта - используется для хранения переменных окружения
- Скопируйте все данные из файла .env.example в файл .env
- Запуск контейнеров: Запустите приложение с помощью Docker Compose:
```
cd ..
cd docker
docker-compose up -d
```

## Локальный запуск приложения (используя TinyDB)

Для этого необходимо выполнить следующие шаги:

- Клонирование репозитория
```
git clone git@github.com:Leenominai/test_leadhit.git
```
- Переход в рабочую папку и запуск приложения:
```
cd backend
python app_tinydb.py
```

## Проверочное тестирования приложение

Уделено внимание тестированию нашего приложения. Существует два варианта тестирования:

### Ручное тестирование через Postman:

Для тестирования через программу Postman необходимо:
- Установить её на свою рабочую машину с официального сайта: https://www.postman.com/
- После установки необходимо перейти в раздел Workspaces
- Создать новый Request через +, либо изменить стандартный
- В шкалу URL необходимо ввести следующий адрес: http://127.0.0.1:5000/get_form
- Слева от введённого адреса выбрать тип запроса: POST
- Далее, необходимо выбрать блок Body и раздел x-www-form-urlencoded под ним.
- Для загрузки используем следующий формат: Key и Value. Необходимо в каждое из полей поставить следующие значения (то, что после =):
```
    Key = user_email и Value = test@example.com
    Key = user_phone и Value = +7 921 123 45 67
    Key = user_phone и Value = +7 921 891 23 45
```
- Нажать кнопку Send (отправить запрос)

Ответ системы может быть двух видов:
- Если подходящий шаблон форм найден:
```
  "User contacts"
```
- Можно изменить запрос:
```
    Key = user_email и Value = test@example.com
    Key = user_phone1 и Value = +7 921 123 45 67
    Key = user_phone2 и Value = +7 921 891 23 45
```
- И получить другой ответ:
```
{
    "user_email": "email",
    "user_phone1": "phone",
    "user_phone2": "phone"
}
```

При тестировании через Postman коды ответа системы можно будет увидеть:
- При локальном запуске через Docker с MongoDB:
    ```
    docker logs test_backend
    ```
- При локальном запуске с TinyDB - в консоли используемого IDE-приложения в терминале, где был запущен файл app_tinydb.py

### При помощи скрипта с тестовой базой:

Необходимо запустить файл с проверками, включающий множество различных тестовых запросов.
Просмотр ответа системы реализован через логгирование.

- При локальном запуске через Docker и MongoDB необходимо перейти внутрь контейнера и запустить файл test_requests.py:
    ```
    docker exec -it test_backend bash
    python test_requests.py
    exit
    ```
    После выполнения кода данного скрипта ответ можно будет увидеть в командной строке используемого IDE-приложения.
- При локальном запуске с TinyDB необходимо запустить файл из рабочих папок напрямую:

  Не забываем запустить само приложение:
    ```
    cd ..
    cd backend
    python app_tinydb.py
    ```
  Запускаем скрипт проверки через новое окно терминала (чтобы не прерывать работу программы):
    ```
    cd ..
    cd backend
    python test_requests.py
    ```
    После выполнения кода данного скрипта ответ можно будет увидеть в командной строке вашего IDE-приложения во вкладке терминала, где вы запускали основной файл app_tinydb.py


### Доступные пути API

- **http://127.0.0.1:5000/get_form**: путь для принятия POST-запросов на поиск шаблонов форм.

## Разработчики

Проект разработан и поддерживается Александром Рассыхаевым.

GitHub: [Ссылка на GitHub профиль](https://github.com/Leenominai)

Telegram: [@Leenominai](https://t.me/Leenominai)
