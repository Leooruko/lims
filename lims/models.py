from django.db import models

# Create your models here.
class Sample(models.Model):    
    registered=models.DateTimeField(auto_now_add=True)
    sampleId=models.CharField(max_length=150)
    sampleName=models.CharField(max_length=150)
    industry=models.CharField(max_length=150)
    client=models.CharField(max_length=150)
    phoneNumber=models.CharField(max_length=150)
    stage=models.CharField(max_length=150)
    analysisStart=models.DateTimeField(blank=True, null=True)
    analysisEnd=models.DateTimeField(blank=True, null=True)
    analysis=models.CharField(max_length=5000,blank=True, null=True)
    recommended=models.DateTimeField(blank=True, null=True)
    recommendation=models.CharField(max_length=5000,blank=True, null=True)
    invoiced=models.DateTimeField(blank=True, null=True)


class Results(models.Model):
    sampleId=models.CharField(max_length=150)
    results_pdf=models.FileField(upload_to='pdfs/results',null=True,blank=True)
    
class Invoices(models.Model):    
    sampleId=models.CharField(max_length=150)
    invoice_pdf=models.FileField(upload_to='pdfs/invoices',null=True,blank=True)