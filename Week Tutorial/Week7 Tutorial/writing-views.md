# Writing Views

[Django Document](https://docs.djangoproject.com/en/5.0/topics/http/views/)

> A view function, or view for short, is a Python function that takes a web request and returns a web response. 

โดยที่ response นั้นอาจจะเป็น HTML page หรือ redirect หรือ 404 error หรือ XML file หรือ รูปภาพ ... จริงๆ แล้วก็คืออะไรก็ได้

โดยปกติเราจะวาง View Function ไว้ใน views.py (แต่จริงๆ วางตรงไหนก็ได้ เรากำหนดการเข้าถึงที่ URLconfs)

## A simple view - function-based views

```python
from django.http import HttpResponse
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
```

*Important! อย่าลืมว่าเราจะเรียก view นี้ได้จะต้องไป map URL มาที่ view นี้ก่่อนนะครับใน urls.py*

## Returning errors

โดยปกติเมื่อเรา return HttpResponse() Django จะ default HTTP status code = 200 ให้ แต่ถ้าเราต้องการกำหนด status code เองก็สามารถทำได้

```python
from django.http import HttpResponse


def my_view(request):
    # ...

    # Return a "created" (201) response code.
    return HttpResponse(status=201)
```

## The Http404 exception

เพื่อความง่าย Django มีหน้า page 404 standard มาให้ (แต่เราสามารถ custom เองได้นะ) โดยถ้าคุณมีการ raise Http404 ตรงไหนใน view ก็ตาม Django จะ catch error นี้ให้และ return page 404 ตัว standard มาให้เสมอ พร้อม HTTP status code = 404

```python
from django.http import Http404
from django.shortcuts import render
from polls.models import Poll


def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, "polls/detail.html", {"poll": p})
```


# View decorators

## What is a decorator?

[Source](https://realpython.com/primer-on-python-decorators/)

ก่อนที่จะเข้าใจ decorator คุณจะต้องเข้าใจ concept เหล่านี้ก่อน

1. First-Class Objects - This means that functions can be passed around and used as arguments, just like any other object like str, int, float, list, and so on.

```python
def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we're the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")
```

เมื่อเรียกใช้งาน

```bash
>>> greet_bob(say_hello)
'Hello Bob'

>>> greet_bob(be_awesome)
'Yo Bob, together we're the awesomest!'
```

2. Inner Functions - It’s possible to define functions inside other functions. Such functions are called inner functions. 


```python
def parent():
    print("Printing from parent()")

    def first_child():
        print("Printing from first_child()")

    def second_child():
        print("Printing from second_child()")

    second_child()
    first_child()
```

เมื่อเรียกใช้งาน

```bash
>>> parent()
Printing from parent()
Printing from second_child()
Printing from first_child()
```

3. Functions as Return Values

```python
def parent(num):
    def first_child():
        return "Hi, I'm Elias"

    def second_child():
        return "Call me Ester"

    if num == 1:
        return first_child
    else:
        return second_child
```

เมื่อเรียกใช้งาน

```bash
>>> first = parent(1)
>>> second = parent(2)

>>> first
<function parent.<locals>.first_child at 0x7f599f1e2e18>

>>> second
<function parent.<locals>.second_child at 0x7f599dad5268>
```

ค่าที่ return ออกมาจะเป็น function ซึ่งสามารถ execute ได้

```bash
>>> first()
'Hi, I'm Elias'

>>> second()
'Call me Ester'
```

### Simple Decorators in Python

ทีนี้่เรามาลองดู decorator ง่ายๆ กัน

```python
def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = decorator(say_whee)
```

เมื่อเรียกใช้งาน

```bash
>>> from hello_decorator import say_whee

>>> say_whee()
Something is happening before the function is called.
Whee!
Something is happening after the function is called.
```

> Put simply, a decorator wraps a function, modifying its behavior.

*ลองมาสร้าง decorator ที่ทำประโยชน์อะไรสักหน่อยจะได้เข้าใจมากขึ้น*

```python
from datetime import datetime

def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

def say_whee():
    print("Whee!")

say_whee = not_during_the_night(say_whee)
```

ถ้าเราเรียก say_whee() หลังเวลา 22.00 ก็จะไม่มีการ print "Whee!" ออกมา

โดย Python เขาก็มี syntax ในการเรียกใช้ decorator ที่ง่ายละเห็นแล้วจำได้ว่าเป็น decorator ก็คือการใช้ `@` ดังในตัวอย่าง

```python
from datetime import datetime

def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

@not_during_the_night
def say_whee():
    print("Whee!")
```


## Allowed HTTP methods decorators

- require_http_methods(request_method_list) ใช้กำหนดว่า view นั้นๆ รับ request ที่มี HTTP Method อะไรได้บ้าง

```python
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def my_view(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    pass
```

- require_GET()
- require_POST()
- require_safe() - Decorator to require that a view only accepts the GET and HEAD methods.

## Other decorators

- `gzip_page()`
- `no_append_slash()`
- `cache_control(**kwargs)`
- `never_cache(view_func)`