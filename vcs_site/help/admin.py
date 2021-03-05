from django.contrib import admin

from .models import Page, Section


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_date')
    ordering = ('title',)
    search_fields = ('title',)


admin.site.register(Page, PageAdmin)
admin.site.register(Section)
