# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile,LoginRecord,UserGroup
from .forms import LoginForm,ChangePassword,UserGroupForm,UserForm
import json

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user

        except Exception as e:
            return None


def UserIP(request):
    """获取用户IP"""
    ip = ''
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    return ip


class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
            if user:
                login(request,user)
                LoginRecord.objects.create(type=u"用户登录",user=request.user,action=u"用户登录",ip=UserIP(request),content="用户登录 %s" % request.user)
                return HttpResponseRedirect(reverse("index"))
        LoginRecord.objects.create(type=u"用户登录",user=request.POST.get('username'),action=u'用户登录',
                                   ip=UserIP(request),content=u"用户登录失败 %s" % request.POST.get('username'))
        return render(request,"login.html",{'form':form})



class LogoutView(View):
    """用户登出"""
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


@login_required
def change_password(request):
    user = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        form = ChangePassword(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            form = ChangePassword(instance=user)

        return render(request,'',{"form":form})


# class LoginView(View):
#     def get(self,request):
#         return render(request, "login.html",{})
#
#     def post(self,request):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user_name = request.POST.get("username","")
#             pass_word = request.POST.get("password","")
#             user = authenticate(username=user_name, password=pass_word)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse("index"))
#                 else:
#                     return render(request, "login.html", {"msg": "用户名未激活！"})
#             else:
#                 return render(request, "login.html", {"msg": "用户名或者密码错误！"})
#         else:
#             return render(request, "login.html", {"login_form": login_form})



class IndexView(LoginRequiredMixin,View):
    """首页"""
    def get(self,request):
        return render(request,'index.html',{})


class UserList(LoginRequiredMixin,View):
    def get(self,request):
        user_obj = UserProfile.objects.all()
        return render(request,'',{'user_obj':user_obj})


@login_required
def user_audit(request):
    """日志审计"""
    if request.user.is_superuser:
        logs = LoginRecord.objects.all()[:300]
        if request.method == 'GET':
            if request.GET.get('aid'):
                aid = request.get_full_path().split('=')[1]
                log_detail = LoginRecord.objects.filter(id=aid)
                return render(request,'',{'log_detail':log_detail})

        return render(request,'',{'all_logs':logs})
    else:
        raise page_not_found


class UserAdd(LoginRequiredMixin,View):
    def get(self,request):
        form =UserForm()
        return render(request,'',{'form':form})

    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('passowrd2')
            group_select = request.POST.getlist('group_sel')
            group_delete = request.POST.getlist('group_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            if password1 and password1 == password2:
                form.save()
                user = get_object_or_404(UserProfile,username=username)
                user.set_password(password1)
                user.save()
                #添加用户至UserGroup
                user.groups.add(*group_select)
                user.groups.remove(*group_delete)
                #授权用户权限
                user.user_permissions.add(*perm_select)
                user.user_permissions.remove(*perm_delete)
                return HttpResponseRedirect(reverse(""))

        else:
            return render(request,"")


class UserEdit(LoginRequiredMixin,View):
    def get(self,request,aid):
        user_obj = UserProfile.objects.filter(id=aid).first()
        form = UserForm(instance=user_obj)
        return render(request,'',{'form':form,'aid':aid})

    def post(self,request,aid):
        user_obj = UserProfile.objects.filter(id=aid).first()
        form = UserForm(request.POST,instance=user_obj)
        if form.is_valid():
            group_select = request.POST.getlist('group_sel')
            group_delete = request.POST.getlist('group_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            form.save()
            #修改用户的组,用户的权限
            user_obj.groups.add(*group_select)
            user_obj.groups.remove(*group_delete)
            user_obj.user_permissions.add(*perm_select)
            user_obj.user_permissions.remove(*perm_delete)
        return HttpResponseRedirect("")


class UserDel(View):
    def get(self,request):
        ret ={'status':True}
        try:
            nid = request.POST.getlist('nid[]')
            obj = UserProfile.objects(id__in=nid).delete()

        except Exception as e:
            ret['status'] =False

        return HttpResponse(json.dumps(ret))


class UserGroupList(LoginRequiredMixin,View):
    def get(self,request):
        groups = UserGroup.objects.all()
        return render(request,'',{})


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code=404
    return response


# 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
