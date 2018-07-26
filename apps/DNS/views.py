# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import BindServer,BindView,BindZone,BindRecord
from django.shortcuts import get_object_or_404, redirect, render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View
from forms import FormAddRecord,FormDeleteRecord
from DNS import helpers
from DNS.exceptions import KeyringException, RecordException, TransferException, ZoneException
from django.contrib import messages

# Create your views here.

# class ServerList(View):
#     def get(self,request):
#
#         server_list = BindServer.objects.all().order_by('hostname')
#
#         return render(request,'server_list.html',{
#             "server_list":server_list,
#             #"all_server":all_server
#
#         })
def serverviews(request):
    #server = BindServer.objects.get(id=int(server_id))
    Server_views_list = BindView.objects.all()
    content = {"Server_views_list":Server_views_list}
    return content

class ServerViews(View):
    def get(self,request):
        #server = BindServer.objects.get(id=int(server_id))
        server_views_list = BindView.objects.all()

        return render(request,'server_view_list.html',{
           #"server":server,
            "server_views_list":server_views_list
            #'view_zone_list':view_zone_list

        })

class ViewList(View):
    def get(self,request):
        view_server=BindServer.objects.all().order_by("hostname")
        return render(request,'list_views.html',{
            "view_server":view_server,
        })


class ViewZone(View):
    def get(self,request,view_id):
        #server_id = int(server_id)
        views = BindView.objects.get(id=int(view_id))
        view_zone_list = views.default_transfer_view.all()

        return render(request,'view_zone_list.html',{
            #"server_id":server_id,
            "views":views,
            'view_zone_list':view_zone_list
            #"view_server":view_server
        })
#
class ZoneList(View):
    def get(self,request):
        zone_list = BindZone.objects.all().order_by("zonename")
        return render(request,'list_zone.html',{
            "zone_list":zone_list
        })



class ZoneDetail(View):
    def get(self,request,view_id,zone_id):
        #l1=[]
        #server_id=server_id
        view_id=view_id
        zone_id=zone_id
        views = BindView.objects.get(id=int(view_id))
        key=views.default_transfer_key.id
        Server = BindServer.objects.all()
        zone = BindZone.objects.get(id=int(zone_id))
        #all_record = zone.bindrecord_set.filter(bindzone__bindview__default_transfer_view_id=int(view_id))
        #zon_set = views.default_transfer_view.all()
        all_record=BindRecord.objects.filter(bindview=views)



        try:
            page = request.GET.get('page',1)

        except PageNotAnInteger:
            page =1

        p=Paginator(all_record,10,request=request)
        records=p.page(page)

        return render(request, 'zone_record_list.html', {

            "Server":Server,
            #"server_id":server_id,
            "views":views,
            "view_id":view_id,
            "zone":zone,
            "zone_id":zone_id,
            "all_record":records

        })


