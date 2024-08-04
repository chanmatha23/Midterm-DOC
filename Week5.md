# Week-5

ค้นหาข้อมูล `Payment` โดยให้เพิ่ม field ราคาที่ลบกับส่วนลดแล้ว โดยกำหนดให้ชื่อ field ว่า "after_discount_price" โดยใช้แสดงข้อมูล 10 ตัวแรกเรียงตาม "after_discount_price" จากมากไปน้อย 

```python
val = Payment.objects.annotate(
    after_discount_price=F('price') - F('discount')
).order_by('-after_discount_price')[:10]

for obj in val:
    print(f"ID: {obj.id}, PRICE: {obj.price}, DISCOUNT: {obj.discount}, AFTER DISCOUNT: {obj.after_discount_price}")

```

จากนั้น filter เฉพาะข้อมูล `Payment` ที่มี "after_discount_price" มากกว่า 500,000

```python
total = Payment.objects.annotate(
		after_discount_price= F('price') - F('discount')
).filter(after_discount_price__gt=500000).order_by(F('after_discount_price').asc())[:10]

for payment in total:
    print(
    f"ID: {payment.id}, PRICE: {payment.price},"
    f"DISCOUNT: {payment.discount}, AFTER_DISCOUNT: {payment.after_discount_price}"
)
```

เรียงลำดับข้อมูลลูกค้า (`Customer`) โดยเรียงลำดับตามลำดับตัวอักษร `น้อยไปมาก` จากชื่อเต็มของลูกค้า (`full_name`) โดยแสดง 5 คนแรก (0.5 คะแนน)

**Hint:** Field `full_name` นั้นจะต้องถูก annotate ขึ้นมาโดยการนำ `first_name` มาต่อกับ `last_name` โดยใช้ `Concat(*expressions, **extra)`

**Hint:** แปลง object เป็น dict ใช้ `values()` [doc](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#values)

```python
>>> Blog.objects.filter(name__startswith="Beatles").values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

**Hint:** อยาก print dictionary สวยๆ ใช้ `json.dumps`

```python
print(json.dumps(dictionary, indent=4, sort_keys=False))
```

# Concat:

```python
import json
from django.db.models import Value, Q
from django.db.models.functions import Concat

customer = Customer.objects.annotate(
    full_name=Concat("first_name", Value(' '), "last_name")
).order_by("full_name")[:5]

print(json.dumps(list(customer.values("id", "email", "address", "full_name")), indent=4, sort_keys=False))
```

## **aggregation - count(), sum(), AVG()**

ให้นักศึกษาหาค่าเฉลี่ยของราคาสินค้า (`Product.price`) ที่มีจำนวนคงเหลือ (`Product.remaining_amount`) มากกว่า 0 (0.25 คะแนน)

```python
from django.db.models import Avg
from shop.models import Product

average_price = Product.objects.filter(remaining_amount__gt=0).aggregate(avg=Avg('price'))

print(average_price)

```

จงหาผลรวมราคา (`CartItem.product.price`) ที่อยู่ในตระกร้าสินค้าของเดือน `พฤษภาคม` (ดูจาก `Cart.create_date`) 

```python
from django.db.models import Sum, F
from shop.models import CartItem

total_price = CartItem.objects.filter(
    cart__create_date__month=5
).aggregate(sum=Sum(F('product__price')))

print(total_price)

```

ให้นักศึกษานับจำนวนสินค้าที่อยู่ประเภท `Electronics`, `Jewelry` และ ราคาของสินค้าอยู่ในช่วง 8,000.00 - 50,000.00

```python
from django.db.models import Count, Q
from shop.models import Product
price_range = (8000.00, 50000.00)

product_counts = Product.objects.filter(
    Q(categories__name__in=["Electronics", "Jewelry"]) & 
    Q(price__range=price_range)
).values('categories__name').annotate(count=Count('id'))

for product_count in product_counts:
    category_name = product_count['categories__name']
    count = product_count['count']
    print(f"PRODUCT CATEGORY NAME: {category_name}, PRODUCT COUNT: {count}")

```

# **many-to-many**

ให้นักศึกษาค้นหาข้อมูลสินค้า (`Product`) ที่อยู่ในประเภทสินค้า "Information Technology" 10 รายการแรก (เรียงลำดับด้วย `Product.id`) และแสดงชื่อประเภทสินค้า (`ProductCategory`) (0.25 คะแนน)

5.1 ให้นักศึกษาค้นหาข้อมูลสินค้า (`Product`) ที่อยู่ในประเภทสินค้า "Information Technology" 10 รายการแรก (เรียงลำดับด้วย `Product.id`) และแสดงชื่อประเภทสินค้า (`ProductCategory`) (0.25 คะแนน)

ตัวอย่าง Output บางส่วน

```python
from shop.models import Product

products = Product.objects.filter(categories__name="Information Technology").order_by('id')[:10]

for product in products:
    name = (', ').join([i.name for i in product.categories.all()])
    print(f"PRODUCT ID: {product.id}, PRODUCT NAME: {product.name}, PRODUCT CATEGORY: {name}")
```

```python
from shop.models import Product

# กรองสินค้าที่อยู่ในหมวดหมู่ "Information Technology" และเรียงตาม id, แสดงเพียง 10 รายการแรก
products = Product.objects.filter(categories__name="Information Technology").order_by('id')[:10]

# ลูปผ่านสินค้าที่กรองได้
for product in products:
    # ดึงหมวดหมู่ทั้งหมดของสินค้านั้นๆ
    categories = product.categories.all()
    
    # สร้างลิสต์ของชื่อหมวดหมู่
    category_names = [category.name for category in categories]
    
    # รวมชื่อหมวดหมู่เป็นสตริงเดียว โดยใช้คอมมาและช่องว่างคั่น
    name = ', '.join(category_names)
    
    # แสดงผลข้อมูลสินค้า
    print(f"PRODUCT ID: {product.id}, PRODUCT NAME: {product.name}, PRODUCT CATEGORY: {name}")

```

```python
total = Payment.objects.annotate(after_discount_price= 
		F('price') - F('discount')
).filter(after_discount_price__gt=500000).order_by(
		F('after_discount_price').asc())[:10]

for payment in total:
    print(
        f"ID: {payment.id}, PRICE: {payment.price}, "
        f"DISCOUNT: {payment.discount}, AFTER_DISCOUNT: {payment.after_discount_price}"
    )
```

5.2 ให้นักศึกษาทำตามขั้นตอนดังนี้ (0.25 คะแนน)

**หมายเหตุ: ถ้าใช้ DB จาก WEEK4 `Books and Media` อาจจะถูกเปลี่ยนเป็น `Books` แล้ว**

```
1. เปลี่ยนชื่อประเภทสินค้า `Books and Media` เป็น `Books and Toys`
2. ลบประเภท `Toys and Games` ออกโดยให้ใช้เป็น `Books and Toys` แทน
3. ค้นหาว่าสินค้าที่มีประเภทสินค้าเป็น `Books and Toys` ทั้งหมดมีจำนวนเท่าไหร่
```

```python
ProductCategory.objects.filter(name='Books').update(name = 'Books and Media')

toys_and_games = ProductCategory.objects.get(name='Toys and Games')
books_and_toys = ProductCategory.objects.get(name='Books and Media')

product_toys_and_games = Product.objects.filter(categories=toys_and_games)

for product in product_toys_and_games:
    product.categories.add(books_and_toys)
    product.categories.remove(toys_and_games) 

count = Product.objects.filter(categories=books_and_toys).count()

print(count)

toys_and_games.delete()

```
