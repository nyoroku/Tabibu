from django.conf.urls import url
from . import views
from .views import TestAutocomplete


app_name = 'TabibuNet'
urlpatterns = [



    url(r'^add_patient/', views.PatientCreate.as_view(), name='patient_add'),
    url(r'^list_patient/', views.PatientListView.as_view(), name='patient_list'),
    url(r'^waiting_for_provider/', views.waiting_for_provider, name='waiting_for_provider'),
    url(r'^waiting_for_lab/', views.wait_for_lab, name='waiting_for_lab'),
    url(r'^waiting_for_pharmacy/', views.wait_for_pharmacy, name='waiting_for_pharmacy'),
    url(r'^patient/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<patient>[-\w]+)/$',
           views.patient_detail,
           name='patient-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.PatientUpdateView.as_view(), name='patient_edit'),
    url(r'^edit/(?P<patient_id>\d+)/$', views.edit, name='info_edit'),
    url(r'^visit_add/(?P<patient_id>\d+)/$', views.add_visit, name='add_visit'),
    url(r'^visit_list/', views.VisitListView.as_view(), name='visit_list'),
    url(r'^invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    url(r'^visit/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<visit>[-\w]+)/$',
           views.visit_detail,
           name='visit-detail'),

    url(r'^visit_update/(?P<visit_id>\d+)/$', views.edit_visit, name='edit_visit'),
    url(r'^lab_update/(?P<labtest_id>\d+)/$', views.edit_test, name='edit_lab'),
    url(r'^(?P<pk>\d+)/medications/$', views.PrescriptionMedicationUpdateView.as_view(), name='prescription_update'),
    url(r'^(?P<pk>\d+)/invoice/$', views.VisitInvoiceUpdateView.as_view(), name='invoice_update'),
    url(r'^test_add/(?P<visit_id>\d+)/$', views.add_test, name='add_test'),
    url(r'^lab_test/(?P<visit_id>\d+)/$', views.lab_test, name='lab_test'),
    url(r'^provider_to_lab/(?P<visit_id>\d+)/$', views.provider_to_lab, name='provider_to_lab'),
    url(r'^obs_add/(?P<visit_id>\d+)/$', views.add_obs, name='add_obs'),
    url(r'^test/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<test>[-\w]+)/$',
           views.test_detail,
           name='test-detail'),
    url(r'^ob/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<ob>[-\w]+)/$',
           views.ob_detail,
           name='ob-detail'),
    url(r'^search/$', views.patient_filter, name='search_patient'),
    url(r'^(?P<visit_id>\d+)/sender_to_provider/$', views.send_to_provider, name='send_to_provider'),
    url(r'^(?P<visit_id>\d+)/provider_to_pharmacy/$', views.provider_to_pharmacy, name='provider_to_pharmacy'),
    url(r'^(?P<visit_id>\d+)/provider/$', views.provider, name='provider'),
    url(r'^(?P<labtest_id>\d+)/lab/$', views.lab, name='lab'),
    url(r'^(?P<prescription_id>\d+)/pharmacy/$', views.pharmacy, name='pharmacy'),
    url(r'^(?P<labtest_id>\d+)/lab_to_provider/$', views.lab_to_provider, name='lab_to_provider'),
    url(r'^(?P<labtest_id>\d+)/lab_to_pharmacy/$', views.lab_to_pharmacy, name='lab_to_pharmacy'),
    url(r'^(?P<labtest_id>\d+)/ready_to_close/$', views.lab_to_close, name='lab_to_close'),
    url(
        r'^test-autocomplete/$',
        TestAutocomplete.as_view(),
        name='test-autocomplete',
    ),
    url(r'^labtest/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<labtest>[-\w]+)/$',
        views.labtest_detail,
        name='labtest-detail'),
    url(r'^(?P<pk>\d+)/prescriptions/$', views.prescription_detail, name='prescription'),




]