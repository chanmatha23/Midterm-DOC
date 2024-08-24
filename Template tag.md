# Built-in template tags and filters

## Built-in tag reference

[Ref](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#built-in-tag-reference)

- **autoescape** สำหรับเอาไว้ เปิด - ปิด auto escape

```html
{% autoescape on %}
    {{ body }}
{% endautoescape %}
```

- **block**

- **comment**

```html
<p>Rendered text with {{ pub_date|date:"c" }}</p>
{% comment "Optional note" %}
    <p>Commented out text with {{ create_date|date:"c" }}</p>
{% endcomment %}
```

- **csrf_token**

- **cycle**

```html
{% for o in some_list %}
    <tr class="{% cycle 'row1' 'row2' %}">
        ...
    </tr>
{% endfor %}
```

- **extends**

- **for**

```html
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>

<!-- if "data" is a dictionary -->
{% for key, value in data.items %}
    {{ key }}: {{ value }}
{% endfor %}
```

| Variable              | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| `forloop.counter`     | The current iteration of the loop (1-indexed)                  |
| `forloop.counter0`    | The current iteration of the loop (0-indexed)                  |
| `forloop.revcounter`  | The number of iterations from the end of the loop (1-indexed)  |
| `forloop.revcounter0` | The number of iterations from the end of the loop (0-indexed)  |
| `forloop.first`       | True if this is the first time through the loop                |
| `forloop.last`        | True if this is the last time through the loop                 |
| `forloop.parentloop`  | For nested loops, this is the loop surrounding the current one |

ตัวอย่างการใช้งาน

```html
<ul>
{% for athlete in athlete_list %}
    <li>{{forloop.counter}}. {{ athlete.name }}</li>
{% endfor %}
</ul>
```

- **for ... empty**

```html
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% empty %}
    <li>Sorry, no athletes in this list.</li>
{% endfor %}
</ul>
```

- **if**

```html
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

ใน condition ของ if เราสามารถใส่ and, or หรือ not ได้ เช่น

```html
{% if athlete_list and coach_list %}
    Both athletes and coaches are available.
{% endif %}

{% if not athlete_list %}
    There are no athletes.
{% endif %}

{% if athlete_list or coach_list %}
    There are some athletes or some coaches.
{% endif %}

{% if not athlete_list or coach_list %}
    There are no athletes or there are some coaches.
{% endif %}
```

และสามารถใช้ logic operations ต่างๆได้ ได้แก่

- `==`, `!=`

```html
{% if somevar != "x" %}
  This appears if variable somevar does not equal the string "x",
  or if somevar is not found in the context
{% endif %}
```

- `>`, `>=`, `<`, `<=`

```html
{% if somevar <= 100 %}
  This appears if variable somevar is less than 100 or equal to 100.
{% endif %}
```

- `in`, `not in`

```html
{% if user in users %}
  If users is a QuerySet, this will appear if user is an
  instance that belongs to the QuerySet.
{% endif %}
```

- `is`, `is not`

```html
{% if somevar is True %}
  This appears if somevar is not True, or if somevar is not found in the
  context.
{% endif %}

{% if somevar is not None %}
  This appears if and only if somevar is not None.
{% endif %}
```

- **now**

```html
It is {% now "jS F Y H:i" %}
```

- **url**

```html
{% url 'some-url-name' v1 v2 %}
```

ตัวอย่างเช่น

```python
path("client/<int:id>/", app_views.client, name="app-views-client")
```

ใน template จะใช้ tag **url** ดังนี้

```html
{% url 'app-views-client' client.id %}
```

## Built-in filter reference

[Ref](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#built-in-filter-reference)

- **add**

```html
{{ value|add:"2" }}
```

- **addslashes**

```html
{{ value|addslashes }}
```

- **capfirst**

- **cut**

```html
{{ value|cut:" " }}
```

ถ้าค่าของ `value` คือ "String with spaces" จะได้ output เป็น "Stringwithspaces"

**date** - ใช้ในการ format ข้อมูล datetime [Ref](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#date)

```html
{{ value|date:"D d M Y" }} {{ value|time:"H:i" }}
```

- **default**

```html
{{ value|default:"nothing" }}
```

ถ้าค่าของ `value` แปลงเป็น boolean ได้เป็น False จะแสดงค่า "nothing"

- **default_if_none**

```html
{{ value|default_if_none:"nothing" }}
```

ถ้าค่าของ `value` เป็น None จะแสดงค่า "nothing"

- **dictsort**

```html
{{ value|dictsort:"name" }}

<!-- ถ้าค่าของ value เป็น -->
[
    {"name": "zed", "age": 19},
    {"name": "amy", "age": 22},
    {"name": "joe", "age": 31},
]

<!-- จะได้ output -->
[
    {"name": "amy", "age": 22},
    {"name": "joe", "age": 31},
    {"name": "zed", "age": 19},
]
```

- **divisibleby**

```html
{{ value|divisibleby:"3" }}
```

- **join**

```html
{{ value|join:" // " }}
```

- **length**

```html
{{ value|length }}
```

- **time**

```html
{{ value|time:"TIME_FORMAT" }}
```

- **timesince**

```html
{{ blog_date|timesince:comment_date }}
```

แสดงเวลาจากค่าตัวแปร (`blog_date`) จนถึงเวลา `now` (เช่น “4 days, 6 hours”)

รับ optional argument เป็นเวลาที่ต้องการเปรียบเทียบแทนค่า `now`

- **timeuntil**

```html
{{ conference_date|timeuntil:from_date }}
```

คล้ายกับ "timesince" แต่จะวัดเวลาจาก `now` ไปจนถึงค่าตัวแปรซึ่งเป็นวันในอนาคต (`conference_date`)

รับ optional argument เป็นเวลาที่ต้องการเปรียบเทียบแทนค่า `now`

- **truncatechars**

```html
{{ value|truncatechars:7 }}
```

ถ้ายาวเกินค่าที่กำหนดจะถูกแทนด้วย "..."

- **urlencode**

```html
{{ value|urlencode }}
```

If value is "https://www.example.org/foo?a=b&c=d", the output will be "https%3A//www.example.org/foo%3Fa%3Db%26c%3Dd".
