from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .models import *
from .forms import *

def load_townships(request):
  city_id = request.GET.get('city')
  townships = Township.objects.filter(city_id=city_id).order_by('name')
  return render(request, 'yfcase/township_dropdown_list_options.html', {'townships': townships})
 
@method_decorator(login_required,name='dispatch') 
class YfcaseListView(ListView):
  model=Yfcase
  template_name="home.html"

@method_decorator(login_required,name='dispatch')
class YfcaseDetailView(DetailView):
  model=Yfcase
  form_class = YfcaseForm
  template_name="yfcase/yfcase_detail.html"
  success_url = reverse_lazy('yfcase:yfcase_detail')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = '建立項目'
    return context
    
class YfcaseCreateView(CreateView):
  model=Yfcase
  form_class = YfcaseForm
  template_name="yfcase/yfcase_new.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(YfcaseCreateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '建立'
    context['title'] = '新增基本資料'
    return context
    
class YfcaseUpdateView(UpdateView):
  model=Yfcase
  form_class = YfcaseForm
  template_name='yfcase/yfcase_edit.html'
    
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", args=(self.object.id,))

  def form_valid(self, form):
    if form.cleaned_data['yfcaseCaseNumber'] is None:
        form.add_error('yfcaseCaseNumber', 'Incident with this email already exist')
        return self.form_invalid(form)
    return super(YfcaseUpdateView, self).form_valid(form)
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '更新'
    context['title'] = '更新基本資料'
    return context
    
class YfcaseDeleteView(DeleteView):
  model=Yfcase
  template_name="yfcase/yfcase_delete.html"
  success_url=reverse_lazy('yfcase:home')


# Land
class LandCreateView(CreateView):
  model=Land
  form_class = LandForm
  template_name="land/land_new.html"

  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id,})

  def get_context_data(self, **kwargs):
    context = super(LandCreateView,self).get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '新增土地項目'
    return context
    
class LandUpdateView(UpdateView):
  model=Land
  form_class = LandForm
  template_name="land/land_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新土地項目'
    return context

class LandDeleteView(DeleteView):
  model=Land
  template_name="land/land_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})
    
# Build
class BuildCreateView(CreateView):
  model=Build
  form_class = BuildForm
  template_name="build/build_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '建立建物項目'
    return context
    
class BuildUpdateView(UpdateView):
  model=Build
  form_class = BuildForm
  template_name="build/build_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新建物項目'
    return context
    
class BuildDeleteView(DeleteView):
  model=Build
  template_name="build/build_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})