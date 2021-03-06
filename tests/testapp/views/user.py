from functools import partial

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Case, When, Value
from django.http import HttpResponse

from binder.json import jsondumps
from binder.permissions.views import PermissionView
from binder.plugins.views import UserViewMixIn, MasqueradeMixin
from binder.router import list_route


class UserView(MasqueradeMixin, UserViewMixIn, PermissionView):
	model = User

	hidden_fields = ['password', 'is_staff', 'date_joined']

	def _scope_view_own(self, request):
		return Q(pk=request.user.pk)

	@list_route(name='identify', methods=['GET'])
	def identify(self, request):
		"""
		Simple endpoint, to identify own user

		:param request:
		:return:
		"""
		me = self.get_queryset(request).get(pk=request.user.pk)
		return HttpResponse(
			jsondumps({
				'username': me.username,
				'email': me.email
			}))
