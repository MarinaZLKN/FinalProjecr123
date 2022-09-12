from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import logging


logger1 = logging.getLogger('django.security')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    logger1.warning('Upgrading to authors')
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')




class ProfileUpdate(LoginRequiredMixin, UpdateView):
    logger1.warning('Updating the profile')
    model = User
    form_class = BaseRegisterForm
    template_name = 'edit_profile.html'
    success_url = '/'





