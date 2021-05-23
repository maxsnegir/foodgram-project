# Проект "Foodgram"

![example workflow](https://github.com/maxsnegir/foodgram-project/actions/workflows/foodgram.yml/badge.svg)

### Описание

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты в список
«Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии

- Python 3.8
- Django 3.0.5
- djangorestframework 3.11.0
- Postgres 12
- Docker
- Nginx 1.19.3

### Копирование репозитория

*Через http протокол:*

```bash
git clone https://github.com/maxsnegir/foodgram-project.git
```

*Через ssh протокол:*

```bash
git clone git@github.com:maxsnegir/foodgram-project.git
```

## Запуск проекта

_Все команды должны выполняться в главной директории проекта._

1. Создайте файл **.env** со следующеми переменными окружения для работы с
   базой данных:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=admin # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

2. Убедитесь, что у вас
   установлен [Docker](https://www.docker.com/products/docker-desktop)
   и запустите проект командой:

```bash
docker-compose up 
```

_Проект запущен и доступен по адресу http://foodgram.cf или http://178.154.251.11

3. Чтобы выполнить миграции, собрать статические файлы и создать
   суперпользователя, выполните:

```bash
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

### Автор

[Максим Снегирёв](https://t.me/maxsneg)



