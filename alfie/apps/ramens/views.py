from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from alfie.apps.ramens.models import Ramen, Manufacturer, Box

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

class MfgCreateView(CreateView):
	model = Manufacturer
	template_name = 'ramens/mfg_form.html'

class MfgDetailView(DetailView):
	queryset = Manufacturer.objects.all()
	context_object_name = 'mfg'
	template_name = 'ramens/mfg_detail.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MfgDetailView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the ramen
		context['ramen_list'] = Ramen.objects.filter(mfg__id=self.kwargs['pk'])
		return context

class MfgUpdateView(UpdateView):
	model = Manufacturer
	success_url = reverse_lazy('mfg_list')
	template_name = 'ramens/mfg_form.html'

class MfgDeleteView(DeleteView):
	model = Manufacturer
	success_url = reverse_lazy('mfg_list')

class BoxListView(ListView):
	model = Box
	context_object_name = 'box_list'
	template_name = 'ramens/box_list.html'

class BoxCreateView(CreateView):
	model = Box
	template_name = 'ramens/box_form.html'

class BoxDetailView(DetailView):
	queryset = Box.objects.all()
	context_object_name = 'box'
	template_name = 'ramens/box_detail.html'

class BoxUpdateView(UpdateView):
	model = Box
	success_url = reverse_lazy('box_list')
	template_name = 'ramens/box_form.html'

class BoxDeleteView(DeleteView):
	model = Box
	success_url = reverse_lazy('box_list')