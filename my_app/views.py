from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Rating, Categorie, Book, Member, Peminjaman
from .forms import MemberForm, BookForm


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