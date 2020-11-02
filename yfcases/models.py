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
    
    # (1)建物(非公設、非增建)持分後總面積
  def get_build_holding_point_area_group_total(self):
    newlist=[]
    try:
      getBuildHoldingPointAreaGroupTotal=0
      for getBuildHoldingPointAreaGroup in self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設"):
        getBuildHoldingPointAreaGroupTotal = getBuildHoldingPointAreaGroupTotal + getBuildHoldingPointAreaGroup.get_build_holding_point_area()
      return getBuildHoldingPointAreaGroupTotal
    except:
      newlist.append(0)

  # (2)建物(公設)持分後總面積
  def get_build_holding_point_public_group_total(self):
    getBuildHoldingPointPublicGroupTotal=0
    for getBuildHoldingPointPublicGroup in self.builds.filter(buildTypeUse="公設"):
      getBuildHoldingPointPublicGroupTotal = getBuildHoldingPointPublicGroupTotal + getBuildHoldingPointPublicGroup.get_build_first_not_add_and_not_public_holding_point_area()
    return getBuildHoldingPointPublicGroupTotal

  # (3)建物(增建)持分後總面積
  def get_build_holding_point_add_group_total(self):
    try:
      getBuildHoldingPointAddGroupTotal=0
      for getBuildHoldingPointAddGroup in self.builds.filter(buildTypeUse="增建-持分後坪數打對折"):
        getBuildHoldingPointAddGroupTotal = getBuildHoldingPointAddGroupTotal + getBuildHoldingPointAddGroup.get_after_add_holding_point_area()
      return getBuildHoldingPointAddGroupTotal
    except ZeroDivisionError:
      return 0

  # 上述(1)+(2)+(3)
  def get_build_holding_point_after_group_total(self):
    newlist=[]
    try:
      return self.get_build_holding_point_area_group_total() + self.get_build_holding_point_public_group_total() + self.get_build_holding_point_add_group_total()
    except:
      newlist.append(0)

    
