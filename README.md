# create_invoices_flask

Приложение для просмотра накладных и скачивания их в формате .docx

##Как развернуть проект:
Клонируем проект
```
git clone https://github.com/metro6/create_invoices_flask.git
cd create_invoices_flask
```
Создаем виртуальное окружение и активируем его
```
python3 -m venv venv
source/bin/activate
```
Устанавливаем зависимости проекта
```
(venv) pip install -r requirements.txt
```
Применяем миграции
```
(venv) flask db upgrade
```
Проект Готов!
Для запуска проекта:
```
(venv) python app.py
```
Приложение стартует по адресу http://localhost:5000

Далее, заходим на сайт, создаем нового пользователя, и форму продуктов

###В проекте используются:
- flask 
- python-docx (https://python-docx.readthedocs.io/en/latest/index.html)
- sqlite
- SQLAlchemy
- jquery, jquery-datetimepicker
