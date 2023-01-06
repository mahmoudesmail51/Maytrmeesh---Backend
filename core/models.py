from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin
from django.conf import settings
from django.db.models.expressions import F
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#Automatically generates auth-token for users saved in the system
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    """ Manager for users"""
    def create_user(self,email,password):
        """ creates a new user"""

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self,email,password):
        """ Creates a super user"""
        user = self.create_user(email,password)

        user.is_staff= True
        user.is_superuser = True
        user.save(using= self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """ Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """ returns string representation of object"""
        return self.email


class CustomerManager(models.Manager):
    """ Manager for Customer"""
    def create_customer(self, user, first_name, last_name, date_of_birth, phone_number):
        """ Creates new customer"""
        customer = self.model(user = user, first_name=first_name, last_name=last_name,
                            date_of_birth=date_of_birth, phone_number= phone_number)
        customer.save(using=self._db)
        return customer

class Customer(models.Model):
    """ Database model for customers"""
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11)

    objects = CustomerManager()

    def __str__(self):
        return self.first_name +" "+ self.last_name

class FoodVenueManager(models.Manager):
    """ return objects with location x"""
    def get_venues(self,location):
        return FoodVenue.objects.filter(location = location)
    
    def create_venue(self, owner, name, location, image, bank_account_number):
        food_venue = self.model(owner= owner, name= name, location= location, image= image, bank_account_number = bank_account_number)
        food_venue.save(using = self._db)
        return food_venue
    
    def is_exist(self,id):
        venues = FoodVenue.objects.all()
        for venue in venues:
            if venue.id == int(id):
                return True
        return False

class FoodVenue(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.TextField()
    bank_account_number = models.CharField(max_length=255)
    objects = FoodVenueManager()

    def __str__(self):

        """ returns string representation of object"""
        return self.name + "-" + self.location

class ReviewManager(models.Manager):
    """ Adds a new review"""
    def add_review(self, comment, rating, customer, food_venue):
        review = self.model(comment = comment, rating = rating, customer = customer, food_venue = food_venue)
        review.save(using = self.db)
        return review
        
class Review(models.Model):
    comment = models.TextField(max_length=255)
    rating = models.DecimalField(max_length=10, max_digits=10 , decimal_places= 1)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    food_venue = models.ForeignKey(FoodVenue, on_delete= models.CASCADE)
    objects = ReviewManager()


class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.TextField()

    BAKERY = 'Bakery'
    PASTRY = 'Pastry'
    DESERTS = 'Deserts'
    SUSHI = 'Sushi'
    DRINKS = 'Beverages'
    OT = 'Others'

    category_types = [
        (BAKERY,'Bakery'),
        (PASTRY,'Pastry'),
        (DESERTS,'Deserts'),
        (SUSHI,'Sushi'),
        (DRINKS,'Beverages'),
        (OT,'Others'),
    ]
    category = models.CharField(choices=category_types,max_length=15)
    description = models.TextField(max_length=255,default="")
    original_price = models.DecimalField(max_length=10 ,max_digits=10,decimal_places=2)
    is_served = models.BooleanField(default=False)
    food_venues = models.ManyToManyField(FoodVenue)
    favorite_by = models.ManyToManyField(Customer,blank=True)
    def __str__(self):

        """ returns string representation of object"""
        return self.name

class PackageManager(models.Manager):
    
    def add_package(self,name, image, description, food_venue,items, price):
        """ """
        package = self.model(name = name, image= image, description = description, food_venue= food_venue, price = price)
        package.save(using = self._db)
        for item in items:
            package.items.add(item)
        package.save(using = self._db)
        
        return package


class Package(models.Model):
    name = models.CharField(max_length=255)
    image = models.TextField(blank=True)
    description = models.TextField(max_length=255,default="")
    food_venue = models.ForeignKey(FoodVenue, on_delete= models.CASCADE)
    is_served = models.BooleanField(default=False)
    items = models.ManyToManyField(Item)
    favorite_by = models.ManyToManyField(Customer,blank=True)
    price = models.DecimalField(max_length=10 ,max_digits=10,decimal_places=2)
    objects = PackageManager()
    def __str__(self):
        """ returns string representation of object"""
        return self.name

class available_item_manager(models.Manager):
    """manager for available items"""
    def add_item(self, item, food_venue,quantity, discount, price, availablity_time):
        item = self.model( item = item, food_venue = food_venue, quantity= quantity, discount = discount, price = price,availablity_time = availablity_time)
        item.save(using = self._db)
        return item


class available_item(models.Model):
    class Meta:
        unique_together = (('food_venue','item'),)
    food_venue = models.ForeignKey(FoodVenue, on_delete= models.CASCADE)
    item = models.ForeignKey(Item, on_delete= models.CASCADE)
  
    quantity = models.IntegerField()
    discount = models.IntegerField()
    price = models.DecimalField(max_length=10 , max_digits=10, decimal_places=2)
    availablity_time = models.IntegerField()
    objects = available_item_manager()
    def __str__(self):
        """ returns string representation of object"""
        return  self.food_venue.name +" "+self.item.name
   

class available_package_manager(models.Manager):
    """Manager for available packages"""

    def add_package(self, food_venue, package, quantity, discount, price, availablity_time):
        package = self.model(package = package, food_venue =food_venue, quantity = quantity, price = price, discount = discount , availablity_time = availablity_time)
        package.save(using = self._db)
        return package



class available_package(models.Model):

    class Meta:
        unique_together = (('food_venue','package'),)

    food_venue = models.ForeignKey(FoodVenue, on_delete= models.CASCADE)
    package = models.ForeignKey(Package, on_delete= models.CASCADE)
    
    quantity = models.IntegerField()
    discount = models.IntegerField()
    price = models.DecimalField(max_length=10 , max_digits=10, decimal_places=2)
    availablity_time = models.IntegerField()
    objects = available_package_manager()
    def __str__(self):
        
        """ returns string representation of object"""
        return  self.food_venue.name +" "+self.package.name

class OrderManager(models.Manager):
    
    def add_order(self,customer, food_venue, is_donated, total, order_time, item, package, order_type, quantity):
        order = self.model(customer = customer, food_venue = food_venue, is_donated = is_donated, total = total, order_time = order_time,item = item, package = package, order_type = order_type, quantity = quantity)
        order.save(using = self._db)
        return order

class Order (models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    food_venue = models.ForeignKey(FoodVenue, on_delete= models.CASCADE)
    is_donated = models.BooleanField(default= False)
    total = models.DecimalField(max_length=10 ,max_digits=10,decimal_places=2)
    order_time = models.DateTimeField(default= None)
    item = models.ForeignKey(Item, on_delete= models.CASCADE, default= None, null=True)
    package = models.ForeignKey(Package, on_delete= models.CASCADE, default= None, null= True)
    order_type = models.TextField()
    quantity = models.IntegerField()

    objects = OrderManager()