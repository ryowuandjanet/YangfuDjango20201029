from urllib.parse import quote
from decimal import *
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
  return value * arg

@register.filter
def m2toping(value):
  newlist=[]
  try:
    return value * Decimal(float(0.3025))
  except:
    newlist.append(0)

@register.filter
def lessfourteen(value):
  if value >= 0 and value <= 14:
    return True

@register.filter
def plusvaluetotal(value,arg1,arg2,arg3,arg4,arg5,arg6):
  newlist=[]
  if arg1 == 0:
    return 1
  # if arg2 == 0:
  #   return 1
  # if arg3 == 0:
  #   return 1
  # if arg4 == 0:
  #   return 1
  # if arg5 == 0:
  #   return 1
  # if arg6 == 0:
  #   return 1
  try:
    return value * Decimal(1+float(arg1))
    # return value * Decimal(1+float(arg1)) * Decimal(1+float(arg2)) * Decimal(1+float(arg3)) * Decimal(1+float(arg4)) * Decimal(1+float(arg5)) * Decimal(1+float(arg6))
  except:
    newlist.append(0)