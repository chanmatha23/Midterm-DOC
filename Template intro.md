# The Django template language

## Templates

> A template is a text file. It can generate any text-based format (HTML, XML, CSV, etc.).

ด้านล่างเป็นตัวอย่าง template ที่มีการใช้งานทุกๆ concept ที่เราจะพูดถึงในวันนี้

```html
{% extends "base_generic.html" %}

{% block title %}{{ section.title }}{% endblock %}

{% block content %}
<h1>{{ section.title }}</h1>

{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```

## Variables

การแสดงค่าตัวแปรใน tamplate จะใช้ {{ variable }}

โดยถ้าเราพยายามแสดงค่าตัวแปรที่ไม่มีการส่งมาใน template ค่า '' จะถูกแสดงแทน

## Filters

Filters ใช้ในการ modify ค่าของตัวแปร เช่น {{ name|lower }} โดย `|` จะเป็น syntax การ apply filter เข้าไปกับตัวแปร

เราสามารถ chain filter หลายๆตัวได้ เช่น {{ text|escape|linebreaks }}

นอกจากนั้น filter บางตัวก็มีการรับ argument เช่น {{ bio|truncatewords:30 }}

[built-in filter reference](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#ref-templates-builtins-filters)

Filter ที่ใช้บ่อยๆ:

```html
{{ value|default:"nothing" }}

{{ value|length }}

{{ value|filesizeformat }}
<!--If value is 123456789, the output would be 117.7 MB.-->
```

## Tags

Syntax ของ tag จะเป็น {% %} โดย tag จะเกี่ยวข้องกับ control flow และ logic

และบาง tag จะต้องมีการเปิด และ ปิด tag

[built-in tag reference](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#ref-templates-builtins-tags)

เช่น

**for**

```html
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

**if elif else**

```html
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

## Comments

```html
{# greeting #}hello

{# {% if foo %}bar{% else %} #}
```

## Template inheritance

Template inheritance นั้นช่วยให้เราสามารถวางโครงสร้างของหน้าเพจ โดยการสร้าง base "skeleton" เช่น

![layout](./layout.png)

ลองมาดูตัวอย่่างการทำ template inheritance กัน

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

ไฟล์ `base.html` นี้ทำการกำหนดโครงสร้างของหน้าเวบเพจเป็น 3 ส่วนคือ

1. title
2. sidebar
3. content

โดยการใช้ tag **block**

หน้าเพจที่มา extend `base.html` นี้ไปอาจจะเป็นดังตัวอย่าง

```html
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

จะเห็นได้ว่ามีการใช้ tag **extends** - `{% extends "base.html" %}`

หน้า "My amazing blog" นี้จะถูก Django render เป็น HTML ออกมาดังนี้

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

จะเห็นว่าตัวลูกที่ extend `base.html` ไม่ได้ทำการกำหนด block "sidebar" ดังนั้น code ใน block นั้นจะเป็นตามค่าที่กำหนดใน `base.html`

## Automatic HTML escaping

เมื่อเราทำการ render HTML จากข้อมูลที่ส่งมาจาก database มันมักจะมีความเสี่ยงที่ข้อมูลจะทำให้หน้าเพจ HTML เกิดปัญหา เช่น

``` html
Hello, {{ name }}

--------------

<!-- ถ้าค่าของตัวแปร name คือ -->
<script>alert('hello')</script>

-------------

<!-- เราก็จะ render ได้ -->
Hello, <script>alert('hello')</script>
```

หรือค่าของ name = <b>username ก็จะทำให้หน้า page ทั้งหมดต่อจากตรงนี้เป็น bold ทันที

ดังนั้นโดย default Django จะทำการ escape ค่าของตัวแปรที่เอามา render ใน templage ให้อัตโนมัติ

- `<` is converted to `&lt;`
- `>` is converted to `&gt;`
- `'` (single quote) is converted to `&#x27;`
- `"` (double quote) is converted to `&quot;`
- `&` is converted to `&amp;`

### How to turn it off

เราสามารถปิด auto-escape ได้หลายระดับ ทั้ง per-site, per-template level หรือ per-variable level

#### Variable level

```html
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}

-------

This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```

#### Template block level

```html
Auto-escaping is on by default. Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```

## Accessing method calls

เราสามารถเรียก function ของ instance ที่เราส่งไป render ที่ template ได้ เช่น

```html
{% for comment in task.comment_set.all %}
    {{ comment }}
{% endfor %}

-------

{{ task.comment_set.all.count }}
```

หรือถ้าเรามีการ define method ของ class เอาไว้ เราก็สามารถเรียก method ของ instance ของ class นั้นได้ใน template

```html
<!-- in models.py -->
class Task(models.Model):
    def foo(self):
        return "bar"

-------

<!-- in template.html -->
{{ task.foo }}
```

**หมายเหตุ: แต่เราจะไม่สามารถส่ง argument เข้า function ได้นะครับใน template**

## Custom tag and filter libraries

เราสามารถสร้าง customer tag และ filter ได้เอง ละก็มีคนอื่นที่เขาทำ libraries ของ third-party custom tags and filters มาให้ใช้งานด้วยเช่น `humanize`

วิธีติดตั้ง `humanize`:

1. pip install humanize
2. เพิ่ม 'django.contrib.humanize' ใน INSTALLED_APPS ในไฟล์ settings

เช่น

```html
{% load humanize %}

{{ 45000|intcomma }}
```
