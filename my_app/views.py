from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

import datetime

from .models import Rating, Categorie, Book, Member, Peminjaman
from .forms import MemberForm, BookForm


today = datetime.date.today()
back = datetime.timedelta(days=7)


def index(request):
    return render(request, 'home/index.html')


def add(request, pagename, modelForm):
    if request.user.is_authenticated:
        page = pagename
        if request.method == 'POST':
            form = modelForm(request.POST)
            if form.is_valid:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                if modelForm is MemberForm:
                    if 'add' in request.POST:
                        return HttpResponseRedirect(reverse('home:member-list'))
                    else:
                        return HttpResponseRedirect(reverse('home:add-member'))
                else:
                    if 'add' in request.POST:
                        return HttpResponseRedirect(reverse('home:book-list'))
                    else:
                        return HttpResponseRedirect(reverse('home:add-book'))
        else:
            form = modelForm()
        return render(request, 'home/add.html', {
            'form': form,
            'page': page,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def add_borrow2(request, member_id):
    if request.user.is_authenticated:
        message = None
        try:
            getMember = Member.objects.get(pk=member_id)
        except (KeyError, Member.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
        if request.method == 'POST':
            try: 
                getBook = Book.objects.get(pk=request.POST['bookid'])
            except (KeyError, Book.DoesNotExist):
                return HttpResponseRedirect(reverse('home:not_found'))
            if getBook.status_dipinjam is True:
                message = 'this book already borrowed by another user, you may wrong enter the id of book'
                return render(request, 'home/peminjaman.html',{
                    'message': message,
                })
            else:
                message = None
            getBook.status_dipinjam = True
            getBook.save()
            new = Peminjaman.objects.create(
                member=getMember,
                book=getBook,
                date_must_back=today + back,
                user=request.user,
            )
            new.save()
            if 'add' in request.POST:
                return HttpResponseRedirect(reverse('home:borrow-list'))
            else:
                return HttpResponseRedirect(f'../../../add-borrow/{getMember.id}/')
        return render(request, 'home/peminjaman.html',{
            'getMember': getMember,
            'message': message,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def add_borrow(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            member = int(request.POST['id'])
            return HttpResponseRedirect(f'../add-borrow/{member}/')
        return render(request, 'home/add-peminjaman.html')
    else:
        return HttpResponseRedirect(reverse('login'))


def borrow_list(request):
    if request.user.is_authenticated:
        page = 'Borrow'
        boorow_object = Peminjaman.objects.filter(status_pengembalian=False).order_by('id')
        for i in boorow_object:
            i.denda_check()
        paginator = Paginator(boorow_object, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list-borrow.html', {
            'data': dataresult,
            'page': page,
        })
    else:
        return HttpResponseRedirect(reverse('login'))
        

def member_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                query = request.POST['nama']
                return search_by_name(request, query, Member)
            except:
                query = request.POST['id']
                return search_by_id(request, query, Member)
        page = "Member"
        with_paginator = True
        data = Member.objects.all().order_by('id')
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list.html', {
            'page': page,
            'data': dataresult,
            'with_paginator': with_paginator,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def book_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                query = request.POST['nama']
                return search_by_name(request, query, Book)
            except:
                query = request.POST['id']
                return search_by_id(request, query, Book)
        page = 'Book'
        with_paginator = True
        data = Book.objects.all().order_by('id')
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list-book.html', {
            'page': page,
            'data': dataresult,
            'with_paginator': with_paginator,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def book_borrow_by_member(request, member_id):
    if request.user.is_authenticated:
        try:
            getMember = Member.objects.get(pk=member_id)
        except (KeyError, Member.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
        getBookList = Peminjaman.objects.filter(member=getMember, status_pengembalian=False)
        for i in getBookList:
            i.denda_check()
        paginator = Paginator(getBookList, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/book-borrow-by-member.html', {
            'getMember': getMember,
            'data': dataresult,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def return_book(request, book_id):
    if request.user.is_authenticated:
        message = None
        try:
            getBook = Book.objects.get(pk=book_id)
        except:
            return HttpResponseRedirect(reverse('home:not_found'))
        try:
            getPeminjaman = Peminjaman.objects.get(book=getBook.id, status_pengembalian=False)
        except: return HttpResponseRedirect(reverse('home:not_found'))
        if request.method == 'POST':
            getPeminjaman.status_pengembalian = True
            getPeminjaman.date_back_by_member = datetime.date.today()
            getPeminjaman.save()
            getBook.status_dipinjam = False
            getBook.save()
            if 'return' in request.POST:
                return HttpResponseRedirect(reverse('home:borrow-list'))
            else:
                return HttpResponseRedirect(reverse('home:return-1'))
        if getPeminjaman.status_pengembalian is True:
            return HttpResponseRedirect(reverse('home:not_found'))
        getPeminjaman.denda_check()
        if getPeminjaman.status_denda is True:
            message = True
        else:
            message = False
        return render(request, 'home/return-display.html', {
            'getBook': getBook,
            'getPeminjaman': getPeminjaman,
            'message': message,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def return_book_input(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            query = int(request.POST['id'])
            return HttpResponseRedirect(f'../return/{query}/')
        return render(request, 'home/return.html')
    else:
        return HttpResponseRedirect(reverse('login'))


def history_member(request, member_id):
    if request.user.is_authenticated:
        try:
            getMember = Member.objects.get(pk=member_id)
        except (KeyError, Member.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
        member_peminjaman = Peminjaman.objects.filter(member=getMember.id)
        for i in member_peminjaman:
            if i.status_pengembalian is False:
                i.denda_check()
            else: pass
        paginator = Paginator(member_peminjaman, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/history-member.html', {
            'data': dataresult,
            'member': getMember,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def history_book(request, book_id):
    if request.user.is_authenticated:
        try:
            getBook = Book.objects.get(pk=book_id)
        except(KeyError, Book.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
        getPeminjaman = Peminjaman.objects.filter(book=getBook.id)
        paginator = Paginator(getPeminjaman, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/history-book.html', {
            'getBook': getBook,
            'data': dataresult,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def search_by_name(request, query, model):
    if request.user.is_authenticated:
        page = f'Search result for name: {query}'
        if model is Member:
            data = model.objects.filter(name__contains=query)
        else:
            data = model.objects.filter(title__contains=query)
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        with_paginator = True
        if model is Member:
            return render(request, 'home/list.html', {
                'page': page,
                'data': dataresult,
                'with_paginator': with_paginator,
            })
        else:
            return render(request, 'home/list-book.html', {
                'page': page,
                'data': dataresult,
                'with_paginator': with_paginator,
        })
    else: 
        return HttpResponseRedirect(reverse('login'))
        

def search_by_id(request, query, model):
    if request.user.is_authenticated:
        page = f'Search result for id: {query}'
        data = model.objects.filter(pk=query)
        with_paginator = False
        return render(request, 'home/list.html', {
            'page': page,
            'data': data,
            'with_paginator': with_paginator,
        })
    else: 
        return HttpResponseRedirect(reverse('login'))


def add_member(request):
    return add(request, 'Member', MemberForm)


def add_book(request):
    return add(request, 'Book', BookForm)


# succes error page
def not_found(request):
    return render(request, 'error-success/404.html')


def success(request):
    return render(request, 'error-success/success.html')