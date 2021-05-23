from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class RegisterView(CreateView):
    form_class = CreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')



