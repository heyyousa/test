from django.db import models

class Userinfo(models.Model):
    id=models.CharField('工号',primary_key=True,max_length=6)
    name=models.CharField('姓名',max_length=10)
    sex=models.CharField('性别',max_length=4)
    password=models.CharField('密码',max_length=50)
    keshi=models.CharField('科室',max_length=50)
    duty=models.CharField('职务',max_length=20)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('更新时间',auto_now=True)

    # 表名自定义
    class Meta:
        db_table='userinfo'
        verbose_name_plural='用户信息'

    # admin界面的显示哪些数据及格式
    def __str__(self):
        return '%s | %s | %s | %s | %s'%(self.id,self.name,self.sex,self.keshi,self.duty)

class Userworklog(models.Model):
    id=models.CharField('工号',max_length=6)
    index=models.CharField('索引',primary_key=True,max_length=8)
    date=models.DateField('日期')
    needs=models.CharField('系统需求',max_length=4)
    place=models.CharField('科室',max_length=30)
    qsort=models.CharField('问题类型',max_length=16)
    qdescribe=models.CharField('问题描述',max_length=30)
    fisstatu=models.CharField('完成情况',max_length=10)
    note=models.CharField('备注',max_length=60)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        db_table='Userworklog'
        verbose_name_plural='工作日志'

    def __str__(self):
        return '%s | %s | %s | %s| %s | %s | %s | %s '%(self.id,self.date,self.needs,self.place,self.qsort,self.qdescribe,self.fisstatu,self.note)