from django.urls import path
from home import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('nodes', views.node, name='nodes'),
    path('store_feeds', views.store_feeds, name='store_feeds'),
    path('get_feeds', views.get_feeds, name='get_feeds'),
    path('nodereg', views.nodereg, name='nodereg'),
    path('node_edit', views.edit_node, name='edit_node'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
