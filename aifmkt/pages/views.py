from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition",
                "placeholder": "Your name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition",
                "placeholder": "you@example.com",
            }
        ),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition",
                "placeholder": "What is this about?",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition resize-y",
                "rows": "5",
                "placeholder": "Your message...",
            }
        ),
    )


class AboutView(TemplateView):
    template_name = "pages/about.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thanks! Your message has been received. We'll respond within 24 hours.")
            form = ContactForm()
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
