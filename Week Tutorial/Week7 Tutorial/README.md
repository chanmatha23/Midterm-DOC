# WEEK7 - The Views

หลังจากที่เราได้เรียนเกี่ยวกับ Models ไปอย่างละเอียดแล้ว วันนี้เราจะมาเรียนเกี่ยวกับส่วนทำคัญอีกส่วนของ concept **MVT** ซึ่งก็คือส่วนของ Views กันนะครับ

# URL dispatcher

[Django document](https://docs.djangoproject.com/en/5.0/topics/http/urls/)

เคยเจอ website ที่มี URL path ยาวๆ และอ่านไม่รู้เรื่องไหมครับ website ที่ดีึควรมี URL path ที่อ่านรู้เรื่อง และ ไม่ยาวจนเกินไป ในหัวข้อนี้เราจะเรียนรู้เกี่ยวกับการออกแบบและกำหนด URL path ใน project Django กันนะครับ

## How Django processes a request

```python
from django.urls import path

from . import views

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
]
```

ตัวอย่างการทำงาน

- ถ้ามี request มาที่ path `/articles/2005/03/` จะ match path ที่ 3 ซึ่งเรียก "views.month_archive"
- ถ้ามี request มาที่ path `/articles/2003/` จะ match path ที่ 1 ซึ่งเรียก "views.special_case_2003"
- แต่ว่า `/articles/2003` จะไม่ match เลยเพราะไม่มี '/'
- ส่วน `/articles/2003/03/building-a-django-site/` จะ match path สุดท้าย ซึ่งเรียก "views.article_detail"

**Note: ไม่จำเป็นจะต้องมี / ตอนต้นของ path**

## Path converters

Django มี path converter ให้ใช้งานดังนี้:

- **str** - Matches any non-empty string, excluding the path separator, '/'. - ซึ่งจะเป็นค่า default ถ้าไม่มีการกำหนด
- **int** - Matches zero or any positive integer. Returns an int.
- **slug** - Matches any slug string consisting of ASCII letters or numbers (สามารถใช้ '-' และ '_') เช่น building-your-1st-django-site.
- **uuid** - Matches a formatted UUID (จะต้่องมี '-' และตัวอักษรเป็นตัวเล็กทุกตัว) เช่น 075194d3-6885-417e-a8a8-6c931e272f00 โดยค่าที่ได้รับใน view จะเป็น instance ของ UUID
- **path** - Matches any non-empty string, including the path separator, '/'.

## Using regular expressions

ถ้าต้องการใช้ regex ในการกำหนด URL สามารทำได้โดยใช้ `re_path()` แทน `path()`

โดย format จะเป็น "(?P<name>pattern)" โดยที่ `name` คือเป็นชื่อตัวแปร และ `pattern` เป็น pattern ที่ต้องการ match

```python
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive),
    re_path(
        r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$",
        views.article_detail,
    ),
]
```

## Including other URLconfs

โดยปกติเราจะแบ่งไฟล์ urls.py ไปอยู่แต่ละ app เพื่อความเป็นสัดส่วน ดังนั้นเราสามารถใช้่ `include()` ในการบอก Django ได้ว่าให้ไป match URL ที่ไฟล์ไหน

```python
from django.urls import include, path

urlpatterns = [
    # ... snip ...
    path("shop/", include("shop.urls")),
    path("contact/", include("contact.urls")),
    # ... snip ...
]
```


*ไปต่อกันที่ไฟล์ `writing-views.md`*