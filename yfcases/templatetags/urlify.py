# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

# 民國年份
@register.filter
def chinese_year(chinese_date):
  if chinese_date:
    return int(chinese_date.year)-1911

# 數字改為中文    
@register.filter   
def num2cn2(number, traditional=False): 
  """ 
  數字轉換成中文（簡體和繁體，目前支持到12位數值） 
  :param number: 
  :param traditional:
  :return: 
  """ 
  if traditional: 
    chinese_num = {0: '零', 1: '壹', 2: '貳', 3: '叄', 4: '肆', 5: '伍', 6: '陸', 7: '柒', 8: '捌', 9: '玖'} 
    chinese_unit = ['仟', '', '拾', '佰'] 
  else: 
    chinese_num = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'} 
    chinese_unit = ['千', '', '十', '百'] 
  extra_unit = ['', '萬', '億'] 
  num_list = list(str(number)) 
  num_cn = [] 
  zero_num = 0 # 連續0的個數 
  prev_num = '' # 遍歷列表中當前元素的前一位 
  length = len(num_list) 
  for num in num_list: 
    tmp = num 
    if num == '0': # 如果num為0，記錄連續0的數量 
      zero_num += 1 
      num = '' 
    else: 
      zero = '' 
      if zero_num > 0: 
        zero = '零' 
      zero_num = 0 
      # 處理前一位數字為0，後一位為1，並且在十位數上的數值
      if prev_num in ('0', '') and num == '1' and chinese_unit[length % 4] in ('十', '拾'): 
        num = zero + chinese_unit[length % 4] 
      else: 
        num = zero + chinese_num.get(int(num)) + chinese_unit[length % 4] 
    if length % 4 == 1: # 每隔4位加'萬'、'億'拼接 
      if num == '零': 
        num = extra_unit[length // 4] 
      else: 
        num += extra_unit[length // 4] 
    length -= 1 
    num_cn.append(num) 
    prev_num = tmp 
  num_cn = ''.join(num_cn) 
  return num_cn

