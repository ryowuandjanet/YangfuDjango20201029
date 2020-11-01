from django.db import models

class City(models.Model):
  name = models.CharField(max_length=30)

  def __str__(self):
    return self.name

  class Meta:
    # managed = True
    db_table = 'yfcase_city'

class Township(models.Model):
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  name = models.CharField(max_length=30)

  def __str__(self):
    return self.name
 
  class Meta:
      # managed = True
    db_table = 'yfcase_township'
        
class Yfcase(models.Model):
  yfcaseCaseNumber=models.CharField(u'案號(*)',max_length=100)
  yfcaseCompany=models.CharField(u'所屬公司',max_length=50,null=True,blank=True)
  yfcaseCity=models.ForeignKey(City,verbose_name = u'縣市',on_delete=models.SET_NULL,null=True)
  yfcaseTownship=models.ForeignKey(Township,verbose_name = u'鄉鎮區里', on_delete=models.SET_NULL, null=True)
  yfcaseBigSection=models.CharField(u'段號',max_length=10,null=True,blank=True)
  yfcaseSmallSection=models.CharField(u'小段',max_length=10,null=True,blank=True)
  yfcaseOtherAddress=models.CharField(u'其他住址',max_length=100,null=True,blank=True)
  yfcaseDebtor=models.CharField(u'債務人',max_length=10,null=True,blank=True)
  yfcaseCreditor=models.CharField(u'債權人',max_length=10,null=True,blank=True)
  user = models.ForeignKey('users.CustomUser',verbose_name = u'區域負責人', on_delete=models.CASCADE)

  def __str__(self):
    return self.yfcaseCaseNumber
    
  class Meta:
    # managed = True
    db_table = 'yfcase_yfcase'
