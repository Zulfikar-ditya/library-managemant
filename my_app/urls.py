from  django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    # member
    path('add-member/', views.add_member, name='add-member'),
    path('member-list/', views.member_list, name='member-list'),

    # error success
    path('404/', views.not_found, name='not_found'),
    path('success/', views.success, name='success'),

]
