

## Django Installation

ตรวจสอบว่ามีการติดตั้ง Python แล้วในเครื่อง
Windows & MacOS

    py --version
    python --version
## Windows
**Install virtualenv**

    pip install virtualenv

**Create a virtual environment**

    py -m venv myvenv

**Activate virtual environment**

    myvenv\Scripts\activate.bat

**Install Django**

    pip install django

ตรวจสอบว่า install สำเร็จหรือไม่ด้วย command

    python -m django --version
**สร้าง project ชื่อ  `mysite`  ด้วย command**

    django-admin startproject mysite
**Runserver**

    python manage.py runserver
**ทำการสร้าง Apps**

    python manage.py startapp polls
