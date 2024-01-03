import django
import os
from django.conf import settings
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Configure Django settings
settings.configure(
    DEBUG=True,
    # Add other necessary settings...
)
django.setup()

from datetime import datetime
from django.utils import timezone
from io import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lims.models import Sample
from lims.serializers import SampleSerializer

sample1=Sample(sampleId='PS01',sampleName='water',industry='effluents',client='Kimfey',phoneNumber='0711223713',stage='registeration')
sample1.save()
sample2=Sample(sampleId='PS02',sampleName='water',industry='effluents',client='Kimfey',phoneNumber='0711223713',stage='registeration')
sample2.save()

json_renderer=JSONRenderer()
serializer_sample1=SampleSerializer(sample1)
sample1_json_renderer=json_renderer.render(serializer_sample1.data)
print(sample1_json_renderer)

serializer_sample2=SampleSerializer(sample2)
sample2_json_renderer=json_renderer.render(serializer_sample2.data)
print(sample2_json_renderer)

json_new_sample='{"sampleId":"PS04","sampleName":"water","industry":"effluent","client":"Leon","phoneNumber":"0722294013","stage":"registeration"}'
json_bytes_new_sample=bytes(json_new_sample,encoding="UTF-8")
stream_new_sample=BytesIO(json_bytes_new_sample)
parser=JSONParser()
parsed_new_sample=parser.parse(stream_new_sample)
print(parsed_new_sample)  
new_sample_serializer=SampleSerializer(data=parsed_new_sample)
if new_sample_serializer.is_valid():
    sample3=new_sample_serializer.save()
    print(sample3.sampleName)
