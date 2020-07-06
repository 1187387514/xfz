from django.shortcuts import render,reverse
from .models import PayInfo,PayInfoOrder
from apps.xfzauth.decorators import xfz_login_required
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from django.conf import settings
import os
from django.http import FileResponse
from django.http import Http404

def index(request):
    context = {
        "payinfos":  PayInfo.objects.all()
    }
    return render(request,'payinfo/payinfo.html',context=context)

@xfz_login_required
def payinfo_order(request,payinfo_id):
    payinfo = PayInfo.objects.get(pk=payinfo_id)
    order = PayInfoOrder.objects.create(payinfo=payinfo, buyer=request.user, status=1, amount=payinfo.price)

    context = {
        'goods': payinfo,
        'order': order,
        'notify_url': request.build_absolute_uri(reverse('payinfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payinfo:index'))
    }
    return render(request, 'course/course_order.html', context=context)

@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    PayInfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()

def download(request):
    payinfoid = request.GET.get('payinfo_id')
    order = PayInfo.objects.filter(pk=payinfoid).first()
    if order:
        # payinfo = order.payinfo
        # path = payinfo.path
        path = order.path
        fd = open(os.path.join(settings.MEDIA_ROOT,path),'rb')
        response = FileResponse(fd)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = f'attachment;filename = {path.split("/")[-1]}'
        return response
    else:
        return Http404


