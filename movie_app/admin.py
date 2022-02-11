from django.contrib import admin
from .models import Movie
from django.db.models import QuerySet





@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'currency', 'budget', 'rating_status']
    list_editable = ['rating', 'currency', 'budget']
    ordering = ['rating', 'name']
    list_per_page = 10
    actions = ['set_dollars']

    @admin.display(ordering='rating', description='Status')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть?'
        if mov.rating < 70:
            return 'Разок можно глянуть'
        if mov.rating < 85:
            return 'Норм'

    @admin.action(description='Установить валюту доллар')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)
