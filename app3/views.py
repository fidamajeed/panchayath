from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import JsonResponse
from .models import *
from datetime import date
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User,auth
from datetime import datetime
from django.utils import timezone




# Create your views here.

def base(r):
    c=complaint.objects.all()
    u=usersignup.objects.all()
    cl=0
    ur=0
    um=0
    for i in c:
        cl=cl+1
    for j in u:
        if j.status=="resident":
            ur=ur+1
        else:
            um=um+1
    return render(r,"adminn/index.html",{'cl':cl,'ur':ur,'um':um})


def signup(r):
    l=["Puthenvelikkara",'Chengamanadu','Nedumbassery','Parakkadavu','Kunnukara']
    if r.method == 'POST':
        pnc = r.POST.get('panchayat')
        w = r.POST.get('ward')
        n = r.POST.get('name')
        e = r.POST.get('email')
        ph = r.POST.get('phone')
        ad=r.POST.get('address')
        u = r.POST.get('username')
        p = r.POST.get('password')
        p2 = r.POST.get('repassword')
        if p == p2:
            if usersignup.objects.filter(username=u).exists():
                messages.info(r,"Username already exists",extra_tags="signup")
                return redirect(signup) 
            elif usersignup.objects.filter(email=e).exists():
                messages.info(r,"Email already exists",extra_tags="signup")
                return redirect(signup)
            elif pnc=='None' or w =='None':
                messages.info(r,"Select panchayat and ward",extra_tags="signup")
                return redirect(signup)  
            else:
                val=usersignup.objects.create(panchayat=pnc,ward=w,name=n,email=e,phone=ph,address=ad,username=u,password=p,status='resident')
                val.save()  
                return render(r,'sub.html',{"e":e}) 
                 
        else:
            messages.info(r,"Password doesn't match",extra_tags="signup")
            return redirect(signup) 

    return render(r,'my_template.html',{'l':l})
def sub(r,val):
    if r.method=='POST':
        
        usrd = usersignup.objects.get(email=val)
        mem=usersignup.objects.filter(ward=usrd.ward,status='member')
        if len(mem)==0:
            usrd.status = r.POST.get('option')
        else:
             messages.info(r,'one member has already registered in this ward..please contact admin..')
        
        usrd.image = r.FILES.get('image')
        usrd.proof = r.FILES.get('proof')
        usrd.save()
        return redirect(login)
    return render(r,'sub.html')


def login(r):
    if r.method=='POST':
        u = r.POST.get('username')
        p =  r.POST.get('password')
        if u=='admin'and p=='123':
            r.session['id'] = [1]
            return redirect(base)

        elif usersignup.objects.filter(username=u).exists():
            usr = usersignup.objects.filter(username=u).first()
            if usr.approval=='Approved':
                if usr.password == p:
                    if usr.status=='resident':
                        r.session['id'] = [usr.id]
                        return redirect(aftrlog)
                    else:
                        r.session['id'] = [usr.id]
                        return redirect(mmember)
                else:
                    messages.info(r,'Incorrect Password',extra_tags="login")
                    return redirect(login)
            else:
                url='login'
                msg='''<script> alert('Hi %s Admin has to verify your account details to login ..')
                window.location='%s'</script>'''%(usr.username,url)
                return HttpResponse(msg)
        else:
            messages.info(r,'Username not found',extra_tags="login")
            return redirect(login)       
    return render(r,'login.html')

def logout(r):
    if 'id' in r.session:
        r.session.flush()
        return redirect(rbase)
    return redirect(login)
def pro(r,val):
    usr=usersignup.objects.filter(id=val).first()
    return render(r,'adminn/profile.html',{'usr':usr})


#####################__________ ADMIN____________######################

def residents(r):
    w="REGISTERED RESIDENTS"
    u=usersignup.objects.all()
    l=[]
    for i in u:
        if i.approval=="Approved":
            if i.status=="resident":
                l.append(i)
    d1=len(l)
    return render(r,"adminn/userss.html",{"l":l,"w":w,"d1":d1})

def members(r):
    w="REGISTERED MEMBERS"
    u=usersignup.objects.all()
    l=[]
    for i in u:
        if i.approval=="Approved":
            if i.status=="member":
                l.append(i)
    d1=len(l)
    return render(r,"adminn/userss.html",{"l":l,"w":w,"d1":d1})

def userapproval(r):
    u=usersignup.objects.all()
    l=[]
    for i in u:
        if i.approval=="Pending":
            l.append(i)
    d1=len(l)
    return render(r,"adminn/userapproval.html",{"l":l,"d1":d1})

