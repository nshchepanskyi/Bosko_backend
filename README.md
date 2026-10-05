# bosco-backend

Складський застосунок на шаблонах Django (ПР №2.5).

- Група: `<номер групи>`
- Виконав: `<Прізвище Ім'я>`, номер у групі: `<номер>`
- Стек: Python 3.14, Django 6.1, SQLite

## Структура

```
bosco-backend/
├── README.md
├── .gitignore
├── requirements.txt
├── SELF_STUDY.md          ← звіт з експериментів
└── warehouse/             ← застосунок
    ├── manage.py
    ├── config/            ← налаштування проєкту
    ├── catalog/           ← застосунок з товарами
    └── templates/         ← шаблони
```

## Запуск локально

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd warehouse
python manage.py migrate
python manage.py runserver
```

Сторінки: `/` — список товарів, `/products/add/` — форма додавання.

## Команди

```powershell
python manage.py test          # тести
python manage.py check         # перевірка конфігурації
```