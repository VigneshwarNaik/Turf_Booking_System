"""owner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from  customer  import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url('^logcheck', views.logcheck, name='logcheck'),
    url('^ownerturfview', views.ownerturfview, name='ownerturfview'),

    url('^achangepassword', views.achangepassword, name='achangepassword'),
    url('^insertuser', views.insertuser, name='insertuser'),
    url('^insertturf', views.insertturf, name='insertturf'),
    url('^insertBooking(?P<tid>\d+)/$', views.insertBooking, name='insertBooking'),
    url('^insertPayment', views.insertPayment, name='insertPayment'),
    url('^insertReview', views.insertReview, name='insertReview'),

    url('^paymentview', views.paymentview, name='paymentview'),
    url('^bookingview', views.bookingview, name='bookingview'),
    url('^turfview', views.turfview, name='turfview'),
    url('^userview', views.userview, name='userview'),
    url('^reviewview', views.reviewview, name='reviewview'),
    url('^showqr', views.showqr, name='showqr'),
    url('forgotpassword', views.forgotpassword, name='forgotpassword'),
    url('^payconf(?P<pk>\d+)/$',views.payconf,name='payconf')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
