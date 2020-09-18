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
    path('user-book-borrow/<int:member_id>/', views.book_borrow_by_member, name='user-book-borrow'),

    # return
    path('return/', views.return_book_input, name='return-1'),
    path('return/<int:book_id>/', views.return_book, name='return-2'),

    # error success
    path('404/', views.not_found, name='not_found'),
    path('success/', views.success, name='success'),

    # history
    path('history-member/<int:member_id>/', views.history_member, name='history-member'),
    path('history-book/<int:book_id>/', views.history_book, name='history-book'),
]
