from django.db import models
from django.contrib.auth.models import User

import datetime

back_day = datetime.timedelta(days=7)


class Rating(models.Model):
    name = models.CharField(max_length=10)
    

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Rating_detail", kwargs={"pk": self.pk})


class Categorie(models.Model):
    name = models.CharField(max_length=30)
    

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Categorie_detail", kwargs={"pk": self.pk})


class Book(models.Model):
    dateAdd = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    denda = models.IntegerField(default=10000)
    denda_hilang = models.IntegerField(default=50000)
    status = models.BooleanField(default=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE,)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-dateAdd']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"pk": self.pk})

    def book_lost(self):
        self.status = False
        self.save()


class Member(models.Model):
    name = models.CharField(max_length=40)
    date_in = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_born = models.DateField()
    status = models.BooleanField(default=True)


    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['-date_in']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})

    def deactive_member(self):
        self.status = False
        self.save()


class Peminjaman(models.Model):
    dateAdd = models.DateField(auto_now_add=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_must_back = models.DateField(auto_created=back_day)
    date_back_by_member = models.DateField(auto_now_add=True)
    status_denda = models.BooleanField(default=False)
    status_pengembalian = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Peminjaman"
        verbose_name_plural = "Peminjamans"
        ordering = ['-dateAdd']

    def __str__(self):
        return self.member

    def get_absolute_url(self):
        return reverse("Peminjaman_detail", kwargs={"pk": self.pk})

    def denda_check(self):
        today = datetime.date.today()
        if self.date_must_back > today:
            self.status_denda = True
            self.save()
        else: pass

    def kembali(self):
        self.status_pengembalian = True
        self.save()

    def perpanjangan_pinjam(self):
        self.date_must_back += back_day
        self.save()