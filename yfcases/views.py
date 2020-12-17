# encoding: utf-8
from django.conf import settings
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT
from .models import *
from users.models import *
from .forms import *
from .filters import YfcaseFilter
from wkhtmltopdf.views import PDFTemplateView
from django_pdfkit import PDFView


def font_path():
  # pdfmetrics.registerFont(TTFont('yh', '{}/fonts/msyh.ttf'.format(settings.STATICFILES_DIRS[0])))
  pdfmetrics.registerFont(TTFont('yh', '{}/fonts/TaipeiSansTCBeta-Regular.ttf'.format(settings.STATICFILES_DIRS[0])))
  DEFAULT_FONT['helvetica'] = 'yh'

def load_townships(request):
  city_id = request.GET.get('city')
  townships = Township.objects.filter(city_id=city_id).order_by('name')
  return render(request, 'yfcase/township_dropdown_list_options.html', {'townships': townships})
 
@method_decorator(login_required,name='dispatch') 
class YfcaseListView(ListView):
  model=Yfcase
  template_name="home.html"
  filter_class = YfcaseFilter
			
  def get_queryset(self):
    return Yfcase.objects.all()

  def get_context_data(self, *args, **kwargs):
    context = super(YfcaseListView,self).get_context_data(**kwargs)
    myFilter = self.filter_class(self.request.GET, queryset=self.get_queryset())
    object_list = myFilter.qs
    context['myFilter'] = myFilter
    context['object_list'] = object_list
    return context 

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

# Auction
class AuctionCreateView(CreateView):
  model=Auction
  form_class = AuctionForm
  template_name="auction/auction_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '新增拍賣資訊'
    
    return context

class AuctionUpdateView(UpdateView):
  model=Auction
  form_class = AuctionForm
  template_name="auction/auction_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新拍賣資訊'
    return context
    
# Survey
class SurveyCreateView(CreateView):
  model=Survey
  form_class = SurveyForm
  template_name="survey/survey_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '新增勘查項目'
    
    return context

class SurveyUpdateView(UpdateView):
  model=Survey
  form_class = SurveyForm
  template_name="survey/survey_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新勘查項目'
    return context
    
# ClickList
class ClickListCreateView(CreateView):
  model=ClickList
  form_class = ClickListForm
  template_name="clicklist/clicklist_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '新增查檢表項目'
    return context

class ClickListUpdateView(UpdateView):
  model=ClickList
  form_class = ClickListForm
  template_name="clicklist/clicklist_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新查檢表項目'
    return context
    
# ObjectBuild
class ObjectBuildCreateView(CreateView):
  model=ObjectBuild
  form_class = ObjectBuildForm
  template_name="objectBuild/objectBuild_new.html"
  # def form_valid(self, form):
  #   # Save the validated data of your object
  #   self.object = form.save(commit = False)
  #   # Update the value of the desired field
  #   self.object.yfcase = Yfcase.objects.get(id=2).yfcaseCaseNumber
  #   # Save the object to commit the changes
  #   self.object.save()
  #   # Response with the success url or whatever is default
  #   return super(MyView, self).form_valid(form)
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '新增參考物件'
    return context

class ObjectBuildUpdateView(UpdateView):
  model=ObjectBuild
  form_class = ObjectBuildForm
  template_name="objectBuild/objectBuild_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '更新參考物件'
    return context

class ObjectBuildDeleteView(DeleteView):
  model=ObjectBuild
  template_name="objectBuild/objectBuild_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

# ScroeA
class ScoreAUpdateView(UpdateView):
  model=ObjectBuild
  form_class = ScoreAForm
  template_name="score/score_a_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '調整加成評比'
    return context

# 利用UpdateView來清空ScroeA資料
class ScoreADeleteView(UpdateView):
  model=ObjectBuild
  form_class = ScoreAForm
  template_name="score/score_a_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

# ScoreB
class ScoreBUpdateView(UpdateView):
  model=ObjectBuild
  form_class = ScoreBForm
  template_name="score/score_b_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '調整加成評比'
    return context

# 利用UpdateView來清空ScroeB資料
class ScoreBDeleteView(UpdateView):
  model=ObjectBuild
  form_class = ScoreBForm
  template_name="score/score_b_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

# ScoreC
class ScoreCUpdateView(UpdateView):
  model=ObjectBuild
  form_class = ScoreCForm
  template_name="score/score_c_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '調整加成評比'
    return context

# 利用UpdateView來清空ScroeC資料
class ScoreCDeleteView(UpdateView):
  model=ObjectBuild
  form_class = ScoreCForm
  template_name="score/score_c_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})
    
