
# Filter
## django.contrib.humanize
ต้องเพิ่ม `django.contrib.humanize` ใน install ก่อน 

> อย่าลืม {% load humanize %} 

### `apnumber`

For numbers 1-9, returns the number spelled out. Otherwise, returns the number. This follows Associated Press style.

Examples:

-   `1`  becomes  `one`.
-   `2`  becomes  `two`.
-   `10`  becomes  `10`.

You can pass in either an integer or a string representation of an integer.

### `intcomma`
Examples:

-   `4500`  becomes  `4,500`.

### `intword`
Examples:

-   `1000000`  becomes  `1.0  million`.
-   `1200000`  becomes  `1.2  million`.

### `naturalday`

For dates that are the current day or within one day, return “today”, “tomorrow” or “yesterday”, as appropriate. Otherwise, format the date using the passed in format string.
Examples (when ‘today’ is 17 Feb 2007):

-   `16  Feb  2007`  becomes  `yesterday`.
-   `17  Feb  2007`  becomes  `today`.
-   `18  Feb  2007`  becomes  `tomorrow`.

### `naturaltime`
Examples (when ‘now’ is 17 Feb 2007 16:30:00):

-   `17  Feb  2007  16:30:00`  becomes  `now`.
-   `17  Feb  2007  16:29:31`  becomes  `29  seconds  ago`.

### `ordinal`
Examples:
-   `1`  becomes  `1st`.
-   `2`  becomes  `2nd`.
-   `3`  becomes  `3rd`.

### `date` 
>  ใช้ในการจัดรูปแบบวันที่

    {{ some_date|date:"F j, Y" }}  <!-- August 24, 2024 -->` 
    

### `time`
> ใช้ในการจัดรูปแบบเวลา

    {{ some_time|time:"H:i" }}  <!-- 14:30 -->
    

### `default`

> ใช้ในการให้ค่าเริ่มต้นหากตัวแปรเป็น `None` หรือว่าง

       {{ some_var|default:"default_value" }}
    

### `length`

> - ใช้ในการนับจำนวนรายการในลิสต์หรือจำนวนตัวอักษรในสตริง

    {{ some_list|length }}  <!-- จำนวนสมาชิกใน some_list -->

### `truncatewords`

> ตัดคำให้อยู่ในจำนวนที่กำหนดและเพิ่มข้อความ “...” ที่ท้าย

    {{ some_text|truncatewords:10 }}
## Others
### `divisibleby`

> ใช้เพื่อตรวจสอบว่าค่าของตัวแปรสามารถหารด้วยจำนวนที่กำหนดแล้วลงตัวหรือไม่โดยไม่เหลือเศษ

    {% if value|divisibleby:"3" %}
        {{ value }} is divisible by 3.
    {% else %}
        {{ value }} is not divisible by 3.
    {% endif %}

ในตัวอย่างนี้ ถ้า `value` สามารถหารด้วย 3 ลงตัว (เช่น 3, 6, 9 เป็นต้น) ส่วนที่อยู่ใน `{% if %}` จะถูกแสดงผลว่า "9 is divisible by 3." หากไม่สามารถหารลงตัวได้ ก็จะแสดงส่วนที่อยู่ใน `{% else %}`


### `add`
It is used to add an argument to the value.  **Example**

    {{ value | add:"2" }}
### `addslashes`
It is used to add slashes before quotes. Useful for escaping strings in CSV.  **Example**

    {{ value | addslashes }}

If value is “I’m Jai”, the output will be “I\’m Jai”.
### `capfirst`
ถ้า Value คือ "hello world"

	{% load humanize %}
    
    {{ text|capfirst }} 
    
    ในกรณีนี้ ผลลัพธ์ที่ได้จะเป็น:
    
    `Hello world`

### `cut`

It is used to remove all values of arg from the given string.  **Example**

    {{ value | cut:" " }}

If value is “String with spaces”, the output will be “Stringwithspaces”.

### `dictsort`

It takes a list of dictionaries and returns that list sorted by the key given in the argument.  **Example**

    {{ value | dictsort:"name" }}

If value is:

    [
        {'name': 'zed', 'age': 19},
        {'name': 'amy', 'age': 22},
        {'name': 'joe', 'age': 31},
    ]

then the output would be:

    [
        {'name': 'zed', 'age': 19},
        {'name': 'amy', 'age': 22},
        {'name': 'joe', 'age': 31},
    ]
### `join`

It is used to join a list with a string, like Python’s str.join(list)  **Example**

    {{ value | join:" // " }}

If value is the list [‘a’, ‘b’, ‘c’], the output will be the string “a // b // c”.

#### linenumbers
It is used to display text with line numbers.  **Example**

    {{ value | linenumbers }}