def approve(r,val):
    u=usersignup.objects.get(id=val)
    u.approval="Approved"
    u.save()
    return redirect(userapproval)

def allcomplaints(r):
    w="COMPLAINTS"
    c = complaint.objects.all()
    d={}
    for i in c:
        if d:
            temp=d.copy()
            for j,k in temp.items():
                if i.usr.panchayat==j:
                    for m,n in k.items():
                        if i.usr.ward==m:
                            k[i.usr.ward]=n+1
                        else:
                            d[i.usr.ward]=1
                    d.update(temp)
                else:
                    d[i.usr.panchayat]={i.usr.ward:1}
        else:
            d[i.usr.panchayat]={i.usr.ward:1}
    d1=len(d)
    return render(r,'adminn/complaints.html',{"d":d,"w":w,"d1":d1})

def complaintlist(r,val):
    c = complaint.objects.all()
    w=val
    n=[]
    for i in c:
        if i.usr.ward==val:
            n.append(i)
    b=blockk.objects.filter(wards=val).first()
    w=b.panchayatname+" "+"-"+" "+val+" "+"Ward"
    return render(r,"adminn/complaintlist.html",{"n":n,'w':w})

def complaintdetails(r,val):
    n = complaint.objects.filter(id=val).first()
    m = complaintimages.objects.filter(cmp=n)
    return render(r,"adminn/complaintdetails.html",{"n":n,"m":m})

def status(r,wa,s):
    c = complaint.objects.all()
    w=wa
    n=[]
    for i in c:
        if i.usr.ward==wa and i.complaintstatus==s:
            n.append(i)
    b=blockk.objects.filter(wards=wa).first()
    w=b.panchayatname+" "+"-"+" "+wa+" "+"Ward"
    return render(r,"adminn/complaintlist.html",{"n":n,'w':w})


def pending(r):
    w="Pending"
    c = complaint.objects.all()
    d={}
    for i in c:
        if i.complaintstatus=="Pending":
            if d:
                temp=d.copy()
                for j,k in temp.items():
                    if i.usr.panchayat==j:
                        for m,n in k.items():
                            if i.usr.ward==m:
                                k[i.usr.ward]=n+1
                            else:
                                d[i.usr.ward]=1
                        d.update(temp)
                    else:
                        d[i.usr.panchayat]={i.usr.ward:1}
            else:
                d[i.usr.panchayat]={i.usr.ward:1}
    d1=len(d)
    return render(r,'adminn/status.html',{"d":d,"w":w,"d1":d1})

def actiontaken(r):
    w="Action Taken"
    c = complaint.objects.all()
    d={}
    for i in c:
        if i.complaintstatus=="Action Taken":
            if d:
                temp=d.copy()
                for j,k in temp.items():
                    if i.usr.panchayat==j:
                        for m,n in k.items():
                            if i.usr.ward==m:
                                k[i.usr.ward]=n+1
                            else:
                                d[i.usr.ward]=1
                        d.update(temp)
                    else:
                        d[i.usr.panchayat]={i.usr.ward:1}
            else:
                d[i.usr.panchayat]={i.usr.ward:1}
    d1=len(d)
    return render(r,'adminn/status.html',{"d":d,"w":w,"d1":d1})

def solved(r):
    w="Solved"
    c = complaint.objects.all()
    d={}
    for i in c:
        if i.complaintstatus=="Solved":
            if d:
                temp=d.copy()
                for j,k in temp.items():
                    if i.usr.panchayat==j:
                        for m,n in k.items():
                            if i.usr.ward==m:
                                k[i.usr.ward]=n+1
                            else:
                                d[i.usr.ward]=1
                        d.update(temp)
                    else:
                        d[i.usr.panchayat]={i.usr.ward:1}
            else:
                d[i.usr.panchayat]={i.usr.ward:1}
    d1=len(d)
    return render(r,'adminn/status.html',{"d":d,"w":w,"d1":d1})

def my_view(request):
    l=["Puthenvelikkara",'Chengamanadu','Nedumbassery','Parakkadavu','Kunnukara']
    return render(request, 'my_template.html', {'l': l})

def fetch_wards(request):
    pname = request.GET.get('selected_panchayat')
    data = {}
    if pname:
        wards = blockk.objects.filter(panchayatname=pname).values_list('wards', flat=True)
        data['wards'] = list(wards)
    return JsonResponse(data)

def searchfn(r):
    if r.method == 'POST':
        sr = r.POST.get('sr')
        n = complaint.objects.filter(subject__icontains = sr) 
        d1=len(n)
        return render(r,'adminn/show.html',{'n':n,'d1':d1})
    