# RegionalHead
class RegionalHeadCreateView(LoginRequiredMixin,CreateView):
  model=Yfcase
  form_class = RegionalHeadForm
  template_name="finaldecision/regional_head_new.html"
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '選擇最終判定'
    return context


class RegionalHeadUpdateView(UpdateView):
  model=Yfcase
  form_class = RegionalHeadForm
  template_name="finaldecision/regional_head_edit.html"
  
  # def form_valid(self,form):
  #   form.instance.regionalHead = self.request.user
  #   return super(RegionalHeadUpdateView,self).form_valid(form)
    
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '修正最終判定'
    # context["author_id"] = self.request.user.id
    # context['author_fullname'] = self.request.user.full_name
    return context

class RegionalHeadDeleteView(DeleteView):
  model=Yfcase
  template_name="finaldecision/regional_head_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

# SubSigntrueA
class SubSigntrueACreateView(CreateView):
  model=Yfcase
  form_class = SubSigntrueAForm
  template_name="finaldecision/sub_signtrue_A_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '部署人員1-簽核'
    return context

class SubSigntrueAUpdateView(UpdateView):
  model=Yfcase
  form_class = SubSigntrueAForm
  template_name="finaldecision/sub_signtrue_A_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '部署人員1-簽核(修正)'
    return context

class SubSigntrueADeleteView(UpdateView):
  model=Yfcase
  form_class = SubSigntrueAForm
  template_name="finaldecision/sub_signtrue_A_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

# SubSigntrueB
class SubSigntrueBCreateView(CreateView):
  model=Yfcase
  form_class = SubSigntrueBForm
  template_name="finaldecision/sub_signtrue_B_new.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '部署人員2-簽核'
    return context

class SubSigntrueBUpdateView(UpdateView):
  model=Yfcase
  form_class = SubSigntrueBForm
  template_name="finaldecision/sub_signtrue_B_edit.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.id})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['value'] = '建立'
    context['title'] = '部署人員2-簽核(修正)'
    return context

class SubSigntrueBDeleteView(UpdateView):
  model=Yfcase
  form_class = SubSigntrueBForm
  template_name="finaldecision/sub_signtrue_B_delete.html"
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", kwargs={'pk': self.object.yfcase_id})


### After Winner(Edit) #######################################################################
# 契稅申請單-Modal(Form)
class DeedtaxUpdateView(UpdateView):
  model=Yfcase
  form_class = DeedtaxForm
  template_name="yfcase/afterwinner/Deedtax_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(DeedtaxUpdateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '編輯得標後相關資料'
    return context

# 不動產登記清冊-Modal(Form)  
class RealestateregistrationUpdateView(UpdateView):
  model=Yfcase
  form_class = RealestateregistrationForm
  template_name="yfcase/afterwinner/Realestateregistration_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(RealestateregistrationUpdateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '編輯得標後相關資料'
    return context

# 訴訟狀-Modal(Form)    
class ComplaintUpdateView(UpdateView):
  model=Yfcase
  form_class = ComplaintForm
  template_name="yfcase/afterwinner/Complaint_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(ComplaintUpdateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '編輯得標後相關資料'
    return context 

# 存證信函-Modal(Form)
class LetterUpdateView(UpdateView):
  model=Yfcase
  form_class = LetterForm
  template_name="yfcase/afterwinner/Letter_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(LetterUpdateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '編輯得標後相關資料'
    return context
    
# 共有人分割-Modal(Form)
class CommonpropertydivisionUpdateView(UpdateView):
  model=Yfcase
  form_class = CommonpropertydivisionForm
  template_name="yfcase/afterwinner/Commonpropertydivision_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(CommonpropertydivisionUpdateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '編輯得標後相關資料'
    return context

  
### After Winner(PDF) #######################################################################
# PDFkit-評量表
class yfratingscalePDFView(PDFView):
  template_name = './pdf/yfratingscale_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    context.update({
        'yfcase': yfcase,
    })
    return context

# PDFkit-契稅申請書
class deedtaxPDFView(PDFView):
  template_name = './pdf/deedtax_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'users': users,
    })
    return context

# PDFkit-不動產土地登記申請書
class realestateregistrationPDFView(PDFView):
  template_name = './pdf/realestateregistration_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'users': users,
    })
    return context

# PDFkit-訴訟狀
class complaintPDFView(PDFView):
  template_name = './pdf/complaint_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    context.update({
        'yfcase': yfcase,
    })
    return context
    
# PDFkit-存證信函
class letterPDFView(PDFView):
  template_name = './pdf/letter_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    context.update({
        'yfcase': yfcase,
    })
    return context

# PDFkit-共有人分割
class commonpropertydivisionPDFView(PDFView):
  template_name = './pdf/commonpropertydivision_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    context.update({
        'yfcase': yfcase,
    })
    return context

