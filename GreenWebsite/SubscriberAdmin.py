from django.contrib import admin
from django.core.mail import send_mail
from .models import Subscriber


# Define the action function
def send_email(modeladmin, request, queryset):
    for subscriber in queryset:
        send_mail(
            'Subject Here',
            'Here is your message.',
            'kondaveetimanasa77@gmail.com',  # Change to your sender email
            [subscriber.email],
            fail_silently=False,
        )
    modeladmin.message_user(request, "Emails have been sent successfully!")


send_email.short_description = "Send email to selected subscribers"


# Define a custom admin class
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_on']  # Customize as needed
    actions = [send_email]


# Register your model with the custom admin class
admin.site.register(Subscriber, SubscriberAdmin)
