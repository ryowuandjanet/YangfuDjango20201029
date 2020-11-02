from django import forms
from .models import *
from users.models import *

COMPANY_LIST = [
  ("",""),
  ("揚富開發有限公司","揚富開發有限公司"),
  ("鉅鈦開發有限公司","鉅鈦開發有限公司"),
]

BUILD_TYPE_USE= [
  ("",""),
  ("公設","公設"),
  ("公寓-5樓含以下無電梯","公寓-5樓含以下無電梯"),
  ("透天厝","透天厝"),
  ("店面-店舖","店面-店舖"),
  ("辦公商業大樓","辦公商業大樓"),
  ("住宅大樓-11層含以上有電梯","住宅大樓-11層含以上有電梯"),
  ("華廈-10層含以下有電梯","華廈-10層含以下有電梯"),
  ("套房","套房"),
  ("增建-持分後坪數打對折","增建-持分後坪數打對折")
]

AREA_LIST = [
  ("",""),
  ("第一種住宅區","第一種住宅區"),
  ("第二種住宅區","第二種住宅區"),
  ("第三種住宅區","第三種住宅區"),
  ("第四種住宅區","第四種住宅區"),
  ("第一種商業區","第一種商業區"),
  ("第二種商業區","第二種商業區"),
  ("第三種商業區","第三種商業區"),
  ("第四種商業區","第四種商業區"),
  ("第二種工業區","第二種工業區"),
  ("第三種工業區","第三種工業區"),
  ("行政區","行政區"),
  ("文教區","文教區"),
  ("倉庫區","倉庫區"),
  ("風景區","風景區"),
  ("農業區","農業區"),
  ("保護區","保護區"),
  ("行水區","行水區"),
  ("保存區","保存區"),
  ("特定專用區","特定專用區")
]

class YfcaseForm(forms.ModelForm):
  yfcaseCompany = forms.ChoiceField(label="所屬公司",choices=COMPANY_LIST, required=False)
  class Meta:
    model=Yfcase
    fields =['yfcaseCaseNumber','yfcaseCompany','yfcaseCity','yfcaseTownship','yfcaseBigSection','yfcaseSmallSection','yfcaseOtherAddress','yfcaseDebtor','yfcaseCreditor','user'] 

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['yfcaseTownship'].queryset = Township.objects.none()
      
      if 'city' in self.data:
        try:
          city_id = int(self.data.get('city'))
          self.fields['yfcaseTownship'].queryset = Township.objects.filter(city_id=city_id).order_by('name')
        except (ValueError, TypeError):
          pass  # invalid input from the client; ignore and fallback to empty City queryset
      elif self.instance.pk:
        self.fields['yfcaseTownship'].queryset = self.instance.city.city_set.order_by('name')

class LandForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  class Meta:
    model=Land
    fields =['yfcase','landNumber','landUrl','landArea','landHoldingPointPersonal','landHoldingPointAll'] 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
class BuildForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  buildTypeUse = forms.ChoiceField(label="建物型",choices=BUILD_TYPE_USE, required=False)
  buildUsePartition = forms.ChoiceField(label="使用分區",choices=AREA_LIST, required=False)
  class Meta:
    model=Build
    fields ='__all__' 