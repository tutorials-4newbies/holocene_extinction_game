from django.contrib import admin

# Register your models here.
from fauna.models import Animal


class AnimalAdmin(admin.ModelAdmin):
    list_display = ["name", "period", "extinction", "taxonomy_class"]
    search_fields = ["name", "period"]
    list_editable = ["extinction"]

# 
admin.site.register(Animal, AnimalAdmin)
