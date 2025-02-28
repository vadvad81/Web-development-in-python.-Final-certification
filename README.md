# Проект “Сайт рецептов” на Django

Данный проект является реализацией итоговой аттестации по программе
“Вебразработка на Python” и представляет собой веб-приложение
для хранения и просмотра рецептов. 
Пользователи могут добавлять, просматривать и редактировать рецепты, 
а также просматривать рецепты других пользователей.

## Установка
1. Общая подготовка

Что нужно:
- собственный сервер на ubuntu с возможность созадвадть виртуалки kvm
- белый IP, для испольования сайта через сеть Интернет (есть)
- доменное имя (recipe.yermolov.ru)

Разворачиваем виртуальную машину с помощью QEMU/KVM на сервере (recipe_site ip 192.168.1.132)


Делаем обнавление sudo apt update && sudo apt upgrade
```bash
sudo apt update && sudo apt upgrade
```

Делаем snapshot виртуалки

Размещаем проект в  домащней директории пользователя (git или ручками, на усмотрение)

2. Установите зависимости:

Установить пакет venv (версия может быть другой)
apt install python3.10-venv 
```bash
apt install python3.10-venv
```

перейти в каталог с сайтом и установить виртульаное окружение
root@recipe:/home/ermolov/recipe_site# python3 -m venv venv
```bash
python3 -m venv venv
```

активировать виртульаное окружение
root@recipe:/home/ermolov/recipe_site# source venv/bin/activate
(venv) root@recipe:/home/ermolov/recipe_site#
```bash
source venv/bin/activate
```

устанавливаем зависимости
(venv) root@recipe:/home/ermolov/recipe_site# pip install -r requirements.txt
```bash
pip install -r requirements.txt
```

3. Примените миграции базы данных:
(venv) root@recipe:/home/ermolov/recipe_site# python manage.py migrate
```bash
python manage.py migrate
```

4. Для создания суперпользователя:
(venv) root@recipe:/home/ermolov/recipe_site# python manage.py createsuperuser
Имя пользователя (leave blank to use 'root'): ermolov
Адрес электронной почты:
Password:
Password (again):
Superuser created successfully.
```bash
python manage.py createsuperuser
```
    
5. Сгенерируйте новый SECRET_KEY
создайте новый ключ командой:
(venv) root@recipe:/home/ermolov/recipe_site# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
здесь выводится на экран ключ который нужен далее
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
   
SECRET_KEY хранится в переменной окружения (рекомендуется для безопасности):

Установите переменную окружения:
```bash
export SECRET_KEY="ваш-секретный-ключ"
```

6. Прописать все домены и ip адреса
в файле /home/ermolov/recipe_site/recipesite/settings.py
ALLOWED_HOSTS = []
добавить ip и адреса доступа к сайту
мой выглядит так:
ALLOWED_HOSTS = [
    '127.0.0.1',
    '192.168.1.132',
    'recipe.yermolov.ru', #ЗАМЕНИТЬ НА СВОЙ
]

7. Запустите сервер разработки Django:
```bash
python manage.py runserver 192.168.1.132:8000
```

8. Откройте ваш веб-браузер и перейдите по адресу 192.168.1.132:8000, чтобы начать использование приложения.


9. Зайти на админ панель по адресу 192.168.1.132:8000/admin
- добавить категории блюд, иначе пользоватлеи не смогут добовлять рецепты

10. добавил поддомен recipe.yermolov.ru

11. Настроил реверс прокси, чтобы прокисровал запросы из интернета
мой caddyfile
http://recipe.yermolov.ru{
	reverse_proxy 192.168.1.132:8000
}



12 после перезагрузки сервера
- войти в рут права (sudo su)
- перейти в каталог с проектом
source venv/bin/activate
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
export SECRET_KEY="ваш-секретный-ключ"
python manage.py runserver 192.168.1.132:8000




## Функции

- Регистрация и аутентификация пользователей
- Просмотр главной страницы с 3 рецептами кратко
- Просмотр подробной информации о рецепте
- Добавление, редактирование рецептов
- Возможность добавления изображения для рецепта
- Категоризация рецептов

## Технологии

- Python
- Django - фреймворк для разработки веб-приложений
- HTML/CSS - для создания пользовательского интерфейса

## Проект развернут по адресу : 

[https://recipe.yermolov.ru/] 
