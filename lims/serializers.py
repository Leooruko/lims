from rest_framework import serializers
from lims.models import Sample,Results,Invoices

class SampleSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True) 
    class Meta:
        model=Sample
        fields=(
            'pk',
            'sampleId',
            'sampleName',
            'industry',
            'client',
            'phoneNumber',
            'stage',
            'analysisStart',
            'analysisEnd',
            'analysis',
            'recommended',
            'recommendation',
            'invoiced',
        )
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
    
class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        pk=serializers.IntegerField(read_only=True)
        model=Results
        fields=('sampleId','results_pdf',)

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        pk=serializers.IntegerField(read_only=True)
        model=Invoices
        fields=['sampleId','invoice_pdf',]