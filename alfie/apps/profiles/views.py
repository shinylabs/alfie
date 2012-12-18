# time
import datetime
now = datetime.datetime.now()

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from userena.decorators import secure_required
from userena import settings as userena_settings

class ExtraContextTemplateView(TemplateView):
    """ Add extra context to a simple template view """
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraContextTemplateView, self).get_context_data(*args, **kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context

    # this view is used in POST requests, e.g. signup when the form is not valid
    post = TemplateView.get

@secure_required
def cancel_profile(request, username, template_name='userena/cancel_form.html', success_url=None, extra_context=None, **kwargs):
	"""
		Shows warning, confirm action, then update profile as cancelled
	"""
	user = get_object_or_404(User, username__iexact=username)
	profile = user.get_profile()

	# When a form is sent
	if request.method == 'POST':
		"""
		if form.has_shipped(profile) is False:
            profile = form.save()
            try:
                update_subscription(profile, profile.choice.name, prorate="False")
            except:
                pass
            msg = 'Your menu choice has been updated.'
        else:
            profile = form.save()
            msg = 'Your changes will be scheduled for next month.'
        """
        if profile.cancelled is None:
        	profile.cancelled = now
        	profile.save()
        	msg = 'Account cancelled'
        else:
			profile.cancelled = None
			profile.save()
			msg = 'Account reinstated'

        if userena_settings.USERENA_USE_MESSAGES:
            messages.success(request, _(msg), fail_silently=True)

        if success_url: redirect_to = success_url
        else: redirect_to = reverse('userena_profile_detail', kwargs={'username': username})
        return redirect(redirect_to)

	if not extra_context: extra_context = dict()
	extra_context['profile'] = profile
	return ExtraContextTemplateView.as_view(template_name=template_name, extra_context=extra_context)(request)