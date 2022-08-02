from django.conf.urls import url
from . import views

app_name = 'billing'
urlpatterns = [

          url(r'^bill_add/(?P<visit_id>\d+)/$', views.add_bill, name='add_bill'),

          url(r'^billing_update/(?P<visit_id>\d+)/$', views.bill_update, name='update_bill'),
          url(r'^bill/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
          r'(?P<bill>[-\d]+)/$',
          views.bill_detail,
          name='bill_detail'),
          url(r'^(?P<pk>\d+)/bill/$', views.get_bill, name='bill'),
          url(r'^(?P<pk>\d+)/invoice/$', views.BillItemUpdateView.as_view(), name='invoice_update'),
          url(r'^lab_bills/', views.lab_bills, name='lab_bills'),
          url(r'^(?P<labbill_id>\d+)/confirm_payment/$', views.confirm_payment, name='confirm_pay'),
          url(r'^coupon/(?P<bill_id>\d+)$', views.coupon_apply, name='apply'),
          url(r'^bills/', views.bills, name='bills'),
          url(r'^(?P<bill_id>\d+)/confirm_pay/$', views.confirm_pay, name='confirm_payment'),


]




