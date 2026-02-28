from django.db import models
from django.contrib.auth.models import User
import uuid

# 1. CATEGORIES
class Category(models.Model):
    name = models.CharField(max_length=50)
    theme_color = models.CharField(max_length=20, default="green")
    def __str__(self): return self.name

# 2. SUB-CATEGORIES
class SubCategory(models.Model):
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self): return f"{self.parent_category.name} - {self.name}"

# 3. EVENTS
class Event(models.Model):
    title = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory, related_name='events', on_delete=models.CASCADE)
    event_date = models.DateTimeField(null=True, blank=True) # 👈 Added for you
    venue = models.CharField(max_length=100)
    entry_fee = models.IntegerField()
    winning_prize = models.CharField(max_length=100, default="TBA")
    team_size = models.CharField(max_length=20, default="5v5")
    description = models.TextField(blank=True, default="No description added.")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    STATUS_CHOICES = [('LIVE', 'Live'), ('OPEN', 'Open'), ('FAST', 'Filling Fast'), ('CLOSED', 'Closed')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    def __str__(self): return self.title

# 4. REGISTRATIONS
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    PAYMENT_CHOICES = [('UPI', 'UPI Online'), ('VENUE', 'Pay at Venue')]
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)
    pass_id = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pass_id:
            self.pass_id = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.player_name} - {self.event.title}"

# 5. MATCHES
class Match(models.Model):
    event = models.ForeignKey(Event, related_name='matches', on_delete=models.CASCADE)
    player_1 = models.ForeignKey(Registration, related_name='matches_as_p1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Registration, related_name='matches_as_p2', on_delete=models.CASCADE)
    round_name = models.CharField(max_length=50, default="Round 1")
    winner = models.ForeignKey(Registration, related_name='won_matches', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self): return f"{self.player_1.player_name} vs {self.player_2.player_name}"