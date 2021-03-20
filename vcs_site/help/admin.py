from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Page, Section


class PageAdminForm(forms.ModelForm):
    body_text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Page
        fields = '__all__'


class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('name', 'title', 'created_at')
    search_fields = ('title', 'body_text')


admin.site.register(Page, PageAdmin)
admin.site.register(Section)
