from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from django.conf import settings

from fauna.models import Profile, AnimalStats
from fauna.models.animal import Animal


class UserLikes(admin.TabularInline):
    model = Animal.likes.through
    # fields = ["likes__id", "likes__username", "likes__email"]
    can_delete = False
    show_change_link = True


class UserCreated(admin.TabularInline):
    model = get_user_model()


class AnimalAdmin(ImportExportModelAdmin):
    list_display = ['name', 'extinction', 'period', 'taxonomy_class', 'taxonomy_class', 'taxonomy_family']
    list_filter = ['period']
    search_fields = ['name']
    list_editable = ['extinction']
    actions = ["promote"]
    exclude = ('likes',)

    inlines = [
        UserLikes,
        # UserCreated
    ]

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


class ProfileAdmin(ImportExportModelAdmin):
    fields = ("user", )


class AnimalStatsAdmin(ImportExportModelAdmin):
    fields = ("animal", "is_loved")


admin.site.register(Animal, AnimalAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AnimalStats, AnimalStatsAdmin)
