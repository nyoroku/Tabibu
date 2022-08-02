from django.conf.urls import url
from . import views

app_name = 'inpatient'
urlpatterns = [

          url(r'^admission_add/(?P<patient_id>\d+)/$', views.add_admission, name='add_admission'),
          url(r'^admission_list/', views.AdmissionListView.as_view(), name='admission_list'),
          url(r'^visit/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<admission>[-\w]+)/$',
           views.admission_detail,
           name='admission_detail'),
          url(r'^admission_update/(?P<admission_id>\d+)/$', views.edit_admission, name='edit_admission'),
          url(r'^test_add/(?P<admission_id>\d+)/$', views.add_test, name='add_test'),
          url(r'^obs_add/(?P<visit_id>\d+)/$', views.add_obs, name='add_obs'),
          url(r'^(?P<pk>\d+)/medication/$', views.AdmissionPrescriptionUpdateView.as_view(),
              name='medication_update'),

]
