from django.contrib import admin
from .models import Message
from .models import Chat

class MessageAdmin(admin.ModelAdmin):
    fields = ('text','chat','created_at','author', 'receiver')
    list_display = ('created_at','chat','text','author', 'receiver')
    search_fields = ('text',)

# Register your models here.
admin.site.register(Message,MessageAdmin)
admin.site.register(Chat)
