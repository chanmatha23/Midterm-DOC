# Writing your first view

ก่อนจะไปสร้าง view เรามาทำการ setup project "week7_tutorial" และสร้าง app "polls" กันก่อน
และทำการ copy models เหล่านี้ลงไปที่ `polls/models.py`

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

จากนั้นก็ `makemigrations` และ `migrate` และทำการ import `polls.sql` เข้าไปใน database

## Let's start!

สำหรับ poll application เราสร้างจะ views ดังต่อไปนี้

- Question “index” page – แสดงรายการ questions ล่าสุด
- Question “detail” page – แสดง question text และตัวเลือก
- Vote action – สำหรับทำการ vote

เรามาเริ่มต้นด้วยการเพิ่ม code ด้านล่างนี้ใน `/polls/views.py`

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the index page of polls app")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

กำหนด path สำหรับเข้าถึง `urls.py` ของ app polls ใน `week7_tutorial/urls.py`

```python
...

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
]
```

กำหนด path url สำหรับเข้าถึง views ด้านบน `/polls/urls.py`

```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

หมายเหตุ: <int:question_id> เป็นการประกาศ path parameter ซึ่งจะรับค่าตัวแปรที่ถูกส่งมาใน url

## Write views that actually do something

เรามาปรับแก้ไข view index() ให้ทำการ query ข้อมูล question 5 รายการล่าสุด เรียงตาม pub_date แบบจากมากไปน้อย

```python
from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)

# Leave the rest of the views (detail, results, vote) unchanged
```

ใน view index() เราได้ทำการ return list ของ questions ออกมา และส่งต่อข้อมูลไปยัง `/polls/index.html`

เอ้ะแต่ไฟล์ `/polls/index.html` มันอยู่ไหน ไม่เห็นมี @_@

เราจะต้องไปสร้างไฟล์ **template** ก่อน โดยสร้าง folder `/polls/templates` และสร้างไฟล์ `/polls/templates/index.html` และเพิ่ม code ด้านล่าง

```html
<html>
    <head>
    </head>
    <body>
        <h1>Lastest questions</h1>
        {% if latest_question_list %}
            <ul>
            {% for question in latest_question_list %}
                <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No polls are available.</p>
        {% endif %}
    </body>
</html>
```

แก้ไขไฟล์ `mysite/settings.py` เพิ่ม code ดังนี้

```python
import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, 'templates'),
)
```

เรามาลอง start server ดูว่าหน้า index สามารถใช้งานได้ไหม

เปิด browser และพิมพ์ url `http://127.0.0.1:8000/polls/`
จะเห็นว่ามีรายการ questions แสดงขึ้นมา 5 รายการ

เรามาทำให้ view อื่นๆ ใช้งานได้่กัน

```python
from django.shortcuts import render, redirect

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "detail.html", {
        "question": question,
        "choices": question.choice_set.all().order_by("choice_text")
    })

def vote(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == "GET":
        return render(request, "vote.html", {
            "question": question,
            "choices": question.choice_set.all().order_by("choice_text")
        })
    elif request.method == "POST":
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        return redirect("detail", question_id=question_id)
```

สร้างไฟล์ `/polls/templates/detail.html` และเพิ่ม code ด้านล่าง

```html
<html>
    <head>
    </head>
    <body>
        <h1>Question: {{ question.question_text }}</h1>
        <p>Publist date: {{ question.pub_date }}</p>
        <ul>
        {% for choice in choices %}
            <li>{{ choice.choice_text }} (Votes: {{choice.votes}})</li>
        {% endfor %}
        </ul>
        <br/>
            <a href="{% url 'vote' question.id %}">
            <button>Let's Vote</button>
        </a>
    </body>
</html>
```

สร้างไฟล์ `/polls/templates/vote.html` และเพิ่ม code ด้านล่าง

```html
<html>
    <head>
    </head>
    <body>
        <h1>Question: {{ question.question_text }}</h1>
        <p>Publist date: {{ question.pub_date }}</p>
        <form action="/polls/{{ question.id }}/vote/" method="POST">
            {%csrf_token%}
            <ul>
            {% for choice in choices %}
                <li>
                    <input type="radio" id="choice{{ forloop.counter }}" name="choice" value="{{ choice.id }}">
                    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label>
                </li>
            {% endfor %}
            </ul>
            <input type="submit" value ="VOTE" name="submit"/>
        </form>
    </body>
</html>
```

## Let's try class-based views

เรามาลองเปลี่ยนเป็น class-based views กันบ้างนะครับ จะเห็นว่า code เป็นระเบียบขึ้น (ผมคิดว่านะ...)

**แก้ไขใน `polls.views`**

```python
from django.shortcuts import render, redirect
from django.views import View

from .models import Question, Choice


class IndexView(View):

    def get(self, request):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        context = {"latest_question_list": latest_question_list}
        return render(request, "index.html", context)

class PollView(View):

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        return render(request, "detail.html", {
            "question": question,
            "choices": question.choice_set.all()
        })

class VoteView(View):

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        return render(request, "vote.html", {
            "question": question,
            "choices": question.choice_set.all()
        })
    
    def post(self, request, question_id):
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        return redirect("detail", question_id=question_id)
```

อย่าลืมไปแก้ไข `polls/urls.py` ด้วยนะครับเพิ่ม `.as_view()`

```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.PollView.as_view(), name="detail"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
]
```