################# _____________RESIDENT___________ ################
    
def rbase(r):
    return render(r,'resident/index.html')
def aftrlog(r):
    rid=r.session['id'][0]
    
    usr=usersignup.objects.get(id=rid)
    mem=usersignup.objects.get(ward=usr.ward,status='member')
    comp=complaint.objects.filter(usr_id=rid)
    pen=complaint.objects.filter(usr_id=rid,complaintstatus='Pending')
    sol=complaint.objects.filter(usr_id=rid,complaintstatus='Solved')
    act=complaint.objects.filter(usr_id=rid,complaintstatus='Action Taken')
    tc=len(comp)
    pe=len(pen)
    so=len(sol)
    ac=len(act)

    print(comp)
    print(mem)
    return render(r,'resident/aftrlog.html',{'usr':usr,'mem':mem,'tc':tc,'pe':pe,'so':so,'ac':ac})
def rresident(r):
    return render(r,'resident/r1.html')
def rviewcomplaints(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        u=usersignup.objects.filter(id=val).first()
        date2=u.updated_at
        c=complaint.objects.filter(usr=u).all()
        d1=len(c)
        l={}
        w="Pending Complaints"
        for i in c:
            date1=i.created_at
            if ((i.complaintstatus=="Pending") or (i.complaintstatus=="Action Taken")):
                date1=i.created_at
                print("DATE",date1)

            if date2 > date1:   

                d= (date2-date1).days
                l[i.id]={i:d}

            else:

                d= (date1-date2).days
                l[i.id]={i:d}
        return render(r,'resident/viewcomplaints.html',{'c':c,'d1':d1,'w':w,'l':l})
    else:
        return redirect(login)

def rregcomplaints(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        if r.method=='POST':
            sub = r.POST.get('sub')
            det =  r.POST.get('det')
            img = r.FILES.getlist('image')
            if img:
                vall=complaint.objects.create(usr=usr,subject=sub,details=det)
                vall.save()
                for i in img:
                    valll=complaintimages.objects.create(cmp=vall,complaintimages=i)
                    valll.save()
                
                return redirect(aftrlog)

            else:
                vall=complaint.objects.create(usr=usr,subject=sub,details=det)
                vall.save()
                return redirect(aftrlog)
    return render(r,'resident/r1.html')

def rprofile(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        usr=usersignup.objects.filter(id=val).first()
        return render(r,'resident/profile.html',{'usr':usr})
def reditprofile(r):
    se=r.session.get('id')
    val=se[0]
    b=usersignup.objects.get(id=val)
    if r.method=='POST':
        b.name=r.POST.get('name')
        b.email=r.POST.get('email')
        b.phone=r.POST.get('phone')
        b.username=r.POST.get('username')
        b.save()
        pic=r.FILES.get('image')
        pic2=r.FILES.get('proof')
        print(pic2,pic)
        if pic:
            b.image=pic
            b.save()
        if pic2:
            b.proof=pic2
            b.save()
        
        return redirect(rprofile)
    return render(r,'resident/editprofile.html',{'b':b})
def rchangepassword(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        if r.method == 'POST':
            o = r.POST.get('opass')
            n = r.POST.get('npass')
            rp = r.POST.get('rpass')
            if o == usr.password:
                if n==rp:
                    usr.password=n
                    usr.save()
                    return redirect(rprofile)
                else:
                    messages.info(r,"Password doesnt match")
                    return redirect(rchangepassword) 
            else:
                messages.info(r,"Incorrect old password")
                return redirect(rchangepassword) 

        return render(r,"resident/changepassword.html",{'usr':usr})

def rcd(r,val):
    n = complaint.objects.filter(id=val).first()
    print("CMP",n.updated_at)
    nd = timezone.now()
    if (n.complaintstatus=="Pending" and n.smailp==0)or (n.complaintstatus=="Action Taken" and n.smailact==0):
        dd=nd-n.updated_at
        fd = dd.days
        print(n.complaintstatus,"difference=",dd,"days=",fd)
    else:
        fd=0
    
    m = complaintimages.objects.filter(cmp=n).all()
    try:      
        
        cmp=complaintmessage.objects.get(cmp_id=n)
       
    except:
        cmp=None
        pass

    return render(r,'resident/cd.html',{"n":n,"m":m,'cmp':cmp,'fd':fd})

def rsendmail(r,val):
    n = complaint.objects.filter(id=val).first()
    s=n.subject
    d=n.details
    send_mail(f'Complaint -status {n.complaintstatus}', f'{s}\n{d}','settings.EMAIL_HOST_USER', ['fidashirin15@gmail.com'],fail_silently=False)
    if n.complaintstatus=="Pending":
        n.smailp=1
        n.save()
    if n.complaintstatus=="Action Taken":
        n.smailact=1
        n.save()
    return redirect(rcd,val)

def rsendmail2(r,val):
    se=r.session.get('id')
    val=se[0]
    u=usersignup.objects.filter(id=val).first()
    if r.method=='POST':
        s=r.POST.get('sub')
        d=r.POST.get('det')
        

        send_mail('Reply From Admin', f'{s},{d}','settings.EMAIL_HOST_USER', ['abacomplaint@gmail.com'],fail_silently=False)
        return redirect(rviewcomplaints)
    return redirect(rviewcomplaints)
def rpending(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        date2=usr.updated_at
        print("DATE-2",date2)
        u=complaint.objects.filter(usr=usr,complaintstatus="Pending")
        l={}
        w="Pending Complaints"
        for i in u:
            date1=i.created_at
            if ((i.complaintstatus=="Pending")):
                date1=i.created_at

            if date2 > date1:   

                d= (date2-date1).days
                l[i.id]={i:d}

            else:

                d= (date1-date2).days
                l[i.id]={i:d}
        return render(r,"resident/show.html",{'w':w,'l':l,'n':u})
def ractiontaken(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        date2=usr.updated_at
        print("DATE-2",date2)
        n=complaint.objects.filter(usr=usr,complaintstatus="Action Taken")
        return render(r,"resident/show.html",{"n":n})
def rsolved(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        date2=usr.updated_at
        print("DATE-2",date2)
        n=complaint.objects.filter(usr=usr,complaintstatus="Solved")
        print("N",n)
        w="Solved Complaints"
    #   n=[]
        # for i in u:
        #     if i.complaintstatus=="Solved":
        #         n.append(i)
        return render(r,"resident/show.html",{"n":n})

def rnumOfDays(date1, date2):

  #check which date is greater to avoid days output in -ve number

    if date2 > date1:   

        return (date2-date1).days

    else:

        return (date1-date2).days
 

############__________ MEMBER __________#################
    

def mmember(r):
    rid=r.session['id'][0]
    usr=usersignup.objects.get(id=rid)
    res=usersignup.objects.filter(ward=usr.ward)
    comp=complaint.objects.filter(usr__id__in=usersignup.objects.filter(ward=usr.ward))
    total_res=len(res)
    tot_comp=len(comp)
    print(total_res)
    print(tot_comp)
    pen= comp.filter(complaintstatus='Pending').count()
    act= comp.filter(complaintstatus='Action Taken').count()
    sol= comp.filter(complaintstatus='Solved').count()

    tc=[]
    for i in comp:
         tc.append(i.complaintstatus)

    print("COMPLAINTS")
    print(tc.count('Solved'),tc.count('Pending'),tc.count('Action Taken'))

    
     
     
    return render(r,'members/member.html',{'usr':usr,'tot':total_res,'comp':tot_comp,'pen':pen,'act':act,'sol':sol,'res':res})

def mredet(r):
    rid=r.session['id'][0]
    usr=usersignup.objects.get(id=rid)
    res=usersignup.objects.filter(ward=usr.ward)
    comp=complaint.objects.filter(usr__id__in=usersignup.objects.filter(ward=usr.ward))
    total_res=len(res)
    cmp=[]
    dic={}
    for i in comp:
        cmp.append(i.usr_id)


    for i in res:
        dic[i.id]=cmp.count(i.id)
    print(dic)



    
    tot_comp=len(comp)
    return render(r,'members/resdet.html',{'res':res,'usr':usr,'tot':total_res,'comp':tot_comp,'dic':dic})



def mcomplaints(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        usr=usersignup.objects.filter(id=val).first()
        obj=complaint.objects.all()
        n=[]
        for i in obj:
            print()
            if i.usr.ward==usr.ward and i.usr.panchayat==usr.panchayat:
                n.append(i)
        d1=len(n)
        print(n)
        return render(r,'members/complaint.html',{'n':n,"d1":d1})


def mcomplaintlist(r,val):
    n = complaint.objects.filter(id=val).first()
    m = complaintimages.objects.filter(cmp=n)
    


    # n=[]
    # for i in c:
    #     if i.usr.ward==val:
    #         n.append(i)
    return render(r,"members/viewcomplaint.html",{"n":n,"m":m})



def mprofile(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        user=usersignup.objects.filter(id=val).first()
        return render(r,'members/profile.html',{'user':user})  
    return render(r,'members/profile.html') 

def muedit(r):
    se=r.session.get('id')
    val=se[0]
    user=usersignup.objects.filter(id=val).first()
    return render(r,'members/uedit.html',{'user':user})

def muedit1(r):
    se=r.session.get('id')
    val=se[0]
    user=usersignup.objects.get(id=val)
    if r.method=='POST':
        user.name=r.POST.get('name')
        user.email=r.POST.get('email')
        user.phone=r.POST.get('phone')
        user.image=r.FILES.get('image')
        user.proof=r.FILES.get('proof')
        user.save()
        return redirect(mprofile)
    return render(r,'members/uedit.html',{'user':user})


def mpending(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        u=complaint.objects.all()
        usr=usersignup.objects.filter(id=val).first()
        n=[]
        for i in u:
            if i.usr.ward==usr.ward:
                if i.complaintstatus=="Pending":
                    n.append(i)
        d1=len(n)
        return render(r,"members/pending.html",{"n":n,"d1":d1})
    

def mactiontaken(r):
   if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        u=complaint.objects.all()
        usr=usersignup.objects.filter(id=val).first()
        n=[]
        for i in u:
             if i.usr.ward==usr.ward:
                if i.complaintstatus=="Action Taken":
                    n.append(i)
        d1=len(n)
        return render(r,"members/actiontaken.html",{"n":n,"d1":d1})


def msolved(r):
     if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        u=complaint.objects.all()
        usr=usersignup.objects.filter(id=val).first()
        n=[]
        for i in u:
            if i.usr.ward==usr.ward:
                if i.complaintstatus=="Solved":
                    n.append(i)
        d1=len(n)
        return render(r,"members/solved.html",{"n":n,"d1":d1})
      
    
def mstatus(r,val):
    if r.method=='POST':
        print('hi')
        s=r.POST.get('status')
        print("status",s)
        c=complaint.objects.get(id=val)
        c.complaintstatus=s
        c.save()
        if s=='Action Taken':
            cmp=complaintmessage.objects.create(cmp=c,message=r.POST.get('message'))
            cmp.save()
        return redirect(mcomplaints)
    


def mmy_view(request):
    l=["Puthenvelikkara",'Chengamanadu','Nedumbassery','Parakkadavu','Kunnukara']
    return render(request, 'signup.html', {'l': l})

def mfetch_wards(request):
    pname = request.GET.get('selected_panchayat')
    data = {}
    if pname:
        wards = blockk.objects.filter(panchayatname=pname).values_list('wards', flat=True)
        data['wards'] = list(wards)
    return JsonResponse(data)


def mchangepassword(r):
    se=r.session.get('id')
    val=se[0]
    user=usersignup.objects.filter(id=val).first()
    return render(r,'members/changepassword.html',{'user':user})


def mchangepassword1(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        if r.method == 'POST':
            o = r.POST.get('opass')
            n = r.POST.get('npass')
            rp = r.POST.get('rpass')
            if o == usr.password:
                if n==rp:
                    usr.password=n
                    usr.save()
                    return redirect(mprofile)
                else:
                    messages.info(r,"Password doesnt match")
                    return redirect(mchangepassword1) 
            else:
                messages.info(r,"Incorrect old password")
                return redirect(mchangepassword1) 

        return render(r,"members/changepassword.html",{'usr':usr})
   

def msearch(r):
    if 'id' in r.session:
        se=r.session.get('id')
        val=se[0]
        usr=usersignup.objects.filter(id=val).first()
        if r.method=='POST':
            search_term=r.POST.get('search')
            print(search_term)
            s=complaint.objects.filter(subject__icontains=search_term)
            n=[]
            for i in s:
                if i.usr.panchayat==usr.panchayat and i.usr.ward==usr.ward:
                    n.append(i)
            d1=len(n)
            return render(r,'members/search.html',{'n':n,'d1':d1})
        return redirect(mmember)

    
# Create your views here.
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = usersignup.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, "resident/forget.html")
def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.set_password(new_password)
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'resident/reset.html',{'token':token})
def user_message(req):
    if req.method=='POST':
        nm=req.POST['name']
        email=req.POST['email']
        sub=req.POST['subject']
        msg=req.POST['message']
        send_mail(f'{sub} from user {req.user.email}', f'{msg}','settings.EMAIL_HOST_USER', [email], fail_silently=False)

    return render(req,'user_message.html')
