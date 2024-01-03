from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Sample,Results,Invoices
from .serializers import SampleSerializer,ResultsSerializer,InvoiceSerializer
from datetime import date
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
import io
from django.http import Http404

# Create your views here.

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def sample_list(request):
    if request.method=='GET':
        samples=Sample.objects.all()
        sample_serializer=SampleSerializer(samples,many=True)
        return JSONResponse(sample_serializer.data)
    elif request.method=='POST':
        sample_data=JSONParser().parse(request)
        sample_serializer=SampleSerializer(data=sample_data)
        if sample_serializer.is_valid():
            sample_serializer.save()
            return JSONResponse(sample_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(sample_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
def sample_detail(request, pk):
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sample_serializer = SampleSerializer(sample)
        return JSONResponse(sample_serializer.data)
    elif request.method == 'PUT':
        sample_data = JSONParser().parse(request)
        sample_serializer = SampleSerializer(sample, data=sample_data, partial=True)  # Use partial=True
        if sample_serializer.is_valid():
            sample_serializer.save()
            return JSONResponse(sample_serializer.data)
        return JSONResponse(sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sample.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    # If the method is not supported, return a response indicating that
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def samples_by_stage(request, stage):
    # Define the stages based on the criteria you provided
    stages = {
        'registration': {'analysisStart__isnull': True, 'analysisEnd__isnull': True},
        'analysis': {'analysisStart__isnull': False, 'analysisEnd__isnull': True},
        'recommendation': {'analysisEnd__isnull': False, 'invoiced__isnull': True},
        'invoice_complete': {'invoiced__isnull': False}
    }

    # Retrieve samples based on the specified stage
    stage_criteria = stages.get(stage, {})
    samples = Sample.objects.filter(**stage_criteria)

    # Serialize the samples data to JSON
    serialized_samples = [{'sampleId': sample.sampleId, 'stage': sample.stage} for sample in samples]

    return JSONResponse({'samples': serialized_samples})

@csrf_exempt
def sample_dashboard(request):
    today = date.today()

    new_samples = Sample.objects.filter(registered__date=str(today)).count()
    total_samples = Sample.objects.count()
    analysis_stage_samples = Sample.objects.filter(stage='analysis').count()
    recommended_samples = Sample.objects.exclude(recommended=None).count()
    analysed_samples = Sample.objects.exclude(analysisEnd=None).count()

    data = {
        'new_samples': new_samples,
        'total_samples': total_samples,
        'analysis_stage_samples': analysis_stage_samples,
        'recommended_samples': recommended_samples,
        'analysed_samples': analysed_samples,
    }

    return JSONResponse(data)



@csrf_exempt
def results(request):
    if request.method == 'GET':
        results = Results.objects.all()
        serializer = ResultsSerializer(results, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        results_data = JSONParser().parse(request)
        pdf_data = generate_results_pdf(request, results_data['sampleId'])
        serializer = ResultsSerializer(data=pdf_data)  # Use ResultsSerializer instead of passing raw data
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@csrf_exempt
def invoices(request):
    if request.method == 'GET':
        invoices = Invoices.objects.all()
        serializer = InvoiceSerializer(invoices,many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        invoice_data = JSONParser().parse(request)
        # sample_id = invoice_data['sampleId']        
        pdf_data =  generate_invoice_pdf(request,invoice_data['sampleId'])
        serializer = InvoiceSerializer(data=pdf_data)  # Use InvoiceSerializer
        if serializer.is_valid():  # Call is_valid() on the serializer instance
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@csrf_exempt
def generate_results_pdf(request, sample_id):
    try:
        # Fetch sample data from the database
        sample = Sample.objects.get(sampleId=sample_id)

        # Create the PDF content
        pdf_content = io.BytesIO()
        p = canvas.Canvas(pdf_content)
        p.drawString(100, 800, f"Results for Sample {sample.sampleId}")
        p.drawString(100, 780, f"Analysis: {sample.analysis}")
        p.drawString(100, 760, f"Recommendation: {sample.recommendation}")
        # Add more content as needed
        p.showPage()
        p.save()

        # Save the PDF content in the Results model
        results_instance = Results.objects.create(sampleId=sample_id)
        results_instance.results_pdf.save(f"results_{sample_id}.pdf", ContentFile(pdf_content.getvalue()))

        # Return a dictionary with necessary data
        return {'sampleId': sample_id, 'results_pdf': results_instance.results_pdf}
    except Sample.DoesNotExist:
        raise Http404("Sample does not exist")



@csrf_exempt
def generate_invoice_pdf(request, sample_id):
    try:
        # Fetch sample data from the database
        sample = Sample.objects.get(sampleId=sample_id)

        # Create the PDF content
        pdf_content = io.BytesIO()
        p = canvas.Canvas(pdf_content)
        p.drawString(100, 800, f"Invoice for Sample {sample.sampleId}")
        p.drawString(100, 780, f"Invoice: {sample.invoiced}")
        # Add more content as needed
        p.showPage()
        p.save()

        # Save the PDF content in the Invoices model
        invoice_instance = Invoices.objects.create(sampleId=sample_id)
        invoice_instance.invoice_pdf.save(f"invoice_{sample_id}.pdf", ContentFile(pdf_content.getvalue()))

        # Return a dictionary with necessary data
        return {'sampleId': sample_id, 'invoice_pdf': invoice_instance.invoice_pdf}

    except Sample.DoesNotExist:
        raise Http404("Sample does not exist")
