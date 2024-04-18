# **Предварительные требования**
## Убедитесь, что на вашем компьютере установлены Python и pip. Проект тестировался с Python 3.10.2.

## **Клонирование репозитория**

    git clone https://github.com/rustem02/sdu_dorm.git

    cd sdu_dorm

## **Установка зависимостей**

    pip install -r requirements.txt


## **Применение миграций**

  Примените миграции для настройки вашей базы данных:

    python manage.py migrate

## **Запуск проекта**

  ### Windows:

    python manage.py runserver


  ### MacOS/Linux:

    python3 manage.py runserver
