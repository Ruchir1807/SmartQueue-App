from django.contrib import admin
from .models import Service, Token

# Register Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')   # shows ID + name in admin
    search_fields = ('name',)


# Register Token model
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_number', 'service', 'student', 'status', 'created_at')
    list_filter = ('service', 'status')
    search_fields = ('token_number', 'student__username')
    list_editable = ('status',)   # ✅ makes status editable from list view

