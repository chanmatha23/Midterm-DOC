

## Django Installation
# Install virtualenv

```python
pip install virtualenv
python -m venv myvenv
myvenv\Scripts\activate.bat

#New Django project
pip install django
django-admin startproject myshop
python manage.py startapp shop 
#start server: python manage.py runserver

#Postgres client
pip install psycopg2-binary

#Jupyter Notebook
pip install django-extensions ipython jupyter notebook   
pip install ipython==8.25.0 jupyter_server==2.14.1 jupyterlab==4.2.2 jupyterlab_server==2.27.2
pip install notebook==6.5.6 #or 6.5.7
mkdir notebooks
python manage.py shell_plus --notebook

#Startup
python manage.py migrate
python manage.py makemigrations
```

# Projects Settings

project_name/urls.py

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("employee.urls")), #<--ชื่อแอพ
]
```

project_name/settings.py

```python

# Database setting

DATABASES = {
	"default": {
			"ENGINE": "django.db.backends.postgresql",
			"NAME": "db_name",
			"USER": "postgres",
			"PASSWORD": "1234",
			"HOST": "localhost",
			"PORT": "5432",
	}
}

# Add app blogs to INSTALLED_APPS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    #'django.contrib.humanize',
    "employee",
]

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

# jupyter notebook

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

#EX
from blogs.models import Blog
for blog in Blog.objects.all():
    print(blog)
```
