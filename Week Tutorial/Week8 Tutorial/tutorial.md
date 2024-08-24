# WEEK 8: Django Templates

**สำหรับการใช้งาน static files (images, css ,js เราจะต้องทำการตั้งค่ากันก่อน)**

## Configuring static files

1. ดูว่าใน "INSTALLED_APPS" นั้นมี "django.contrib.staticfiles" อยู่
2. เพิ่มการกำหนดว่า static files ของโปรเจคจะอยู่ที่ folder ไหนใน `settings.py`

```python
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

3. สร้าง folder `static` ในระดับเดียวกับ folder `polls` และใส่ไฟล์ statics ที่ต้องใช้ใน folder `static`
4. ในไฟล์ template ของคุณ ให้ load template tag "static" และเรียกใช้ดังนี้

```python
{% load static %}
<img src="{% static 'my_app/example.jpg' %}" alt="My image">
```

5. เก็บ static files ใน folder "static"

## Let's start the tutorial

เราจะมาปรับแก้ไข app "polls" ที่เราได้ทำกันไปใน WEEK 7 กันนะครับ

### index.html

ขั้นตอนแรกเราจะแก้ไขในไฟล์ `polls/views.py` เพื่อแสดงคำถามทั้งหมด

```python
...
class IndexView(View):
    def get(self, request):
        question_list = Question.objects.order_by("-pub_date")
        context = {"question_list": question_list}
        return render(request, "index.html", context)
...
```

จากนั้นเราจะมาปรับไฟล์ `/polls/templates/index.html`

```html
<html>
    <head>
    </head>
    <body>
        <h1>Lastest questions</h1>
        {% if question_list %}
            <ul>
            {% for question in question_list %}
                <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No polls are available.</p>
        {% endif %}
    </body>
</html>
```

โดยเพิ่มให้แสดงคำถาม `question_text` ไม่เกิน 40 ตัวอักษร [truncatechars](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#truncatechars) และ แสดง pub_date "Fri 31, Jan 24" [date](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#date)

```html
...
<li><a href="/polls/{{ question.id }}/">{{ question.question_text|truncatechars:40 }}</a> - Published date: {{question.pub_date|date:"D d, M y"}}</li>
...
```

ผมคิดว่าเราน่าจะทำให้เวบไซต์ของเราสวยขึ้นสักหน่อยโดยใช้ css framework "Bulma"

ก่อนอื่นไป [download](https://github.com/jgthms/bulma/releases/download/1.0.2/bulma-1.0.2.zip) ไฟล์ bulma.css มาจาก website "https://bulma.io/"

จากนั้นวางไฟล์ bulma.css ไว้ใน folder `static/css/bulma.css`

และเพิ่ม `{% load static %}` และ import css ไฟล์ใน <head></head>

```html
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Index</title>
    <link rel="stylesheet" href="{% static 'css/bulma.css' %}">
    </head>
    <body>
        <section class="section">
            <h1 class="title">All questions</h1>
            <div class="content">
            {% if question_list %}
                <ul>
                {% for question in question_list %}
                <li><a href="{% url 'detail' question.id %}">{{ question.question_text|truncatechars:40 }}</a>
                    - Published date: {{question.pub_date|date:"D d, M y"}}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No polls are available.</p>
            {% endif %}
            </div>
        </section>
        <section class="section">
            <p class="subtitle">
                Total: {{question_list|length}} questions <!-- ใช้ filter length เพื่อแสดงขนาดของ list question_list -->
            </p>
        </section>
    </body>
</html>
```

### detail.html

จากนั้่นเราไปแก้ไขหน้า `detail.html` ให้สวยงามกันบ้าง

```html
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Detail</title>
    <link rel="stylesheet" href="{% static 'css/bulma.css' %}">
    </head>
    <body>
        <section class="section">
            <h1 class="title">Question: {{ question.question_text }}</h1>
            <p class="subtitle">Published date: {{ question.pub_date|date:"D d, M Y" }} ({{ question.pub_date|timesince }})</p>
            <div class="content">
            <ul>
                {% for choice in choices %}
                    <li>Choice {{forloop.counter}} => {{ choice.choice_text }} (Votes: {{choice.votes}})</li>
                {% endfor %}
            </ul>
            <a href="{% url 'vote' question.id %}" class="button ml-3">Let's Vote</a>
            <p class="subtitle is-6">Current time: {% now "D d, M Y" %}</p>
            </div>
        </section>
    </body>
</html>
```

จะเห็นได้ว่าเรามีการใช้งาน filter `timesince` และ ใช้งาน `forloop.counter` เพื่อแสดงหมายเลขรอบของ for loop

และมีการใช้งาน template tag `now` เพื่อแสดง วัน-เวลา ปัจจุบัน

### vote.html

สุดท้ายเราไปแก้ไขหน้า `vote.html` ให้สวยงามกัน

```html
{% load static %}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Detail</title>
    <link rel="stylesheet" href="{% static 'css/bulma.css' %}">
    </head>
    <body>
        <section class="section">
            <h1 class="title">Question: {{ question.question_text }}</h1>
            <p class="subtitle">Published date: {{ question.pub_date|date:"D d, M Y" }} ({{ question.pub_date|timesince }})</p>
        </section>
        <div class="container pl-6 pt-1">
            <form action="{% url 'vote' question.id %}" method="POST">
            {% csrf_token %}
            <div class="field">
                {% for choice in choices %}
                <div class="control">
                    <label class="radio">
                        <input type="radio" id="choice{{ forloop.counter }}" name="choice" value="{{ choice.id }}">
                        {{ choice.choice_text }}
                    </label>
                </div>
                {% endfor %}
            </div>
              
            <div class="field">
                <div class="control">
                  <input type="submit" class="button is-link" value="Submit">
                </div>
            </div>
            </form>
        </div>
    </body>
</html>
```

จะเห็นได้ว่ามีการใช้งาน template tag `csrf_token` และ `url`

#### What is CSRF Token in Django?

[Source](https://www.geeksforgeeks.org/csrf-token-in-django/)

> Django provides a feature to prevent such types of malicious attacks. When a user is authenticated and surfing on the website, Django generates a unique CSRF token for each session. This token is included in forms or requests sent by the user and is checked by the server to verify that the request is coming from the authenticated user and not from a malicious source.
