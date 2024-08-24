# Class-based views

Class-based view นั้นโดยหลักแล้วจะมีไว้เพื่อให้เราสามารถกำหนด response สำหรับ HTTP request method ที่แตกต่างกันได้ แทนที่จะต้องมาใช้ if ดังเช่นในกรณี function-based view

```python
from django.http import HttpResponse


def my_view(request):
    if request.method == "GET":
        # <view logic>
        return HttpResponse("result")
    elif request.method == "POST":
        # <view logic>
        return HttpResponse(status=201)
```

แต่ถ้าเป็น class-based view จะเขียนได้ดังนี้

```python
from django.http import HttpResponse
from django.views import View


class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse("result")
    
    def post(self, request):
        # <view logic>
        return HttpResponse(status=201)
```

ในกรณีที่ใช้ class-based view ในไฟล์ urls.py จะต้องปรับนิดหน่อย โดยจะต้องเรียก `as_view()`

```python
# urls.py
from django.urls import path
from myapp.views import MyView

urlpatterns = [
    path("about/", MyView.as_view()),
]
```

## Handling forms with class-based views

การใช้งาน form ใน function-based view จะเป็นประมาณนี้

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm


def myview(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")
    else:
        form = MyForm(initial={"key": "value"})

    return render(request, "form_template.html", {"form": form})
```

ส่วนถ้าใช้ใน class-based view จะเป็นดังนี้

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm


class MyFormView(View):
    form_class = MyForm
    initial = {"key": "value"}
    template_name = "form_template.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect("/success/")

        return render(request, self.template_name, {"form": form})
```

จะเห็นได้ว่ามีการแยกที่เป็นสัดส่วนระหว่าง GET และ POST และสามารถกำหนด class attributes ได้ด้วย


## Decorating class-based views

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class ProtectedView(TemplateView):
    template_name = "secret.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

หรือ

```python
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(never_cache, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "secret.html"
```