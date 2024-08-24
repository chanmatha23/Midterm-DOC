## **Instruction**

1. สร้าง `virtual environment`
2. ติดตั้ง `django` และ `psycopg2` libraries
3. สร้างโปรเจคใหม่ใหม่ชื่อ`myshop`
4. จากนั้นให้ทำการ startapp ใหม่ชื่อ `shop`
5. สร้าง database ชื่อ `shop` ใน Postgres DB
6. ทำการเพิ่ม code ด้านล่างนี้ในไฟล์ `shop/models.py`
7. เพิ่ม **'shop'** ใน `settings.py`
8. ทำการ `makemigrations` และ `migrate`

query หาข้อมูล `Order` ทั้งหมดที่เกิดขึ้นในเดือน `พฤษภาคม` มาแสดงผล 10 รายการแรก

```python
from shop.models import Order
ord = Order.objects.filter(order_date__month=5)[:10]
for obj in ord:
   print(f"ORDER ID:{obj.id}, DATE: {obj.order_date}, PRICE: {obj.payment.price}")
```

## contains , icontains

- `__icontains`, `__istartswith`, `__iendswith`: ไม่คำนึงถึงตัวพิมพ์ใหญ่-เล็ก
- `__contains`, , `__endswith`: คำนึงถึงตัวพิมพ์ใหญ่-เล็ก

query หาข้อมูล `Product` ที่มีคำลงท้ายว่า `features.` ในรายละเอียดสินค้า และแสดงผลดังตัวอย่าง

```python
from shop.models import Product

#ลงท้ายด้วย features.
products_with_features = Product.objects.filter(description__endswith='features.')
for product in products_with_features:
    print(f"PRODUCT ID: {product.id}, DESCRIPTION: {product.description}")
```

query หาข้อมูล `Product` ที่มีราคาสินค้าตั้งแต่ `5000.00` ขึ้นไป และอยู่ในหมวดหมู่ `Information Technology` และแสดงผล

```python
from shop.models import Product, ProductCategory

products_it = Product.objects.filter(
    Q(price__gte=5000.00) & Q(categories__name='Information Technology')
)

for product in products_it:
    print(f"PRODUCT ID: {product.id}, NAME: {product.name}, PRICE: {product.price:.2f}")
```

## Gt, Lt

query หาข้อมูล `Product` ที่มีราคาสินค้าน้อยกว่า `200.00` และมากกว่า `100.00`

```python
from shop.models import Product

products = Product.objects.filter(price__gt=100.00, price__lt=200.00)
for product in products:
    print(f"PRODUCT ID: {product.id}, NAME: {product.name}, PRICE: {product.price:.2f}")
```

## Range

```python
from shop.models import Product

products = Product.objects.filter(price__range=(101,199))

for product in products:
    print(f"PRODUCT ID: {product.id}, NAME: {product.name}, PRICE: {product.price:.2f}")
```

## Date

```python
from shop.models import Order

# หาปที่ 2024
orders_at_2024 = Order.objects.filter(order_date__year=2024)
# หาปีที่ > 2024
orders_from_2024 = Order.objects.filter(order_date__year__gt=2024)

for order in orders_at_2024:
    print(f"ORDER ID: {order.id}, DATE: {order.order_date}, YEAR: {order.order_date.year}")

```

## Between Date

```python
from shop.models import Order
orders_in_2005 = Order.objects.filter(order_date__range=('2005-01-01', '2005-12-31'))

for order in orders_in_2005:
    print(f"ORDER ID: {order.id}, DATE: {order.order_date}")

```

# **เพิ่ม ลบ แก้ไข สินค้า**

ให้เพิ่มสินค้าใหม่จำนวน 3 รายการ (0.5 คะแนน)

