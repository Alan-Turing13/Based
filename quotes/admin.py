from django.contrib import admin
from .models import Author, Quote

admin.site.register(Author)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'added_by', 'is_approved', 'added_at']
    list_filter = ['is_approved']
    actions = ['approve_quotes']

    def approve_quotes(self, request, queryset):
        queryset.update(is_approved=True)

    approve_quotes.short_description = 'Approve quotes'