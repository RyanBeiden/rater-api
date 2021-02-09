from django.conf import settings
from pathlib import Path
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from gamerraterapi.views import GameViewSet, CategoryViewSet, ReviewViewSet, RatingViewSet, login_user, register_user

base_dir = Path(__file__).resolve().parent.parent

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameViewSet, 'game')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'reviews', ReviewViewSet, 'review')
router.register(r'ratings', RatingViewSet, 'rating')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin', admin.site.urls),
]

if settings.DEBUG is True:
    urlpatterns += static('media/', base_dir / 'media/')
elif settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)