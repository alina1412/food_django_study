# food_django_study
Учебный проект (2023)

<img width="1584" height="811" alt="image" src="https://github.com/user-attachments/assets/7da570e5-966f-4a73-984b-f79eca0d4271" />
<img width="1721" height="909" alt="image" src="https://github.com/user-attachments/assets/f8dc4401-6e52-4300-ac4e-3d2fe87cd633" />

# Технологии
- django 4.2
- js, css - шаблон
- bootstrap5
- html
- python 3.10

# Установка
- создать .env (при необходимости, поменять коннекшн к базе)
- python manage.py makemigrations
- python manage.py migrate

- cd /food_django_study/food_recipes && python manage.py makemigrations users

- Пример тестовых данных для базы:
`python manage.py loaddata database.json (Если postgres или в settings установить sqlite, в деплое -mysql )`
- при необходимости создать суперюзера

Пользователи:
- Админкой могут пользоваться юзеры, если staff_status=True: если группа юзера Normal - только просмотр, если юзер-редактор - с редакторскими правами.


Дз1

1) index Шаблон для главной страницы
2) recipe Шаблон для отдельной страницы новости (нужно нажать на квадратную картинку в галерее)
3) foodlist Шаблон страницы со списком новостей
4) profile Страница аккаунта пользователя
5) sidebar Шаблон для меню навигации, который будет интегрироваться в другие шаблоны

-Контакты
-Регистрация / Войти

Дз2
1) Есть поиск по заголовку / аннотации
2) Создать рецепт пока только из админки
3) Можно посмотреть "Мои рецепты" у зарегистрированного пользователя
4) Можно обновлять данные профиля Account пользователя со фронта
5) users_top использует User.objects.annotate
6) Ссылки на изображения в модели File
7) реализованы регистрация и авторизация пользователей.


