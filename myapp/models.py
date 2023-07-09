from django.db import models
from django.utils import timezone

from myapp.tuples import ORDER_STATUSES_CHOICES, ORDER_STATUSES


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name='products')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    completed_dt = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=ORDER_STATUSES.new, choices=ORDER_STATUSES_CHOICES)

    class Meta:
        ordering = ('-created_dt',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.completed_dt:
            self.status = ORDER_STATUSES.complete
        if self.status == ORDER_STATUSES.complete and not self.completed_dt:
            self.completed_dt = timezone.now()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        unique_together = ('order', 'product')

    def __str__(self):
        return self.product.name
