from django.urls import path
import lims.views

urlpatterns=[
    path(r'samples/',lims.views.sample_list),
    path(r'samples/<int:pk>/',lims.views.sample_detail),
    path(r'sample-dashboard/', lims.views.sample_dashboard),
    path(r'stages/<str:stage>/',lims.views.samples_by_stage),
    path(r'results/',lims.views.results),
    path(r'invoices/',lims.views.invoices)
]