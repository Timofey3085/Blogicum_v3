![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Hi,+I'am+a+Python+developer.)](https://git.io/typing-svg)
# django_sprint4

## Усовершенствованный проект Blogicum

### Функционал:

- Посмотреть опубликованные посты.

- Осортировать по категории.

- Регистрация и авторизация.

- Создание постов.

- Написание комментариев к постам.

- Редактирование собственного профиля.

- Редактирование своих постов.

- Редактирование своих комментариев.

#### Как начать?

Скопировать код:
```python
git clone git@github.com:Timofey3085/django_sprint4
```
Создать виртуальное окружение и установить зависимости:
```bash
cd django_sprint3                    # переходим в папку django_sprint3
python -m venv venv                  # создаем виртуальное окружение
source venv/bin/activate             # включаем виртуальное окружение (если у вас не терминал bash замените bin на Scripts)
pip install --upgrade pip            # обновляем установщик пакетов pip
pip install -r requirements.txt      # устанавливаем необходимые для работы проекта зависимости
```
Перейти в папку blogicum и вы полнить первоначальные действия:
```bash
cd blogicum                         # переходим в папку blogicum
python manage.py migrate            # выполняем миграции
python manage.py createsuperuser    # создаем суперюзера
python manage.py loaddata db.json   # загружаем первоначальные данные
```
#### Для просмотра главной страницы переходим по адресу localhost:8000/.

#### Для просмотра постов данной категории переходим по адресу localhost:8000/category/<slug>/.

#### Для просмотра конкретного поста переходим по адресу localhost:8000/posts/<id>/.

#### Для просмотра конкретного профиля переходим по адресу localhost:8000/profile/<slug>/.

#### Админ зона находится по адресу localhost:8000/admin/, логин и пароль - те что вы задавали при команде python manage.py createsuperuser.
Автор.
[Timofey - Razborshchikov](https://github.com/Timofey3085)
