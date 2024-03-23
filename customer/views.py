from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.urls import reverse
import smtplib
# Create your views here.
import datetime
import os

from customer.models import UserLogin,booking,user,turf,booking,payment,Review
from owner.settings import BASE_DIR


def index(request):
    return render(request,'index.html')

def showqr(request):
    return render(request,'qrcode.html')


def logcheck(request):
    if request.method == "POST":
        username = request.POST.get('t1', '')
        password = request.POST.get('t2', '')
        request.session['username']=username
        #if username=="admin" and password=="admin":
        checklogin = UserLogin.objects.filter(username=username).values()
        for a in checklogin:
            utype = a['utype']
            upass= a['password']
            if(upass == password):
                if(utype == "user"):
                    return render(request,'user_home.html',context={'msg':'welcome to owner'})
            if (utype == "owner"):
                return render(request, 'owner_home.html', context={'msg': 'welcome to owner'})

            else:
                return render(request,'login.html',context={'msg':'fail'})

    return render(request,'login.html')

def achangepassword(request):
    uname=request.session['username']
    if request.method == 'POST':
        currentpass = request.POST.get('t1', '')
        newpass = request.POST.get('t2', '')
        confirmpass = request.POST.get('t3', '')

        ucheck = UserLogin.objects.filter(username=uname).values()
        for a in ucheck:
            u = a['username']
            p = a['password']
            if u == uname and currentpass == p:
                if newpass == confirmpass:
                    UserLogin.objects.filter(username=uname).update(password=newpass)
                    base_url=reverse('logcheck')
                    msg='password has been changed successfully'
                    return redirect(base_url,msg=msg)
                else:
                    return render(request, 'changepassword.html',{'msg': 'both the usename and password are incorrect'})
            else:
                return render(request, 'changepassword.html',{'msg': 'invalid username'})
    return render(request, 'changepassword.html')


def insertuser(request):
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        s5 = request.POST.get('t5', '')

        udata = user.objects.filter(email=s4).count()
        if udata >= 1:
            return render(request, 'user.html', {'msg': 'user is already exist'})
        else:
            user.objects.create(user_id=s1, name=s2, password=s3, email=s4, ph_no=s5)
            UserLogin.objects.create(username=s4, password=s5, utype='user')
            return render(request, 'user.html')
    return render(request,'user.html')


def insertturf(request):
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        s5 = request.POST.get('t5', '')
        turf.objects.create(truf_id=s1, name=s2, location=s3, type=s4, price=s5)
        return render(request, 'turf.html')

    eid = turf.objects.all().order_by('id').last()

    enum = int(eid.truf_id) + 1
    return render(request, "turf.html",{'enum':enum})


def insertBooking(request,tid):
    turfid = tid
    request.session['tfid']=turfid

    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        s5 = request.POST.get('t5', '')
        s6 = request.POST.get('t6', '')

        booking.objects.create(booking_id=s1, truf_id=s2, booking_date=s3, start_time=s4, end_time=s5, type=s6,)

        base_url = reverse('insertPayment')

        return redirect(base_url)


    return render(request, "booking.html",{'turfid':turfid})


def insertPayment(request):
    tid = request.session['tfid']
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')

        payment.objects.create(payment_id=s1, booking_id=s2, payment_date=s3, amount=s4,status='pending')

        return render(request, 'qrcode.html')

    pno = payment.objects.all().order_by('payment_id').last()
    num = int(pno.payment_id) + 1
    turfamt = turf.objects.filter(truf_id=tid).all()
    for u in turfamt:
        amt = u.price
    return render(request, "payment.html", {'num': num,'amt':amt})


def insertReview(request):
    uname = request.session['username']
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        s5 = request.POST.get('t5', '')
        s6 = request.POST.get('t6', '')

        Review.objects.create(id=s1, user_id=s2, turf_id=s3, rating=s4, comment=s5, review_date=s6)

        return render(request, 'review.html')
    return render(request, "review.html",{'uname':uname})


def paymentview(request):
    userdict=payment.objects.all()
    return render(request,'viewpayment.html',{'userdict' : userdict})

def bookingview(request):
    userdict=booking.objects.all()
    return render(request,'viewbooking.html',{'userdict' : userdict})

def turfview(request):
    userdict=turf.objects.all()
    return render(request,'viewturf.html',{'userdict' : userdict})

def ownerturfview(request):
    userdict=turf.objects.all()
    return render(request,'ownerviewturf.html',{'userdict' : userdict})

def userview(request):
    userdict=user.objects.all()
    return render(request,'viewuser.html',{'userdict' : userdict})

def reviewview(request):
    userdict=Review.objects.all()
    return render(request,'viewreview.html',{'userdict' : userdict})


def forgotpassword(request):
    if request.method=="POST":
        uname = request.POST.get('t1', '')
        user = UserLogin.objects.filter(username=uname).count()
        if user >= 1:
            userlog = UserLogin.objects.filter(username=uname).values()
            for u in userlog:
                upass= u['password']
                content = upass
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('turfbooking98@gmail.com', 'eburhopblranjprq')
                mail.sendmail('turfbooking98@gmail.com', uname , content)
                mail.close()
                return render(request,'login.html', {'msg': 'Your password has been sent to your E-mail'})
        else:
            return render(request,'forgotpassword.html', {'msg': 'Enter a valid username'})
    return render(request,'forgotpassword.html')

def payconf(request,pk):
    payment.objects.filter(id=pk).update(status='confirmed')
    base_url = reverse('paymentview')

    return redirect(base_url)

