
## ใช้ `Concat` ใน Django ORM

1.  **รวมฟิลด์หลายฟิลด์เป็นฟิลด์เดียวกัน**:
    
ใช้ `Concat` เพื่อรวมฟิลด์ `first_name` และ `last_name` เป็นฟิลด์ `full_name`:

    from django.db.models import Value
    from django.db.models.functions import Conca


**ค้นหาทุกคนและรวมชื่อและนามสกุลเป็นฟิลด์ `full_name`**

    people = Person.objects.annotate(
        full_name=Concat(
            F('first_name'), Value(' '), F('last_name')
        )
    )
    for person in people:
        print(person.full_name)
    
   **ค้นหาทุกคนและรวมข้อความกำหนดเองกับชื่อเต็ม**

    people = Person.objects.annotate(
        greeting=Concat(
            Value('Hello, my name is '), F('first_name'), Value(' '), F('last_name')
        )
    )
    
    for person in people:
        print(person.greeting)` 

 **การใช้งานกับ `filter` และ `order_by`**
คุณยังสามารถใช้ `Concat` ร่วมกับ `filter` และ `order_by`:

    people = Person.objects.annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'))
    ).filter(full_name__startswith='John')

**จัดเรียงตามชื่อเต็ม**
people = people.order_by('full_name')
