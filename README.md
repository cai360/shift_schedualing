
```
schedule-system/
│
├── app/
│   ├── __init__.py         ← create_app(), set the Flask app、initial db、register blueprints
│   ├── models.py           ← (plan to)desine SQLAlchemy ORM models（change CS50 SQL into Flask-SQLAlchemy in to future）
│   ├── routes/
│   │   ├── __init__.py     ← import and register blueprint
│   │   ├── auth.py         ← login/logout..etc
│   │   ├── manager.py      ← manager related router
│   │   └── employee.py     ← employee related 
│   ├── services/           ← (plan to develop the scedualing login )
│   ├── static/             ← CSS 
│   └── templates/          ← Jinja2 HTML files
│
├── helper.py              ← login_required, apology 
├── schedule.py            
├── config.py              
└── run.py                 ← entry of starting Flask
```
