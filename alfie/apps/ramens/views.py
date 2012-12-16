from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from alfie.apps.ramens.models import Ramen, Brand, Box

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



class BrandListView(ListView):
	model = Brand
	context_object_name = 'brand_list'
	template_name = 'ramens/brand_list.html'

class BrandCreateView(CreateView):
	model = Brand
	template_name = 'ramens/brand_form.html'

class BrandDetailView(DetailView):
	queryset = Brand.objects.all()
	context_object_name = 'brand'
	template_name = 'ramens/brand_detail.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BrandDetailView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the ramen
		context['ramen_list'] = Ramen.objects.filter(brand__id=self.kwargs['pk'])
		return context

class BrandUpdateView(UpdateView):
	model = Brand
	success_url = reverse_lazy('brand_list')
	template_name = 'ramens/brand_form.html'

class BrandDeleteView(DeleteView):
	model = Brand
	success_url = reverse_lazy('brand_list')



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
	#bigups http://stackoverflow.com/questions/4918768/django-manytomany-in-template-format

class BoxUpdateView(UpdateView):
	model = Box
	success_url = reverse_lazy('box_list')
	template_name = 'ramens/box_form.html'

class BoxDeleteView(DeleteView):
	model = Box
	success_url = reverse_lazy('box_list')