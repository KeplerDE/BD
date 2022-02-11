from django.contrib import admin
from .models import Movie
from django.db.models import QuerySet



class RatingFilter(admin.SimpleListFilter):
    title = "Фильтр по Рейтингу"
    parameter_name = "qwerty"

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('от 40 до 59', 'Средний'),
            ('от 60 до 79', 'Высокий'),
            ('>=', 'Еще выше'),

        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value()=='<40':
            return queryset.filter(rating__lt=40)
        if self.value()=='от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        return queryset




@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'currency', 'budget', 'rating_status']
    list_editable = ['rating', 'currency', 'budget']
    ordering = ['rating', 'name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    search_fields = ['name__istartswith']
    list_filter = ['name', 'currency', RatingFilter]

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


    @admin.action(description='Установить валюту евро')
    def set_euro(self, request, qs: QuerySet):
        qs.update(currency=Movie.EUR)





