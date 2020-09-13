from django.contrib import admin

from .models import Rating, Categorie, Book, Member, Peminjaman


class RatingAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


class CategorieAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


class BookAdmin(admin.ModelAdmin):
    list_display = [
        'dateAdd',
        'name',
        'author',
        'status',
        'rating',
        'categorie',
        'user_add',
    ]
    list_filter = (
        ('status', admin.BooleanFieldListFilter),
        'author',
        'name',
        ('categorie', admin.RelatedOnlyFieldListFilter),
        ('user_add', admin.RelatedOnlyFieldListFilter),
        
    )


class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'date_in',
        'address',
        'email',
        'date_born',
        'status'
    ]
    list_filter = (
        ('status', admin.BooleanFieldListFilter),
        'date_in',
        'address',
    )


class PeminjamanAdmin(admin.ModelAdmin):
    list_display = [
        'dateAdd',
        'member',
        'book',
        'date_must_back',
        'date_back_by_member',
        'status_denda',
        'status_pengembalian',
        'user',
    ]
    list_filter = (
        ('status_denda',  admin.BooleanFieldListFilter),
        ('status_pengembalian', admin.BooleanFieldListFilter),
        ('member', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'dateAdd',
    )

admin.site.register(Rating, RatingAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Peminjaman, PeminjamanAdmin)
