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
