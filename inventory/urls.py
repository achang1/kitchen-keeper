from django.urls import include, path
from inventory import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'storage', views.StorageViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'item', views.ItemViewSet)

# Automatically generate URL using router class
urlpatterns = [
    path('', include(router.urls)),
]