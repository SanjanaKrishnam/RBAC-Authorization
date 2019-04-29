from django.views import generic
from braces.views import LoginRequiredMixin
from profiledet.models import USERMODEL
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from profiledet.models import USERMODEL
import json
from django.http import Http404
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models
from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q



class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'django_private_chat/dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        p = USERMODEL.objects.get(name = self.request.user.username)
        if p.type=='Public':
            raise Http404
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
    #    if not dialogs:
    #        raise Http404
        return dialogs

    def get_context_data(self, **kwargs):
        p = USERMODEL.objects.get(name = self.request.user.username)
        if p.type=='Public':
            raise Http404
        context = super().get_context_data()
        jd = json.decoder.JSONDecoder()
        if p.auth is None:
            p.auth = json.dumps([])
            p.save()
        k = jd.decode(p.auth)
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
            if self.kwargs.get('username') == self.request.user.username or self.kwargs.get('username') not in k :
                raise Http404
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            return context
    
        if self.request.user == context['active_dialog'].owner:
            context['opponent_username'] = context['active_dialog'].opponent.username
        else:
            context['opponent_username'] = context['active_dialog'].owner.username
        context['ws_server_path'] = '{}://{}:{}/'.format(
            settings.CHAT_WS_SERVER_PROTOCOL,
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context
