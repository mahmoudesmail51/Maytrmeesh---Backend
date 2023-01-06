from django.contrib import admin

# Register your models here.
from django.contrib import admin

from core import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Customer)
admin.site.register(models.FoodVenue)
class ItemAdmin(admin.ModelAdmin):
    exclude = ('favorite_by',)
admin.site.register(models.Item)

admin.site.register(models.Review)
class PackageAdmin(admin.ModelAdmin):
    exclude = ('favorite_by',)
admin.site.register(models.Package)
admin.site.register(models.available_item)
admin.site.register(models.available_package)

admin.site.register(models.Order)
