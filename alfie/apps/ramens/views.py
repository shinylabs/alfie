from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from alfie.apps.ramens.models import Ramen, Manufacturer

class RamenListView(ListView):
	model = Ramen
	context_object_name = 'ramen_list'

class RamenCreateView(CreateView):
	model = Ramen

class RamenDetailView(DetailView):
	model = Ramen

class RamenUpdateView(UpdateView):
	model = Ramen
	success_url = reverse_lazy('ramen_list')

class RamenDeleteView(DeleteView):
	model = Ramen
	success_url = reverse_lazy('ramen_list')

class MfgListView(ListView):
	model = Manufacturer
	context_object_name = 'mfg_list'
	template_name = 'ramens/mfg_list.html'

class MfgDetailView(DetailView):
	queryset = Manufacturer.objects.all()
	context_object_name = 'mfg'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MfgDetail, self).get_context_data(**kwargs)
		# Add in the QuerySet of all the books
		context['ramen_list'] = Ramen.objects.all()
		return context