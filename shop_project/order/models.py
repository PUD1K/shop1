from django.db import models    
# импортируем чтобы знать, какой юзер в данный момент авторизован
from django.contrib.auth.models import User

# поскольку все продукты связаны с корзиной, чтобы не создавать велосипед просто импортируем эти продукты 
from product.models import Product

# создаем класс заказа
class Order(models.Model):
    # работаем по первичному ключу = юзеру
    user = models.ForeignKey(User, related_name='orders',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    stripe_token  = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return self.first_name

# здесь находится экземпляр продукта корзины
class OrderItem(models.Model):
    # Вытаскиваем конкретный order по первичному ключу
    order = models.ForeignKey(Order, related_name ='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id