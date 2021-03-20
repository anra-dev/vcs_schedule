from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'get_recipient_name', 'get_recipient_email')
    search_fields = ('recipient', 'created_at', 'message')

    @staticmethod
    def get_recipient_name(obj):
        return ",\n".join([rec.get_full_name() for rec in obj.recipient.all()])

    @staticmethod
    def get_recipient_email(obj):
        return ",\n".join([rec.email for rec in obj.recipient.all()])

    class Meta:
        model = Message
        fields = '__all__'


admin.site.register(Message, MessageAdmin)