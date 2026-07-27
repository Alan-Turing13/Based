from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse

from theology import settings
from .models import Author, Quote

admin.site.register(Author)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'added_by', 'is_approved', 'added_at']
    list_filter = ['is_approved']
    actions = ['approve_quotes']

    def approve_quotes(self, request, queryset):
        for quote in queryset:
            if not quote.is_approved and quote.added_by and quote.added_by.email:
                quote.is_approved = True
                quote.save()
                # Send user a link to their quote now that it's approved
                quote_url = f'https://{settings.SITE_DOMAIN}{reverse("quotes:quote_detail", args=[quote.pk])}'
                send_mail(
                    subject='Quote approved',
                    message=f'Hi {quote.added_by.username},\n\nYour quote has been approved and is now live on Based.\n\n{quote_url}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[quote.added_by.email],
                )

    approve_quotes.short_description = 'Approve quotes'