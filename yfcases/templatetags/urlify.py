from urllib.parse import quote
from decimal import *
from datetime import datetime
from django import template

register=template.Library()

@register.filter
def divide(value, arg):
  try:
    return int(value) / int(arg)
  except (ValueError, ZeroDivisionError):
    return None

@register.filter
def zeroNegative(value):
  return 0 - value


@register.filter
def decimaltofloat(value):
  newlist=[]
  try:
    return float(value)
  except:
    newlist.append(0)

@register.filter
def multiplication(value, arg):
  newlist=[]
  try:
    return value * arg
  except:
    newlist.append(0)
  

@register.filter
def m2toping(value):
  newlist=[]
  try:
    return value * Decimal(float(0.3025))
  except:
    newlist.append(0)


    
# 判斷是否為兩週內 
@register.filter
def less_two_week(auctionDate):
  # 取得目前的日期，要用form dateteim import datetime,不可用import datetime
  today = datetime.now()
  # 修改對應日期的格式
  auctionDateValue = datetime.strptime(auctionDate,'%Y-%m-%d')
  DateValue = (auctionDateValue-today).days + 1
  if DateValue >= 0 and DateValue <= 14 :
    return "兩週內(" + str(DateValue) + ")"
  
# 取最大值
# 用法 {% add_two 66 185 %}
@register.simple_tag(name='add_two')
def maxvalue(arg1 ,arg2):
  newlist=[]
  try:
    maxx = max(arg1 ,arg2)
    return maxx
  except:
    newlist.append(0)

# 最終判定取後三個字
@register.filter
def last_string(string):
  strvalue = string[1:]
  return strvalue
