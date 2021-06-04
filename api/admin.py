from django.contrib import admin

from .models import Category, User


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoriesAdmin)
admin.site.register(User)
