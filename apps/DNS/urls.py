from django.conf.urls import url,include
from DNS.views import ZoneDetail,ViewZone,ServerViews,ViewList,ZoneList,view_add_record,view_edit_record,view_delete_record

urlpatterns = [
    #url(r'^server_list/$', ServerList.as_view(),name='server_list'),
    url(r'^server_view_list/$', ServerViews.as_view(),name='server_view_list'),
    url(r'^view_list/$', ViewList.as_view(),name='view_list'),
    url(r'^view_zone_list/(?P<view_id>\d+)/$',ViewZone.as_view(),name='view_zone_list'),
    url(r'^zone_list/$', ZoneList.as_view(),name='zone_list'),
    url(r'^zone_record_list/(?P<view_id>\d+)/(?P<zone_id>\d+)/$', ZoneDetail.as_view(),name='zone_record_list'),
    url(r'^add_record/(?P<view_id>\d+)/(?P<zone_id>\d+)/$',view_add_record,name='add_record'),
    #url(r'^edit_record/(?P<server_id>\d+)/(?P<view_id>\d+)/(?P<zone_id>\d+)/$',view_edit_record.as_view(),name='edit_record'),
    url(r'^edit_record/(?P<view_id>\d+)/(?P<zone_id>\d+)/(?P<record_id>\d+)/(?P<record_name>[\S+]+)/(?P<record_type>[\S+]+)/(?P<record_ttl>[\S+]+)/(?P<record_data>[\S+]+)/$',view_edit_record, name="edit_record"),
    url(r'^delete_record/(?P<view_id>\d+)/(?P<zone_id>\d+)/$',view_delete_record,name='delete_record'),



]