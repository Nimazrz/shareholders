from django.urls import path
from . import views
app_name = 'holders'
urlpatterns = [
    path('', views.index, name='index'),
    path('shareholder/<int:shareholderid>/', views.shareholder_detail, name='shareholder_detail'),

]