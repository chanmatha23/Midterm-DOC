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