class Land(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='lands',on_delete=models.CASCADE)
  landNumber=models.CharField(u'地號',max_length=100,null=True,blank=True)
  landUrl=models.URLField(u'謄本',max_length=200,null=True,blank=True)
  landArea=models.DecimalField(u'地坪(平方公尺)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  landHoldingPointPersonal=models.DecimalField(u'個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  landHoldingPointAll=models.DecimalField(u'所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  landRemarks=models.CharField(u'備註',max_length=100,null=True,blank=True)
  landPresentValue=models.CharField(u'土地現值',max_length=100,null=True,blank=True)
  landTotalArea=models.DecimalField(u'地坪總面積',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  landAreaWidth=models.DecimalField(u'土地寬度',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  landAreaDepth=models.DecimalField(u'土地深度',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
		
  def __str__(self):
    return self.landNumber
  
  def get_land_holding_point_area(self):
    return self.landArea * ( self.landHoldingPointPersonal / self.landHoldingPointAll)
    
class Build(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='builds',on_delete=models.CASCADE)
  buildNumber=models.CharField(u'建號',max_length=100,null=True,blank=True)
  buildUrl=models.URLField(u'謄本',max_length=200,null=True,blank=True)
  buildArea=models.DecimalField(u'建坪(平方公尺)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  buildHoldingPointPersonal=models.DecimalField(u'個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  buildHoldingPointAll=models.DecimalField(u'所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  buildTypeUse=models.CharField(u'建物型',max_length=100,null=True,blank=True)
  buildUsePartition=models.CharField(u'使用分區',max_length=100,null=True,blank=True)

  def __str__(self):
    return self.buildNumber
    
  # 建物(非公設、非增建)各別面積
  def get_build_holding_point_area(self):
    newlist=[]
    try:
      return self.buildArea * ( self.buildHoldingPointPersonal / self.buildHoldingPointAll)
    except:
      newlist.append(0)

  # 建物(增建)各別面積
  def get_after_add_holding_point_area(self):
    newlist=[]
    try:
      return self.get_build_holding_point_area() / 2
    except:
      newlist.append(0)

  # 建物(公設)各別面積
  def get_build_first_not_add_and_not_public_holding_point_area(self):
    try:
      return self.buildArea * (self.buildHoldingPointPersonal / self.buildHoldingPointAll) * self.yfcase.get_first_not_add_and_not_public_holding_point_rate()
    except ZeroDivisionError:
      return 0
      
class Auction(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='auctions',on_delete=models.CASCADE)
  auctionDateFirst = models.CharField(u'拍賣日(第一拍)',max_length=100,null=True,blank=True)
  auctionDateSecond = models.CharField(u'拍賣日(第二拍)',max_length=100,null=True,blank=True)
  auctionDateThird = models.CharField(u'拍賣日(第三拍)',max_length=100,null=True,blank=True)
  auctionDateFourth = models.CharField(u'拍賣日(第四拍)',max_length=100,null=True,blank=True)
  auctionFloorPriceFirst = models.DecimalField(u'底價(第一拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceSecond = models.DecimalField(u'底價(第二拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceThird = models.DecimalField(u'底價(第三拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceFourth = models.DecimalField(u'底價(第四拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionClickFirst = models.DecimalField(u'點閱(第一拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickSecond = models.DecimalField(u'點閱(第二拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickThird = models.DecimalField(u'點閱(第三拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickFourth = models.DecimalField(u'點閱(第四拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorFirst = models.DecimalField(u'監控(第一拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorSecond = models.DecimalField(u'監控(第二拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorThird = models.DecimalField(u'監控(第三拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorFourth = models.DecimalField(u'監控(第四拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMarginFirst = models.DecimalField(u'保証金(第一拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginSecond = models.DecimalField(u'保証金(第二拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginThird = models.DecimalField(u'保証金(第三拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginFourth = models.DecimalField(u'保証金(第四拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)

  def get_ping_first_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFirst / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_second_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceSecond / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_third_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceThird / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_fourth_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFourth / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_first_cp(self):
    newlist=[]
    try:
      return  self.yfcase.pbk() / self.get_ping_first_price()
    except:
      newlist.append(0)

  def get_second_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_second_price()
    except:
      newlist.append(0)

  def get_third_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_third_price()
    except:
      newlist.append(0)

  def get_fourth_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_fourth_price()
    except:
      newlist.append(0)

  def get_suggestedincreaseFirst(self):
    newlist=[]
    try:
      suggestedincreaseFirst = (math.ceil(self.auctionClickFirst / 100)+self.auctionMonitorFirst) * 3 / 100
      if suggestedincreaseFirst > 0.15:
        return 0.15
      else:
        return suggestedincreaseFirst
    except:
      newlist.append(0)

  def get_suggestedincreaseSecond(self):
    newlist=[]
    try:
      suggestedincreaseSecond = (math.ceil(self.auctionClickSecond / 100)+self.auctionMonitorSecond) * 3 / 100
      if suggestedincreaseSecond > 0.15:
        return 0.15
      else:
        return suggestedincreaseSecond
    except:
      newlist.append(0)

  def get_suggestedincreaseThird(self):
    newlist=[]
    try:
      suggestedincreaseThird = (math.ceil(self.auctionClickThird / 100)+self.auctionMonitorThird) * 3 / 100
      if suggestedincreaseThird > 0.15:
        return 0.15
      else:
        return suggestedincreaseThird
    except:
      newlist.append(0)

  def get_suggestedincreaseFouth(self):
    newlist=[]
    try:
      suggestedincreaseFouth = (math.ceil(self.auctionClickFourth / 100)+self.auctionMonitorFourth) * 3 / 100
      if suggestedincreaseFouth > 0.15:
        return 0.15
      else:
        return suggestedincreaseFouth
    except:
      newlist.append(0)

  # 建議加價(第一拍)
  def get_suggestedincreaseFirst_floor_price(self):
    if self.auctionFloorPriceFirst != 0:
      return self.auctionFloorPriceFirst * Decimal( 1 + self.get_suggestedincreaseFirst())

  # 建議加價CP(第一拍)
  def get_suggestedincreaseFirst_cp(self):
    newlist=[]
    try:
      return self.get_first_cp() / Decimal( 1 + self.get_suggestedincreaseFirst())
    except:
      newlist.append(0)


  # 建議加價(第二拍)
  def get_suggestedincreaseSecond_floor_price(self):
    if self.auctionFloorPriceSecond !=0 and self.auctionFloorPriceSecond != 0:
      return self.auctionFloorPriceSecond * Decimal( 1 + self.get_suggestedincreaseSecond())

  # 建議加價CP(第二拍)
  def get_suggestedincreaseSecond_cp(self):
    newlist=[]
    try:
      return self.get_second_cp() / Decimal( 1 + self.get_suggestedincreaseSecond())
    except:
      newlist.append(0)

  # 建議加價(第三拍)
  def get_suggestedincreaseThird_floor_price(self):
    if self.auctionFloorPriceThird != 0:
      return self.auctionFloorPriceThird * Decimal( 1 + self.get_suggestedincreaseThird())
  # 建議加價CP(第三拍)

  def get_suggestedincreaseThird_cp(self):
    newlist=[]
    try:
      return self.get_third_cp() / Decimal( 1 + self.get_suggestedincreaseThird())
    except:
      newlist.append(0)

  # 建議加價(第四拍)
  def get_suggestedincreaseFourth_floor_price(self):
    newlist=[]
    try:
      if self.auctionFloorPriceFourth != 0:
        return self.auctionFloorPriceFourth * DecimalField( 1 + self.get_suggestedincreaseFouth())
    except:
      newlist.append(0)


  # 建議加價CP(第四拍)
  def get_suggestedincreaseFourth_cp(self):
    newlist=[]
    try:
      return self.get_fourth_cp() / Decimal( 1 + self.get_suggestedincreaseFouth())
    except:
      newlist.append(0)
