from django.http import JsonResponse,request,HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()
@require_POST
def login_view(request):
    forms = LoginForm(request.POST)
    if forms.is_valid():
        telephone = forms.cleaned_data.get('telephone')
        password = forms.cleaned_data.get('password')
        remember = forms.cleaned_data.get(('remember'))
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                print(JsonResponse({'code':200,'message':'','data':{}}))
                print(remember)
                return restful.ok()
            else:
                return restful.unauth_error(message='您的账号已被冻结')
        else:
            return restful.params_error(message='手机号码或者密码错误')
    else:
        errors = forms.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print('fail')
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text,image = Captcha.gene_code()

    out = BytesIO()
    image.save(out,'png')
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)
    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    # 暂时先不直接发短信验证码，省钱，实际用的时候再解除注释
    # result = aliyunsms.send_sms(telephone,code)
    cache.set(telephone,code,5*60)
    # print(result)
    print(code)
    return restful.ok()

def cache_test(request):
    cache.set('zhihao','123456',5*60)
    result = cache.get('zhihao')
    print(result)
    return HttpResponse('success')
