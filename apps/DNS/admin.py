from django.contrib import admin

from DNS.models import *
from django.forms import ModelForm,ValidationError


class KeyAdminForm(ModelForm):
    def clean_data(self):
        return self.cleaned_data["data"]


class KeyAdmin(admin.ModelAdmin):
    form = KeyAdminForm
    list_display = ['name', 'data', 'algorithm']


class BindZoneAdmin(admin.ModelAdmin):
    list_display = ['zonename']
    #filter_horizontal = ('default_transfer_zone',)

    # def get_default_transfer_zones(self,obj):
    #     return "\n".join([p.name for p in obj.default_transfer_zone.all()])


class BindServerAdmin(admin.ModelAdmin):
    list_display =['hostname','get_views']

    def get_views(self, obj):
        hostname = obj.hostname
        view_list = BindView.objects.filter(server__hostname=str(hostname))
        return "\n".join([v.viewname for v in view_list.all()])


class BindViewAdmin(admin.ModelAdmin):
    list_display = ['default_transfer_key','name','viewname', 'server', 'get_default_transfer_views']
    filter_horizontal = ('default_transfer_view',)

    def get_default_transfer_views(self, obj):
        return "\n".join([p.zonename for p in obj.default_transfer_view.all()])




class BindRecordAdmin(admin.ModelAdmin):
    list_display = ['name','Type','ttl','Data','get_default_transfer_zones']
    filter_horizontal = ('bindview',)
    def get_default_transfer_zones(self,obj):
        return "\n".join([p.zonename for p in obj.bindzone.all()])

admin.site.register(BindServer, BindServerAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(BindRecord,BindRecordAdmin)
admin.site.register(BindZone,BindZoneAdmin)
admin.site.register(BindView, BindViewAdmin)
