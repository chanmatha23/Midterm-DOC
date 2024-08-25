
## Including other URLconfs

    from  django.contrib  import  admin
    from  django.urls  import  path, include
    
    urlpatterns  = [
	    path('admin/', admin.site.urls),
	    path('employee/', include('employee.urls')),
    ]

> โดยปกติเราจะแบ่งไฟล์ urls.py ไปอยู่แต่ละ app เพื่อความเป็นสัดส่วนดังนั้นเราสามารถใช้่  `include()`  ในการบอก Django ได้ว่าให้ไป match URL ที่ไฟล์ไหน

## function-based views

    from django.http import HttpResponse
    import datetime
    
    def current_datetime(request):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

> Important! อย่าลืมว่าเราจะเรียก view นี้ได้จะต้องไป map URL มาที่ view นี้ก่่อนนะครับใน urls.py

## Class-based view 

    from .models  import  *
    from  django.shortcuts  import render
    from  django.views  import  View
    from django.db.models import *
    
    class  EmployeeView(View):
	    def  get(self, request):
		    emp  =  Employee.objects.all()
		    return render(request, "employee.html", {'emp':emp})

> ในกรณีที่ใช้ class-based view ในไฟล์ urls.py จะต้องปรับนิดหน่อย โดยจะต้องเรียก  `as_view()`

    from  django.urls  import  path
    from .views  import  *
    urlpatterns  = [
		path('', EmployeeView.as_view(), name='employee'),
		path('position/', PositionView.as_view(), name='position'),
		path('project/', ProjectView.as_view(), name='project'),
		path('project/detail/<int:id>/', ProjectDetail.as_view(), name='projectdetail'),
		path('project/detail/<int:id>/remove/<int:staffid>/', ProjectDetail.as_view(), name='projectremovestaff'),
		path('project/detail/<int:id>/add/<int:staffid>/', ProjectDetail.as_view(), name='projectaddstaff'),
		path('project/delete/<int:id>/', ProjectView.as_view(), name='projectdelete'),
	]
### Dynamic URLs in Templates

    <nav>
	    <a  href="{% url 'project' %}">Project</a>
	    <a  href="{% url 'employee' %}">Employee</a>
	    <a  href="{% url 'position' %}">Position</a>
    </nav>
### Comment in HTML & Django not compile

    {# <button  type="submit"  onclick="deleteProject({{ }})"  class="delete">Delete</button> #}
### Views in Ex

    from  django.http  import  JsonResponse
    class  ProjectDetail(View):
	    def  get(self, request, id):
		    pro  =  Project.objects.get(pk=id)
		    startdate  =  pro.start_date.strftime('%Y-%m-%d')
		    duedate  =  pro.due_date.strftime('%Y-%m-%d')
		    staff  =  pro.staff.all()
		    return  render(request, "project_detail.html", {'pro':pro, 'start':startdate, 'due':duedate, 'staff':staff})
	    def  delete(self, request, id, staffid):
		    pro  =  Project.objects.get(pk=id)
		    pro.staff.remove(staffid)
		    return  JsonResponse({'Kickstaff': True})
	    def  put(self, request, id, staffid):
		    pro  =  Project.objects.get(pk=id)
		    pro.staff.add(staffid)
		    return  JsonResponse({'add': True})

> อย่าลืมเวลาจะใช้ strfttime ต้อง import `from  django.db.models  import  *`
> `%Y`: ปีแบบเต็ม (เช่น 2024)
> `%Y`: ปีแบบเต็ม (เช่น 2024)
> `%m`: เดือนแบบตัวเลข (01-12)
>`%d`: วันในเดือน (01-31)
> `%H`: ชั่วโมง (00-23)
> `%M`: นาที (00-59)
>  `%S`: วินาที (00-59)
>  `%a`: วันในสัปดาห์ (ย่อ) (เช่น Mon)
>  `%A`: วันในสัปดาห์ (เต็ม) (เช่น Monday)
>  `%b`: เดือน (ย่อ) (เช่น Jan)
>  `%B`: เดือน (เต็ม) (เช่น January)
>  `%I`: ชั่วโมงในรูปแบบ 12 ชั่วโมง (01-12)
>  `%p`: AM หรือ PM
>  `%f`: ไมโครวินาที (000000-999999)
### Django Template Language

The Django Template Language, DTL, interpolates Python into HTML.

    <html>
      <head>  
     {% block titl	e %}
     {% endlbock %} 
      </head>
      <body>
     {% block content %}
     {% endblock %}
      </body>
    </html>

### Base Templates

Template สามารถใช้เป็นพื้นฐานสำหรับ Template อื่นๆ ได้โดยใช้  `extends`  tag.

    {% extends "base.html" %}


### Loading Static Files

Templates can load static files using the `{% load static %} tag in the header of the HTML file. Specific files can be loaded by specifying the exact file path as an argument.

    {% load static "custom.css" %}

### Template Variables

Variables can be displayed using variable tags.

    {{ variable_name }}

### Conditional Tags

Templates can include logic using  `if`  statements.
-   {% if[not]equal user.id comment.user_id %} ... [{% else %}] ... {% endif[not]equal %}
    {% if conditional_variable %}
    
    {% endif %}

### for-in Loops

Template variables can be iterated over using  `for`-`in`  loops inside template tags.

    <ul>
    
     {% for item in dictionary %}
    
      <li>{{ item.value }}</li>
    
     {% endfor %}
    
    </ul>


### Template Filters

Filters เรียกใช้โดยใช้สัญลักษณ์  `|`

    {{ variable_name | filter_name }}

### Filter Arguments

Arguments สามารถส่งผ่านไปยังตัวกรองได้โดยใช้สัญลักษณ์  `:` 

    {{ variable_name | filter_name:"argument"}}

### Sorting Dictionaries

Dictionaries can be sorted using the  `dictsort`  filter.

    {{ dictionary_name | dictsort:"key_name"}}

### Datatypes in Filters

Some filters require variables of a certain data type.

    {{ date_time | time"H": "i" }}
