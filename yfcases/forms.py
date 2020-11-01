from django import forms
from .models import *
from users.models import *

COMPANY_LIST = [
  ("",""),
  ("揚富開發有限公司","揚富開發有限公司"),
  ("鉅鈦開發有限公司","鉅鈦開發有限公司"),
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

