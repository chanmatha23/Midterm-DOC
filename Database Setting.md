
**ทำการติดตั้ง Postgres Client  `psycopg2`**
ติดตั้ง PostgreSQL - [POSTGRES DOWNLOAD](https://www.postgresql.org/download/)

    pip install psycopg2
    Or
    pip install psycopg2-binary
    Or
    brew install postgresql # for MacOS
จากนั้นไปทำการแก้ไขใน setting

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "mypolls",
            "USER": "db_username",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

 **สร้าง migration**

    python manage.py makemigrations

**ยืนยันการ migration**

    python manage.py migrate

**ตัวอย่างการ add models**

    from django.db import models
    
    # Create your models here.
    
    class Customer(models.Model):
        first_name = models.CharField(max_length=150)
        last_name = models.CharField(max_length=200)
        email = models.CharField(max_length=150)
        address = models.JSONField(null=True)
    
    class ProductCategory(models.Model):
        name = models.CharField(max_length=150)
    
    class Product(models.Model):
        name = models.CharField(max_length=150)
        description = models.TextField(null=True, blank=True)
        remaining_amount = models.PositiveIntegerField(default=0)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        categories = models.ManyToManyField(ProductCategory)
    
    class Cart(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
        create_date = models.DateTimeField()
        expired_in = models.PositiveIntegerField(default=60)
        
    class CartItem(models.Model):
        cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        amount = models.PositiveIntegerField(default=1)
        
    class Order(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
        order_date = models.DateField()
        remark = models.TextField(null=True, blank=True)
    
    class OrderItem(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        amount = models.PositiveIntegerField(default=1)
        
    class Payment(models.Model):
        order = models.OneToOneField(Order, on_delete=models.PROTECT)
        payment_date = models.DateField()
        remark = models.TextField(null=True, blank=True)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class PaymentItem(models.Model):
        payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
        order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        
    class PaymentMethod(models.Model):
        class MethodChoices(models.Choices):
            QR = "QR"
            CREDIT = "CREDIT"
        
       payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
       method = models.CharField(max_length=15, choices=MethodChoices.choices)
       price = models.DecimalField(max_digits=10, decimal_places=2)
