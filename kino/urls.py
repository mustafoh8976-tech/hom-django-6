from django.urls import path
from .views import home_view, kino_detail


urlpatterns = [
    path('', home_view, name='home'),
    path('kino/<int:pk>/', kino_detail, name='kino_detail'),
]
