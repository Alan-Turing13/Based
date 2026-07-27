import smtplib

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.list import ListView
from thefuzz import fuzz

from quotes.forms import AddQuote, AddAuthor, RegisterForm
from quotes.models import Quote, Author, Profile
from theology import settings

class QuoteSearch(ListView):
    template_name = "quote_search.html"
    model = Quote
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            queryset = Quote.objects.all()
            for word in query.split():
                queryset = queryset.filter(
                    Q(text__icontains=word) |
                    Q(author__name__icontains=word) |
                    Q(subject__icontains=word) |
                    Q(derivation__icontains=word)
                )
            return queryset.distinct().filter(is_approved=True)
        return Quote.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class QuoteList(ListView):
    template_name = "quote_list.html"
    model = Quote
    paginate_by = 20

    def get_queryset(self):
        return Quote.objects.filter(is_approved=True).order_by('-added_at')

class QuoteDetail(DetailView):
    template_name = "quote_detail.html"
    model = Quote

# show all quotes by a given author
class AuthorDetail(DetailView):
    model = Author
    template_name = "author_detail.html"

# show all quotes on a given subject
class SubjectDetail(ListView):
    template_name = "subject_detail.html"

    def get_queryset(self):
        return Quote.objects.filter(subject=self.kwargs['subject'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.kwargs['subject']
        return context

class QuoteCreate(LoginRequiredMixin, CreateView):
    template_name = "quote_create.html"
    form_class = AddQuote
    success_url = reverse_lazy('quotes:quote_list')
    
    def form_valid(self, form):

        # set the current user as the one who posted the quote
        form.instance.added_by = self.request.user

        # has the user had previously approved posts? if so, the user is trusted
        trusted_user = Quote.objects.filter(added_by=self.request.user, is_approved=True).exists()
        form.instance.is_approved = trusted_user

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_form'] = AddAuthor()
        return context

def add_author(request):
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']

            for author in Author.objects.all():
                similarity = fuzz.token_sort_ratio(new_name.lower(), author.name.lower())
                if similarity >= 75:
                    return JsonResponse({'errors': {
                        'name': [f'This author may already exist as "{author.name}", please check the dropdown.']
                    }
                    }, status=400)

            author = form.save()
            return JsonResponse({'id': author.id, 'name': author.name})
    return JsonResponse({'errors': form.errors}, status=400)

class QuoteEdit(LoginRequiredMixin, UpdateView):
    model = Quote
    template_name = "quote_create.html"
    form_class = AddQuote
    success_url = reverse_lazy('quotes:quote_list')

    def get_queryset(self):
        return Quote.objects.filter(added_by=self.request.user)

class QuoteDelete(LoginRequiredMixin, DeleteView):
    template_name = "quote_delete.html"
    model = Quote
    success_url = reverse_lazy('quotes:quote_list')

    def get_queryset(self):
        return Quote.objects.filter(added_by=self.request.user)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user)
            confirmation_link = request.build_absolute_uri(
                reverse('quotes:confirm_email', args=[profile.confirmation_token])
            )
            try:
                send_mail(
                    subject='Confirm your Based account',
                    message=f'Click the link to confirm your account on Based: {confirmation_link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            except (BadHeaderError, smtplib.SMTPException) as e:
                print(f"Email error: {e}")

            return render(request, 'registration/check_your_email.html')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def confirm_email(request, token):
    profile = get_object_or_404(Profile, confirmation_token=token)
    profile.user.is_active = True
    profile.user.save()
    profile.email_confirmed = True
    profile.save()
    login(request, profile.user)
    return redirect('quotes:quote_list')