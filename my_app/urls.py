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

    # borrow
    path('add-borrow/', views.add_borrow, name='add-borrow'),
    path('add-borrow/<int:member_id>/', views.add_borrow2, name='add-borrow2'),
    path('borrow-list/', views.borrow_list, name='borrow-list'),

    # error success
    path('404/', views.not_found, name='not_found'),
    path('success/', views.success, name='success'),

]
