from django.db import models

class Company(models.Model):
    company = models.CharField(max_length=20,blank=True)
    owner=models.CharField(max_length=20,blank=True)
    year = models.IntegerField(null=True,default=0)
    rating = models.FloatField(null=True,default=0.0)

    def __str__(self):
        return self.company

class ProjectManager(models.Model):
    company = models.ForeignKey(Company,verbose_name="Company",on_delete=models.CASCADE)
    manager = models.CharField(max_length=20,blank=True)
    project_list = models.CharField(max_length=20,blank=True)
    experience = models.IntegerField(null=True)
    client_call = models.IntegerField(null=True)

    def __str__(self):
       return self.manager


class Lead(models.Model):
    name = models.CharField(max_length=20,blank=True)
    project = models.CharField(max_length=20,blank=True)
    experience = models.IntegerField(null=True)
    client_call_expe = models.IntegerField(null=True)

    def __str__(self):
       return self.name




class Developer(models.Model):
    name = models.CharField(max_length=20,blank=True)
    project = models.CharField(max_length=20,blank=True)
    experience = models.IntegerField(null=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True,related_name="developer_leads")
    project_manager = models.ForeignKey(ProjectManager,on_delete=models.CASCADE,null=True,blank=True,related_name="developer_project_managers")


    def __str__(self):
       return self.name




class Developers(models.Model):
    developer =(
        ('Python','Python'),
        ('Java','Java'),
        ('NodeJs','NodeJs'),
        ('Blockchain','Blockchain')

    )
    name = models.CharField(max_length=20,blank=True)
    project = models.CharField(max_length=20,blank=True)
    experience = models.IntegerField(null=True)
    developer = models.CharField(max_length = 30, choices=developer,default="Python")
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True,related_name="developer_lead")
    project_manager = models.ForeignKey(ProjectManager,on_delete=models.CASCADE,null=True,blank=True,related_name="developer_project_manager")

    def __str__(self):
       return self.name
