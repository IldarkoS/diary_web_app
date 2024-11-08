# Diary-Web-App
Приложение для управления своими задачами с полноценным интерфейсом для взаимодействия. Сделана регистрация и авторизация. Добавление, удаление, завершение и редактирование уже созданных задач. 

## Взаимодействие
При первом запуске будет предложено авторизоваться или создать аккаунт. После регистрации и входа в аккаунт можно создать задачу, посмотреть подробную информацию, отредактировать, завершить и удалить уже созданную задачу. В списке задачи делятся на завершенные и незавершенные задачи

## Запуск:
- Изменить example.env на .env, при необходимости поменять содержание

docker compose build

docker compose up

Приложение будет доступно по - http://localhost:5000/

## Реализованы методы:
1. Регистрации нового пользователя
- Метод: POST
- URL: /register/

2. Авторизация пользователей:
- Метод: POST
- URL: /login/

3. Выход из аккаунта:
- Метод: GET
- URL: /logout/

4. Получение списка задач:
- Метод: GET
- URL: /view_task/

5. Получение информации о конкретной задаче:
- Метод: GET
- URL: /view_task/<id>

6. Редактирование конкретной задаче:
- Метод: POST
- URL: /view_task/<id>

7. Завершение задачи:
- Метод: POST
- URL: /complete_task/<id>

8. Удаление задачи:
- Метод: POST
- URL: /delete_task/<id>
