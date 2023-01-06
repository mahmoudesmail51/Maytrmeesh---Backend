
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import *

from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('venues', FoodVenueViewSet,basename = 'venues')
router.register('items',ItemViewSet)
router.register('packages',PackageViewSet)
router.register('available-items',AvailableItemsViewSet)
router.register('available-packages',AvailablePackagesViewSet)
router.register('orders', OrdersViewset)



urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token ,name="login"),

]