

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import date, timezone  # Import date for generating token
import uuid



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='menu_images/',  null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
  # <--- New field

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
    
    
from django.db import models
from django.contrib.auth.models import User
from account.models import Profile

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    token_number = models.CharField(max_length=20, unique=True)
    is_completed = models.BooleanField(default=False)

    def generate_token(self):
        from datetime import date
        import random
        today = date.today()
        return f"{self.user.id}{today.strftime('%d%m%y')}{random.randint(1000, 9999)}"

    def save(self, *args, **kwargs):
        if not self.token_number:
            self.token_number = self.generate_token()

        # Ensure Profile exists for the user, and fetch mobile number
        try:
            profile = Profile.objects.get(user=self.user)
            self.name = self.user.first_name or self.user.username  # Use user's first name or username
            self.mobile = profile.mobile if profile.mobile else ""  # If profile has no mobile, use empty string
        except Profile.DoesNotExist:
            self.name = self.user.username  # If no profile exists, use the username as name
            self.mobile = ""  # Set mobile to empty if no profile is found

        # Call the parent save method to save the order
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.token_number} by {self.name} ({self.mobile})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.token_number} - {self.item.name}"
    


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.item.name}"


# ⚡ NEW: Quick Order Items
class QuickOrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} ⚡ {self.item.name}"