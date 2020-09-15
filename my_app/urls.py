from  django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    # member
    path('add-member/', views.add_member, name='add-member'),
    path('member-list/', views.member_list, name='member-list'),

    # book
    path('add-book/', views.add_book, name='add-book'),
    path('book-list/', views.book_list, name='book-list'),

    # error success
    path('404/', views.not_found, name='not_found'),
    path('success/', views.success, name='success'),

]
