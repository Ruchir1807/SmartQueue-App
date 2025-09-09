from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),         # 👈 homepage 
    path('join/', views.join_queue, name='join_queue'),
        path('join_queue_qr/', views.join_queue_qr, name='join_queue_qr'),
    path('status/',views.check_status, name='check_status'),
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('counter/', views.counter_view, name='counter'),

]

