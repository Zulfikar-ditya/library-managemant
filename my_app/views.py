from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
                if request.POST['add']:
                    return HttpResponseRedirect(reverse('home:index'))
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

