from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from alfie.apps.ramens.models import Ramen, Brand, Box
from alfie.apps.ramens.forms import BoxFormSet

#bigups http://stackoverflow.com/questions/4631865/caching-query-results-in-django
#from django.core.cache import cache
#cache.set('key', Brand.objects.all())

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

	#bigups http://stackoverflow.com/questions/4497684/django-class-based-views-with-inline-model-form-or-formset
	def get_context_data(self, **kwargs):
		context = super(BoxCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['box_forms'] = BoxFormSet(self.request.POST)
		else:
			context['box_forms'] = BoxFormSet()
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		box_forms = context['box_forms']
		if box_forms.is_valid():
			self.object = form.save()
			box_forms.instance = self.object
			box_forms.save()
			return HttpResponse('saved')
		else:
			return self.render_to_response(self.get_context_data(form=form))

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