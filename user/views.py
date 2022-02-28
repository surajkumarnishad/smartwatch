from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection


# Create your views here.
def feedback(request):
    return render(request, 'user/feedback.html')


def brands(request):
    return render(request, 'user/brand.html')


def base(request):
    Ourprofile=profile.objects.filter(Email=userid)
    bdata = brand.objects.all()
    return render(request, 'user/base.html', {"data": bdata, "p":Ourprofile})


def home(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    bdata = brand.objects.all().order_by('-id')[0:6]
    pdata = product.objects.all().order_by('-id')[0:12]
    return render(request, 'user/index.html', {"data": bdata, 'product': pdata,"cartcount":addcount})


def about(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    bdata = brand.objects.all()
    return render(request, 'user/AboutUs.html', {'data': bdata,"cartcount":addcount})


def contactus(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    Ourprofile=profile.objects.filter(Email=userid)
    status = "Leave A Message"
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Message = request.POST.get("msg", "")
        contact(name=Name, mobile=Mobile, email=Email, message=Message).save()
        status = "Successfully Submitted "
    bdata = brand.objects.all()
    return render(request, 'user/ContactUs.html', {'s': status,"p":Ourprofile, 'data': bdata,"cartcount":addcount})

def myprofile(request):
    userid=request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    Ourprofile=profile.objects.filter(Email=userid)
    if userid:
        if request.method=='POST': 
            name = request.POST.get("name", "")
            dob = request.POST.get("dob", "")
            gender = request.POST.get("gender", "")
            mobile = request.POST.get("mobile", "")
            password = request.POST.get("passwd", "")
            address = request.POST.get("address", "")
            photo = request.FILES['fu']
            profile(Email=userid, Name=name, Dob=dob, Gender=gender, Mobile=mobile, Password=password, Address=address,
                    Photo=photo).save()
            return HttpResponse("<script>alert('Your profile Updated Successfully..');window.location.href='/user/myprofile/'</script>")

    return render(request,'user/My Profile.html',{"cartcount":addcount,"p":Ourprofile})


def myorder(request):
    userid=request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o, user_product p where o.pid=p.id and o.userid='"+str(userid)+"' ")
        orderdata=cursor.fetchall()
        if oid:
            result=order.objects.filter(id=oid, userid=userid)
            result.delete()
            return HttpResponse("<script> alert('Your order has been canceled');window.location.href='/user/myorder'</script>")
    return render(request, 'user/My Order.html',{"pendingorder":orderdata,"cartcount":addcount})


def prod(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    bdata = brand.objects.all()
    a = request.GET.get('more')
    if a is not None:
        pdata = product.objects.filter(brand=a)
    else:
        pdata = product.objects.all()
    return render(request, 'user/product.html', {'data': bdata, 'aldata': pdata,"cartcount":addcount})


def detail(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    a = request.GET.get('msg')
    data = product.objects.filter(id=a)
    bdata = brand.objects.all()
    return render(request, 'user/viewdetail.html', {'d': data, 'data': bdata,"cartcount":addcount})

def signup(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    bdata = brand.objects.all()
    if request.method == 'POST':
        name = request.POST.get("name", "")
        dob = request.POST.get("dob", "")
        gender = request.POST.get("gender", "")
        mobile = request.POST.get("mobile", "")
        email = request.POST.get("email", "")
        password = request.POST.get("passwd", "")
        address = request.POST.get("address", "")
        photo = request.FILES['fu']
        d = profile.objects.filter(Email=email)
        if d.count() > 0:
            return HttpResponse(
                "<script>alert('You are already registered..');window.location.href='/user/signup/'</script>")
        else:
            profile(Name=name, Dob=dob, Gender=gender, Mobile=mobile, Email=email, Password=password, Address=address,
                    Photo=photo).save()
            return HttpResponse("<script> alert('You are Registered Successfully');window.location.href='/user/signup/'</script>")
    return render(request, 'user/sign up.html', {'data': bdata,"cartcount":addcount})


def signin(request):
    if request.method == 'POST':
        uname = request.POST.get("email")
        passwd = request.POST.get("passwd")
        checkuser = profile.objects.filter(Email=uname, Password=passwd)
        checkuser1=profile.objects.filter(Email=uname)
        if (checkuser):
            request.session['userid'] = uname
            return HttpResponse("<script>alert('Logged In Successfully');window.location.href='/user/myprofile/';</script>")
        elif checkuser1.count()==0:
            return HttpResponse("<script>alert('This UserID Not Registered');window.location.href='/user/signup';</script>")
        else:
            return HttpResponse("<script>alert('You Entered Incorrect Password');window.location.href='/user/signin/';</script>")
    return render(request,'user/login.html')

def proccess(request):
    userid=request.session.get('userid')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    if userid is not None:
        if btn=='cart':
            checkcartitem=addtocart.objects.filter(pid=pid, userid=userid)
            if checkcartitem.count()==0:
                addtocart(pid=pid, userid=userid, status=True, cdate=datetime.datetime.now()).save()
                return HttpResponse("<script>alert('Add in cart');window.location.href='/user'</script>")
            else:
                return HttpResponse("<script>alert('this product already added in cart');window.location.href='/user'</script>")
        elif btn=='order':
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('you order have confirmed...');window.location.href='/user'</script>")
        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid, userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Order Confirmed & Removed from Cart');window.location.href='/user/cart'</script>")
    else:
        return HttpResponse("<script>window.location.href='/user/signin'</script>")
    return render(request, 'user/proccess.html',{"alreadylogin": True})


def cart(request):
    userid = request.session.get('userid')
    addcount = addtocart.objects.filter(userid=userid).count()
    cartdata=""
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_product p where p.id=c.pid and c.userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()
        pid=request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(id=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('Your product has been removed successfully');window.location.href='/user/cart/'</script>")
    return render(request,'user/cart.html',{"cart":cartdata,"cartcount":addcount})


def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home'</script>")

