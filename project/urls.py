"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app3 import views       

urlpatterns = [
    path('admin/', admin.site.urls),

    ###############_____________RESIDENT___________##############

    path('',views.rbase,name='index'),
    path('aftrlog',views.aftrlog,name='aftrlog'),
    path('r',views.rresident,name='resident'),
    path('vc',views.rviewcomplaints,name='viewcomplaints'),
    path('cd/<val>',views.rcd,name='cd'),
    path('profile',views.rprofile,name='profile'),
    path('eprofile',views.reditprofile,name='editprofile'),
    path('regcomplaints',views.rregcomplaints,name='regcomplaints'),
    path('changepassword',views.rchangepassword,name='changepassword'),
    path('rpending',views.rpending,name='rpending'),
    path('ractiontaken',views.ractiontaken,name='ractiontaken'),
    path('rsolved',views.rsolved,name='rsolved'),
    path('sendmail/<val>',views.rsendmail,name='sendmail'),
    path('sendmail/rsendmail/<val>',views.rsendmail2,name='rsendmail2'),
    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),



    #################__________MEMBER_________#################


    path('mmember',views.mmember,name='mmember'),
    path('mprofile',views.mprofile,name='mprofile'),
    path('muedit',views.muedit,name='muedit'),
    path('muedit1',views.muedit1,name='muedit1'),
    
    path('mcomplaint',views.mcomplaints,name='mcomplaint'),
    path('mview/<val>',views.mcomplaintlist,name='mview'),
    path('mpending',views.mpending,name='mpending'),
    path('mactiontaken',views.mactiontaken,name='mactiontaken'),
    path('msolved',views.msolved,name='msolved'),
    path('mview/mstatus/<val>',views.mstatus,name='mstatus'),
    path('mredet',views.mredet,name='mredet'),
    
    path('mchangepassword',views.mchangepassword,name='mchangepassword'),
    path('mchangepassword1',views.mchangepassword1,name='mchangepassword1'),
    
    path('msearch',views.msearch,name='msearch'),



    ################# ________ADMIN_________ ###############

    path('b',views.base,name="base"),

    path('signup',views.signup,name="signup"),
    path('sub/<val>',views.sub,name="sub"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),

    path('residents',views.residents,name="residents"),
    path('members',views.members,name="members"),

    path('comp',views.allcomplaints,name="comp"),
    path('complist/<val>',views.complaintlist,name="complist"),
    path('compdet/<val>',views.complaintdetails,name="compdet"),
    path('complist/compdet/<val>',views.complaintdetails,name="compdet2"),
    path('status/<wa>/<s>',views.status,name="status"),

    path('pending',views.pending,name="pending"),
    path('taken',views.actiontaken,name="taken"),
    path('solved',views.solved,name="solved"),

    path('search',views.searchfn,name="search"),


    path('apr',views.userapproval,name="apr"),
    path('pro/<val>',views.pro,name="pro"),

    path('pro/yess/<val>',views.approve,name="yess"),
    
    path('my-view/', views.my_view, name='my_view'),
    path('fetch-wards/', views.fetch_wards, name='fetch_wards'),
    # Add other URLs as needed

   



]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

