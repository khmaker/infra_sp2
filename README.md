# YaMDb

## База отзывов о фильмах, книгах и музыке

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список
категорий (Category) может быть расширен (например, можно добавить категорию
«Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или
послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в
категории «Книги» могут быть произведения «Винни Пух и все-все-все» и
«Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы
«Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из
списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры
может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые
отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного
до десяти). Из множества оценок автоматически высчитывается средняя оценка
произведения.

## Техническое описание

[Файл с техническим описанием](SPECS.md)

## Запуск

### Требования к системе

Для запуска проекта в системе должен быть
установлен [Docker](https://www.docker.com/)

### Необходимые данные

В файле [./api_yamdb/.env](./api_yamdb/.env) замените следующие значения:

* ```POSTGRES_DB``` имя базы данных
* ```POSTGRES_USER``` имя пользователя базы данных
* ```POSTGRES_PASSWORD``` пароль пользователя базы данных
* ```SECRET_KEY``` Секретный ключ. Используется для 
  [криптографической подписи](https://djbook.ru/rel3.0/topics/signing.html), 
  должен быть случайным и сложным для подбора. Можно сгенерировать по
  ссылке https://djecrety.ir/.
* ```ALLOWED_HOSTS``` Список хостов/доменов, для которых может работать текущий
  сайт. Это сделано для безопасности, чтобы обезопасить от внедрения в куки или
  письма для сброса пароля ссылок на сторонний сайт подменив HTTP заголовок
  Host, что возможно при многих, казалось бы безопасных, конфигурациях сервера.
  Свои адреса можно добавить к уже указанным через пробел.

### Команда для запуска проекта

#### Создать образы, тома, контейнеры и запустить контейнеры

Запускается в каталоге с файлами из командной оболочки.

```shell
docker-compose up -d --build
```
Если все получилось, 
то документация будет доступна 
[здесь](http://localhost:8000/redoc).
### Команды для работы с проектом
Команды для создания учетной записи администратора, 
заполнения базы тестовыми данными 
и стирания базы выполняются внутри контейнера.
#### Вход в командную оболочку контейнера
```shell
docker exec -it web bash
```
#### Заполнение базы тестовыми данными
```shell
python manage.py loaddata fixture.json
```
#### Создание учетной записи администратора
```shell
python manage.py createsuperuser
```
Понадобится ввести имя, адрес электронной почты и пароль.
#### Стирание базы
```shell
python manage.py flush
```
База будет стерта целиком. 
Учетную запись администратора придется создать снова.
#### Выход из командной оболочки контейнера
Выход осуществляется последовательным нажатием двух сочетаний клавиш: 
```Ctrl+P``` и ```Ctrl+Q```



## Создано при помощи

* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [nginx](https://nginx.org/ru/)
* [Docker](https://www.docker.com/)