def view_add_record(request,view_id,zone_id):
    #server_id = server_id
    view_id = view_id
    zone_id=zone_id
    views = BindView.objects.get(id=int(view_id))
    server = BindServer.objects.all()[0]
    zone = BindZone.objects.get(id=int(zone_id))
    key_name = str(BindView.objects.filter(id=view_id)[0].default_transfer_key.name)

    if request.method == 'POST':

        form =FormAddRecord(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data
            record_name=str(form_cleaned['record_name'])
            record_type=str(form_cleaned['record_type'])
            ttl=form_cleaned['ttl']
            record_data=str(form_cleaned['record_data'])
            #zonee=BindZone.objects.filter(id=int(zone_id))[0]
            #key_name = BindView.objects.filter(view_id)[0].default_transfer_key.name
            zonee=BindView.objects.filter(id=int(views.id))[0]

            try:
                helpers.add_Record(server,zone,record_name, record_type, ttl, record_data, key_name)

            except (KeyringException,RecordException) as exc:
                messages.error(request, "Adding %s.%s failed: %s" %
                               (form_cleaned['record_name'], zone, exc))
            else:
                messages.success(request, "%s.%s was added successfully." %
                                 (form_cleaned['record_name'],zone))
                record_obj=BindRecord.objects.create(
                    name=record_name,
                    Type=record_type,
                    ttl=ttl,
                    Data=record_data,
                   #bindzone_id=int(zone_id),
                )
                record_obj.bindview.add(views)
                return redirect('DNS:zone_record_list',view_id=view_id,zone_id=zone_id)
        else:
            messages.error(request, "Form data was invalid. Check all inputs.")
    else:
        server = BindServer.objects.all()[0]
        key_name = str(BindView.objects.filter(id=view_id)[0].default_transfer_key.name)
        form=FormAddRecord(initial={


            'server':server,
            "key_name":key_name
        })
    return render(request,'add_record.html',{
        "views": views,
        "view_id":view_id,
        "server": server,
        "zone_id":zone_id,
        "zone": zone,
        "key_name":key_name,
        "form":form

    })




def view_edit_record(request,view_id,zone_id,record_id,record_name=None,record_type=None,record_data=None,record_ttl=None):
    #server_id = server_id
    view_id = view_id
    zone_id = zone_id
    record_id = record_id
    views = BindView.objects.get(id=int(view_id))
    server = BindServer.objects.all()[0]
    zone = BindZone.objects.get(id=int(zone_id))
    record = BindRecord.objects.get(id=int(record_id))
    #all_record = zone.bindrecord_set.all()
    key_name = str(BindView.objects.filter(id=view_id)[0].default_transfer_key.name)
    if request.method == 'POST':
        form = FormAddRecord(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data

            record_name = str(form_cleaned['record_name'])
            record_type = str(form_cleaned['record_type'])
            ttl = form_cleaned['ttl']
            record_data = str(form_cleaned['record_data'])
            zone = str(BindZone.objects.filter(id=int(zone_id))[0])


            try:
                helpers.edit_Record(server, zone, record_name, record_type, ttl, record_data, key_name)
            except (KeyringException, RecordException) as exc:
                messages.error(request, "Modifying %s.%s failed: %s" %
                               (form_cleaned['record_name'], zone, exc))
            else:
                messages.success(request, "%s.%s was modified successfully." %
                                 (form_cleaned['record_name'], zone))
                BindRecord.objects.filter(id=int(record_id)).update(
                    name=record_name,
                    Type=record_type,
                    ttl=ttl,
                    Data=record_data,
                )


                return redirect('DNS:zone_record_list',
                            #erver_id=server_id,
                            view_id=view_id,
                            zone_id=zone_id

                            )
        else:

            messages.error(request, "Form data was invalid. Check all inputs.")

    else:
        form = FormAddRecord(initial={"record_name": record_name,
                                      "record_type": record_type,
                                      "ttl": record_ttl,
                                      "record_data": record_data
                                      })
    return render(request, 'edit_record.html', {

            #'server_id': server_id,
            "views": views,
            "view_id": view_id,
            "server": server,
            "zone_id": zone_id,
            "zone": zone,
            "record_id": record_id,
            "record": record,
            #"all_record": all_record,
            "key_name":key_name,
            "form": form

        })

def view_delete_record(request,view_id,zone_id):
    #server_id = server_id

    view_id = view_id
    zone_id = zone_id
    views = BindView.objects.get(id=int(view_id))
    server = BindServer.objects.all()[0]
    zone = BindZone.objects.get(id=int(zone_id))
    all_record = BindRecord.objects.filter(bindview=views)
    key_name = BindView.objects.filter(id=view_id)[0].default_transfer_key.name
    rr_list = request.POST.getlist("rr_list")

    if len(rr_list) == 0:
        messages.error(request,"Select at least one record for deletion.")
        return redirect('DNS:zone_record_list',view_id=view_id,zone_id=zone_id)

    if request.method == 'POST':
        form=FormDeleteRecord(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data

            rr_list = form_cleaned["rr_list"]

            zone = BindZone.objects.filter(id=int(zone_id))[0]
            for record in rr_list:
                record_name=BindRecord.objects.filter(name=record.rsplit(" ")[1],Type=record.rsplit(" ")[3],Data=record.rsplit(" ")[4])

                try:

                    helpers.delete_Record(server, zone,record_name[0].name,record_name[0].Type,record_name[0].Data,key_name)
                except (KeyringException, RecordException) as exc:
                    messages.error(request, "Deleting %s.%s failed: %s" %
                                   (record_name, zone, exc))
                else:
                    messages.success(request, "%s.%s was removed successfully." %
                                     (record_name, zone))
                BindRecord.objects.filter(id=int(record_name[0].id)).delete()

            return redirect('DNS:zone_record_list',
                            #server_id=server_id,
                        view_id=view_id,
                        zone_id=zone_id
                        )
        else:

            messages.error(request, "Form data was invalid. Check all inputs.")
    else:
        form = FormDeleteRecord(initial={"rr_list": rr_list})
    return render(request, 'delete_record.html', {

           # 'server_id': server_id,
            "views": views,
            "view_id": view_id,
            "server": server,
            "zone_id": zone_id,
            "zone": zone,
            "all_record": all_record,
            "key_name":key_name,
            "rr_list":rr_list,
            "form": form
        })





























