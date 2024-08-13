1. Клонування репозиторію
git clone https://github.com/r2r-company/TopPos.git
cd TopPos

2. Створення і активація віртуального середовища
Для Windows:
python -m venv venv
venv\Scripts\activate
Для MacOS/Linux:

3. Встановлення залежностей
pip install -r requirements.txt

4. Налаштування бази даних
python manage.py migrate


5. Створення суперкористувача
python manage.py createsuperuser


6. Запуск сервера розробки
python manage.py runserver