```
สินค้าที่ 1
ชื่อ: Philosopher's Stone (1997)
หมวดหมู่สินค้า: Books and Media
จำนวนคงเหลือ: 20
รายละเอียดซ: By J. K. Rowling.
ราคา: 790

สินค้าที่ 2
ชื่อ: Me Before You
หมวดหมู่สินค้า: Books and Media
จำนวนคงเหลือ: 40
รายละเอียดซ: A romance novel written by Jojo
ราคา: 390

สินค้าที่ 3
ชื่อ: Notebook HP Pavilion Silver
หมวดหมู่สินค้า: Information Technology และ Electronics
จำนวนคงเหลือ: 10
รายละเอียดซ: Display Screen. 16.0
ราคา: 20000
```

```python
from shop.models import Product, ProductCategory

books_and_media = ProductCategory.objects.get(name='Books')
it = ProductCategory.objects.get(name='Information Technology')
electronics = ProductCategory.objects.get(name='Electronics')

product1 = Product.objects.create(
    name="Philosopher's Stone (1997)",
    description="By J. K. Rowling.",
    remaining_amount=20,
    price=790
)
product1.categories.add(books_and_media)

product2 = Product.objects.create(
    name="Me Before You",
    description="A romance novel written by Jojo",
    remaining_amount=40,
    price=390
)
product2.categories.add(books_and_media)

product3 = Product.objects.create(
    name="Notebook HP Pavilion Silver",
    description="Display Screen. 16.0",
    remaining_amount=10,
    price=20000
)
product3.categories.add(it, electronics)

```

แก้ไขชื่อสินค้า จาก `Philosopher's Stone (1997)` เป็น `Half-Blood Prince (2005)`

```python
from shop.models import Product
Product.objects.filter(name="Philosopher's Stone (1997)").update(name="Half-Blood Prince (2007)")
```

แก้ไขชื่อหมวดหมู่สินค้า จาก `Books and Media` เป็น `Books`

```python
from shop.models import ProductCategory
ProductCategory.objects.filter(name="Books").update(name="New_name")

```

 ลบสินค้าทุกตัวที่อยู่ในหมวดหมู่ `Books`

```python
from shop.models import Product, ProductCategory

books_category = ProductCategory.objects.get(name="Books")
Product.objects.filter(categories=books_category).delete()

```

# Filters can reference fields on the model

ในกรณีที่เราต้องการเปรียบเทียบค่าของ field ใน model กับ field อื่นใน model เดียวกัน เราสามารถใช้ **F expressions** ได้ `F()`

```python
from django.db.models import F
Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))
Entry.objects.filter(authors__name=F("blog__name")) # span relationships

```

โดย Django นั้น support การใช้ +, -, *, / ร่วมกับ `F()` ด้วย เช่น

```python
Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks") * 2)
Entry.objects.filter(rating__lt=F("number_of_comments") + F("number_of_pingbacks"))

```

## Complex lookups with Q objects

Keyword argument ที่ส่งเข้าไปใน method `filter()` ทุกตัวจะถูกเอามา generate เป็น `SELECT ... WHERE ... AND ...` เสมอ เช่น

โดยปกติถ้าเราใช้ `,` ขั้นระหว่าง filter condition จะเป็นการ AND กัน

```sql
-- Entry.objects.filter(headline__contains='Lennon', pub_date__year=2005)
SELECT * FROM entry WHERE headline LIKE '%Lennon%' AND pub_date BETWEEN '2005-01-01' AND '2005-12-31';

```

ในกรณีที่เราต้องการทำการ query ที่ซับซ้อน อาจจะต้องการใช้ `OR` หรือ `NOT` ร่วมด้วย เราจะต้องใช้ `Q objects`

กรณี OR

```python
Entry.objects.filter(Q(headline__startswith="Who") | Q(headline__startswith="What"))
# SELECT ... WHERE headline LIKE 'Who%' OR headline LIKE 'What%'
```

กรณี NOT

```python
Entry.objects.filter(Q(headline__startswith="Who") | ~Q(pub_date__year=2005))
# SELECT ... WHERE headline LIKE 'Who%' OR pub_date NOT BETWEEN '2005-01-01' AND '2005-12-31';

```

กรณี nested conditions

```python
Poll.objects.get(
    Q(question__startswith="Who"),
    (Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))),
)

```

แปลงเป็น SQL

```sql
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

```
