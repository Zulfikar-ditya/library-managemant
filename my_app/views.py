from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Rating, Categorie, Book, Member, Peminjaman
from .forms import MemberForm


def index(request):
    return render(request, 'home/index.html')


# member page
def add_member(request):
    if request.user.is_authenticated:
        page = 'Member'
        if request.method == 'POST':
            form = MemberForm(request.POST)
            if form.is_valid:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                if 'add' in request.POST:
                    return HttpResponseRedirect(reverse('home:member-list'))
                else:
                    return HttpResponseRedirect(reverse('home:add-member'))
                    
        else:
            form = MemberForm()
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
                return search_member_by_name(request, query)
            except:
                query = request.POST['id']
                return search_member_by_id(request, query)
        page = 'Member'
        data = Member.objects.all().order_by('id')
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list.html', {
            'page': page,
            'data': dataresult,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def search_member_by_name(request, query):
    if request.user.is_authenticated:
        page = f'Search result for name: {query}'
        data = Member.objects.filter(name__contains=query)
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list.html', {
            'page': page,
            'data': dataresult,
        })
    else: 
        return HttpResponseRedirect(reverse('login'))
        

def search_member_by_id(request, query):
    if request.user.is_authenticated:
        page = f'Search result for id: {query}'
        data = Member.objects.filter(pk=query)
        paginator = Paginator(data, 100)
        pageNum = request.GET.get('page')
        dataresult = paginator.get_page(pageNum)
        return render(request, 'home/list.html', {
            'page': page,
            'data': dataresult,
        })
    else: 
        return HttpResponseRedirect(reverse('login'))
        


# succes error page
def not_found(request):
    return render(request, 'error-success/404.html')


def success(request):
    return render(request, 'error-success/success.html')