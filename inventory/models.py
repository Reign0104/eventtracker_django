from django.db import models
from django.contrib.auth.models import User

class Prop(models.Model):
    CATEGORY_CHOICES = [
        ('Lights', 'Lights'),
        ('Tables', 'Tables'),
        ('Banners', 'Banners'),
        ('Costumes', 'Costumes'),
        ('Others', 'Others'),
    ]
    CONDITION_CHOICES = [
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Damaged', 'Damaged'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=10, choices=[('Good', 'Good'), ('Fair', 'Fair'), ('Damaged', 'Damaged')])
    storage_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='prop_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class UsageLog(models.Model):
    RETURN_STATUS_CHOICES = [
        ('Returned', 'Returned'),
        ('Damaged', 'Damaged'),
        ('Missing', 'Missing'),
    ]
    prop = models.ForeignKey(Prop, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    date_of_use = models.DateField()
    quantity_used = models.PositiveIntegerField()
    return_status = models.CharField(max_length=10, choices=[('Returned', 'Returned'), ('Damaged', 'Damaged'), ('Missing', 'Missing')])

    def __str__(self):
        return f"{self.event_name} - {self.prop.name}"

class Borrower(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # optional
    phone = models.CharField(max_length=20, blank=True, null=True)  # optional

    def __str__(self):
        return self.name

class PropUse(models.Model):
    prop = models.ForeignKey(Prop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Just an example
    timestamp = models.DateTimeField(auto_now_add=True)
    used_by_name = models.CharField(max_length=255)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # The user who used it
    borrower = models.ForeignKey(Borrower, on_delete=models.SET_NULL, null=True, blank=True)  # Optional borrower
    used_at = models.DateTimeField(auto_now_add=True)