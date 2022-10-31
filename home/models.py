from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10 ,default='Not Available')
    auth_token = models.CharField(max_length=300)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
CITY_CHOICES = (
    ("Indore", "Indore"),
            ("Bhopal", "Bhopal"),
            ("Jabalpur", "Jabalpur"),
            ("Gwalior", "Gwalior"),
            ("Ujjain", "Ujjain"),
            ("Sagar", "Sagar"),
            ("Dewas", "Dewas"),
            ("Satna", "Satna"),
            ("Ratlam", "Ratlam"),
            ("Rewa", "Rewa"),
            ("Katni", "Katni"),
            ("Singrauli", "Singrauli"),
            ("Burhanpur", "Burhanpur"),
            ("Khandwa", "Khandwa"),
            ("Morena", "Morena"),
            ("Bhind", "Bhind"),
            ("Chhindwara", "Chhindwara"),
            ("Guna", "Guna"),
            ("Shivpuri", "Shivpuri"),
            ("Vidisha", "Vidisha"),
            ("Chhatarpur", "Chhatarpur"),
            ("Damoh", "Damoh"),
            ("Mandsaur", "Mandsaur"),
            ("Khargone", "Khargone"),
            ("Neemuch", "Neemuch"),
            ("Pithampur", "Pithampur"),
            ("Hoshangabad", "Hoshangabad"),
            ("Itarsi", "Itarsi"),
            ("Sehore", "Sehore"),
            ("Betul", "Betul"),
            ("Seoni", "Seoni"),
            ("Datia", "Datia"),
            ("Nagda", "Nagda"),
            ("Dhanpuri", "Dhanpuri"),
            ("Dhar", "Dhar"),
            ("Balaghat", "Balaghat"),
)
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,)
    house_no = models.CharField(max_length=100) 
    street = models.CharField(max_length=100)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICES,max_length=100)
    zip_code = models.IntegerField()
    state = models.CharField(default='Madhya Pradesh',max_length=100)
    
    
    def __str__(self):
        return self.name + self.house_no + self.street + self.locality + self.city
    
    
    
GENDER_CHOICES=(
    ('None','None'),
    ('Men','Men'),
    ('Women','Women'),
)
PRODUCT_CHOICES=(
    ('M','Mobile'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('WW','Winter Wear'),
    ('HA','Home Appliances'),
    ('L','Laptop',)
)

        
class Product(models.Model):
    brand = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='media')
    actual_price = models.IntegerField()
    discounted_price = models.IntegerField(default=None)
    category = models.CharField(choices=PRODUCT_CHOICES,max_length=30)
    in_stock = models.PositiveIntegerField()
    gender_category = models.CharField(choices=GENDER_CHOICES,max_length=30,default=None,null=True)
    def save(self, *args, **kwargs):
        self.title =' '.join([ item.capitalize() for item in self.title.split()])
        self.brand = self.brand.capitalize()
        super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.title + self.brand
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title + self.product.brand

STATUS_CHOICES=(
     ('Canceled','Canceled'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('Ready To Ship','Ready To Ship'),
    ('Shipped','Shipped'),
    ('Out For Delivery','Out For Delivery'),
    ('Delivered','Delivered')   
    
)


class PlacedOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=70)
    
    def __str__(self):
        return self.product
    @property
    def total_price(self):
        return self.product.discounted_price*self.quantity