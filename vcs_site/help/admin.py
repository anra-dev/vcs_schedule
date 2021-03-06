from django.contrib import admin

from .models import Page, Section


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'update_date')
    ordering = ('name',)
    search_fields = ('title', 'body_text')


admin.site.register(Page, PageAdmin)
admin.site.register(Section)
