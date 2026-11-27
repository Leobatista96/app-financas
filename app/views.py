from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import RegistrationForm


class SignUpView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class LandingView(TemplateView):
    """Porta de entrada do sistema: landing page pública em /"""
    template_name = 'landing.html'
