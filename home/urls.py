from django.urls import path
from home import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('nodes', views.nodes, name='nodes'),
]
