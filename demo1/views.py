import datetime
import hashlib

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from user_app import models


def arrive_index(request):
    print(make_password(123456, None, 'pbkdf2_sha256'))
    text = 'pbkdf2_sha256$100000$hWyGKrPoi7x4$cNz2Buc+xgmFFkqoY9XjUjVnh3jnYvTUjkbpb2p86Xg='
    check_password(123456, text)
    return render(request, 'hello.html')


def register_form(request):

    return render(request, 'register.html')


def hash_code(name, now='yan'):
    h = hashlib.sha256()
    name +=  now
    h.update(name.encode())
    return h.hexdigest()

def make_string(user):
    """
    为用户生成一个唯一的注册的标识
    :param user:
    :return:
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)

    return code


def send_email(email, code):
    """
    向用户的邮箱发送验证邮件
    :param email:用户邮箱，
    :param code:生成的唯一的验证标识
    :return:
    """
    subject, from_email, to = '来自149的测试邮件', '18500230996@sina.cn', 'maoxinyu925@163.com'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/user_confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000', code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_register(request):
    """
    处理用户注册视图
    :param request:用户注册信息
    :return:处理完成用户的信息，返回到用户登录的
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    new_user = models.User.objects.create(name=username, password=password, email=email)
    code = make_string(new_user)
    send_email(email, code)

    message = '请前往邮箱进行验证'

    return render(request, 'login.html', locals())


def email_confirm(request):
    """
    由用户的邮箱发起的验证邮箱是否可用的请求
    :param request: 唯一的验证标识
    :return:
    """
    code = request.GET.get('code')
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的请求"
        return render(request, 'register.html')

    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = "感谢确认，请登录"

    return render(request, 'login.html', locals())


def demo1(request):
    print(1111)
    print(1111)


    return HttpResponse()

