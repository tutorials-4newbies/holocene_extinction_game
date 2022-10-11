from django.contrib import admin, messages

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from fauna.models import Animal
from django.conf import settings


class AnimalAdmin(ImportExportModelAdmin):
    list_display = ['name', 'extinction', 'period', 'taxonomy_class', 'taxonomy_class', 'taxonomy_family']
    list_filter = ['period']
    search_fields = ['name']
    list_editable = ['extinction']
    actions = ["promote"]

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        if hasattr(settings, "ACCEPTED_PERIOD"):
            qs = qs.filter(period=settings.ACCEPTED_PERIOD)
        return qs

    @admin.action(description="Promote period")
    def promote(self, request, queryset):
        changed = False
        for animal in queryset:
            if animal.period == 'PERMIAN':
                animal.period = 'TRIASSIC'
                animal.save()
                changed = True
        if changed:
            self.message_user(request=request, message="promoted!", level=messages.WARNING)


admin.site.register(Animal, AnimalAdmin)
