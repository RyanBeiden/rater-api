from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from gamerraterapi.views import GameViewSet, CategoryViewSet, login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameViewSet, 'game')
router.register(r'categories', CategoryViewSet, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
