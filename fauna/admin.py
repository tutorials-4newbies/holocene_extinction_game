from django.contrib import admin

# Register your models here.
from fauna.models import Animal


class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'extinction', 'period', 'taxonomy_class', 'taxonomy_class', 'taxonomy_family']
    list_filter = ['period']
    search_fields = ['name']
    list_editable = ['extinction']
    

admin.site.register(Animal, AnimalAdmin)
