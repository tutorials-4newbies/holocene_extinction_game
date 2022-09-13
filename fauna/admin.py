from django.contrib import admin
from django.db.models import QuerySet
from import_export.admin import ImportExportMixin
# Register your models here.
from fauna.models import Animal

from django.conf import settings


class AnimalAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'extinction', 'period', 'taxonomy_class', 'taxonomy_order', 'taxonomy_family']
    list_filter = ['period']
    search_fields = ['name']
    list_editable = ['extinction']
    actions = ["upgrade_period"]

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        if settings.PERIOD != 'all':
            qs = qs.filter(period=settings.PERIOD)
        return qs

    admin.action(description='Upgrade the period')
    def upgrade_period(self, request, queryset):
        for obj in queryset:
            if obj.period == Animal.PERIOD_CHOICES[0]:
                obj.period = Animal.PERIOD_CHOICES[1]
                obj.save()


admin.site.register(Animal, AnimalAdmin)
