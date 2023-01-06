from django.db.models import fields
from rest_framework import serializers

from core.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
       

class CustomerRegestirationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},write_only= True )
    password2 = serializers.CharField(style={'input_type': 'password'},write_only= True  )
    fullname = serializers.CharField()
    class Meta:
        model = Customer
        fields = ['email','password','password2', 'fullname',  'date_of_birth','phone_number']
        extra_kwargs = {
            'password':{'write_only': True},
            'password2':{'write_only': True}
        }
    
    def save(self):
        """ saves a new user and return it"""
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})  
        email = self.validated_data['email']
        user = User.objects.create_user(email=email, password= password)
        temp = self.validated_data['fullname'].split()
        first_name = temp[0]
        last_name = temp[1]
        date_of_birth = self.validated_data['date_of_birth']
        phone_number = self.validated_data['phone_number']
        user.is_customer = True
        user.save()
        customer = Customer.objects.create_customer(user=user, first_name=first_name, last_name=last_name,date_of_birth=date_of_birth,phone_number=phone_number)

        return customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
       

class FoodVenueSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = FoodVenue
        fields = ['id','manager', 'name', 'location', 'image','bank_account_number']
        extra_kwargs = {
            'manager':{'write_only': True},
            'bank_account_number':{'write_only': True}
        }
    
    def save(self):
        """ saves a new food venue and returns it"""
        manager_id = self.validated_data['manager']
        name = self.validated_data['name']
        location = self.validated_data['location']
        image = self.validated_data['image']
        bank_account_number = self.validated_data['bank_account_number']
        venues = FoodVenue.objects.get_venues(location= location)
        for venue in venues:
            if(venue.name == name and venue.location == location):
                raise serializers.ValidationError ({'venue':'already exist with same name and location'})
        venue = FoodVenue.objects.create_venue(manager= manager_id, name= name, location= location, image= image, bank_account_number= bank_account_number)
        return venue


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['comment','rating','customer','food_venue']

    def save(self):
        comment = self.validated_data['comment']
        rating = self.validated_data['rating']
        customer = self.validated_data['customer']
        food_venue = self.validated_data['food_venue']
        if(rating <= 5 and rating >= 0):
            review = Review.objects.add_review(comment=comment, rating= rating, customer = customer, food_venue= food_venue)
            return review
        else:
            raise serializers.ValidationError({'rating':'rating should be between 0 and 5'})


class ItemSerializer(serializers.ModelSerializer):
    food_venues = FoodVenueSerializer(many = True,write_only = True)
    class Meta:
        model = Item
        fields = ['id','name','description','image','category','original_price','food_venues','favorite_by']
        extra_kwargs = {
            'favorite_by':{'write_only': True}
          
        }
        
        



class PackageSerializer(serializers.ModelSerializer):
    food_venue = FoodVenueSerializer(write_only = True)
    items = ItemSerializer(many = True)
    class Meta:
        model = Package
        fields =['id', 'name', 'image','description' , 'food_venue', 'favorite_by','items','price']
        extra_kwargs = {
            'favorite_by':{'write_only': True},
        }
        
        
        

class AvailableItemsCreateSerialzier(serializers.ModelSerializer):
   
    class Meta:
        model = available_item
        fields = ['id','food_venue','item','quantity','discount','price','availablity_time']
    
    def save(self):
        """ adds a new item to available items """
        food_venue = self.validated_data['food_venue']
        item = self.validated_data['item']
        quantity = self.validated_data['quantity']
        discount = self.validated_data ['discount']
        price = self.validated_data['price']
        availablity_time = self.validated_data['availablity_time']
        a_item = available_item.objects.add_item(item= item, food_venue = food_venue ,quantity= quantity, discount= discount, price = price, availablity_time = availablity_time)
        return a_item
        


class AvailableItemsSerialzier(serializers.ModelSerializer):
     
     food_venue = FoodVenueSerializer()
     item = ItemSerializer()
     class Meta:
        model = available_item
        fields = ['id','food_venue','item','quantity','discount','price','availablity_time']
        


class AvailablePackagesCreateSerialzier(serializers.ModelSerializer):
   
    class Meta:
        model = available_package
        fields = ['id','food_venue','package','quantity','discount','price','availablity_time']
    
    def save(self):
        """ adds a new item to available items """
        food_venue = self.validated_data['food_venue']
        package = self.validated_data['package']
        quantity = self.validated_data['quantity']
        discount = self.validated_data ['discount']
        price = self.validated_data['price']
        availablity_time = self.validated_data['availablity_time']
        a_package = available_package.objects.add_package(package= package, food_venue = food_venue ,quantity= quantity, discount= discount, price = price, availablity_time = availablity_time)
        return a_package
        


class AvailablePackagesSerialzier(serializers.ModelSerializer):
    food_venue = FoodVenueSerializer()
    package = PackageSerializer()
    class Meta:
        model = available_package
        fields = ['id','food_venue','package','quantity','discount','price','availablity_time']
        



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'