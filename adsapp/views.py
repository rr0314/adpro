from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse ,HttpResponseRedirect
from .models import loginform,signform, adminreg, product_tab, cart, contform
import os
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def index(request):
    mydata=product_tab.objects.all()
    return render(request,'index.html',{"data1":mydata})


#log
def login(request):
    if request.method=='POST':
        Email=request.POST['Email']
        password=request.POST['password']
        check=signform.objects.filter(Email=Email,password=password)
        if check:
            for i in check:
                request.session['id']=i.id
                request.session['Name']=i.Name
                log=loginform(Email=Email,password=password)
                log.save()
                return render(request,'index.html',{"error":"logged in"})
        else:
            return render (request,'login.html',{"error":"not registered"})
    else:
        return render(request,'login.html')
    

def logout(request):
    if request.session.has_key('id'):
        del request.session["id"]
        del request.session["Name"]
        return HttpResponseRedirect("/")


#reg / sign
# def reg(request):
#     return render(request,'register.html')

def signupform(request):
    dict11={}
    if request.method=="POST":
        Name=request.POST['Name']
        Email=request.POST['Email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        Address=request.POST['Address']
        country=request.POST['country']
        City=request.POST['City']
        code=request.POST['code']
        number=request.POST['number']
        if password==cpassword:
            add=signform(Name=Name,Email=Email,password=password,cpassword=cpassword,Address=Address,country=country,City=City,code=code,number=number)
            add.save()
            dict11['msg11']="Successfully signed in"
            return render(request,"login.html",dict11)
    else:
        # print(e)
        # dict11['msg11']="Something wrong!!!"
        return render(request,"register.html",dict11)

def shop(request):

    return render(request,'shop.html')

def single(request):
    if request.method == "GET":
        id=request.GET['id']
        mydata=product_tab.objects.filter(id=id)
        return render(request,'single.html',{"data1":mydata})



#admin
def adminlog(request):
    if request.method=="POST":        
        aemail=request.POST['aemail']
        apassword=request.POST['apassword']        
        check=adminreg.objects.filter(aemail=aemail,apassword=apassword)
        if check:
            for x in check:
                request.session["aid"]=x.id
                request.session["aname"]=x.aname
            return render(request,"admin/dashboard.html")
        else:            
            return render(request,"admin/adminreg.html",{"err":"Unregistered"})
    else:
        return render(request,'admin/adminlog.html')
    

def dash(request):
    if request.session.has_key('aid'):
        return render(request,"admin/dashboard.html")
    else:
        return HttpResponseRedirect("/adminlog/")

def adsign(request):
    if request.method=="POST":
        aname=request.POST['aname']
        aemail=request.POST['aemail']
        apassword=request.POST['apassword']
        capassword=request.POST['capassword']
        check=adminreg.objects.filter(aemail=aemail)
        if check:
                return render(request,"admin/adminreg.html",{"error":"email already registered"})
        else:
            addd=adminreg(aname=aname,aemail=aemail,apassword=apassword,capassword=capassword)
            addd.save()
            return render(request,"admin/adminlog.html")
    else:
        return render(request,'admin/adminreg.html')
    
def adlogout(request):
     if request.session.has_key('aid'):
        del request.session["aid"]
        del request.session["aname"]
        return HttpResponseRedirect("/adminlog/")
     

def addproduct(request):
    if request.session.has_key('aid'):
        if request.method == "POST":

            productname=request.POST["pname"]
            oldprice=request.POST['oldprice']
            newprice=request.POST['newprice']
            pdescription=request.POST['pdescription']
            image=request.FILES['image']
            select=request.POST["s1"]
            add=product_tab(productname=productname,oldprice=oldprice,newprice=newprice,
                pdescription=pdescription,image=image,catagory=select)
            add.save()
            print()
            return HttpResponseRedirect("/dash/")
       
        else:
            return render(request,'admin/addprod.html')
    return HttpResponseRedirect("/adminlog/")

def upprod(request):
    if request.method == "POST":
        productname=request.POST["pname"]
        oldprice=request.POST["oldprice"]
        newprice=request.POST["newprice"]
        pdescription=request.POST["pdesciption"]
        select=request.POST["s1"]
        uid=request.GET['uuid']
        checkbox=request.POST["imgup"]
        if checkbox == "yes":
            image=request.FILES["image"]
            oldrec=product_tab.objects.filter(id=uid)
            updrec=product_tab.objects.get(id=uid)
            for x in oldrec:
                imageurl=x.image.url
                pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imageurl
                if os.path.exists(pathtoimage):
                    os.remove(pathtoimage)
                    print('Successfully deleted')
            updrec.image=image
            updrec.save()
        add=product_tab.objects.filter(id=uid).update(productname=productname,oldprice=oldprice,newprice=newprice,pdescription=pdescription,catagory=select)
        return HttpResponseRedirect("/prodtab/")
    else:
        uid=request.GET['uuid']
        mydata=product_tab.objects.filter(id=uid)
        return render(request,"admin/upprod.html",{"data2":mydata})

def prodel(request):
    if request.session.has_key('aid'):
        uid=request.GET['uuid']
        oldrec=product_tab.objects.filter(id=uid)
        for x in oldrec:
            imageurl=x.image.url
            pathoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+imageurl
            if os.path.exists(pathoimage):
                os.remove(pathoimage)
                # prfloat('Successfully deleted')
        mydata=product_tab.objects.filter(id=uid).delete()
        return HttpResponseRedirect("/prodtab/")
    else: 
        return HttpResponseRedirect('/adminlog/')
    
def prodtab(request):
    if request.session.has_key('aid'):
        mydata=product_tab.objects.all()
        return render(request,"admin/tables.html",{"data1":mydata})
    else:
        return HttpResponseRedirect('/adminlog/')

def checkout(request):
    uid=request.session['id']
    usr=signform.objects.get(id=uid)
    datas=cart.objects.filter(uid=usr,status="pending")
    total=0
    for x in datas:
        price=x.total
        total=total+float(price)
    return render(request,"checkout.html",{"data2":datas,"total":total})


def addcart(request):
    if request.session.has_key('id'):
        if request.method == "POST":
            pid=request.GET['pid']
            prd=product_tab.objects.get(id=pid)
            uid=request.session['id']
            usr=signform.objects.get(id=uid)
            product=product_tab.objects.filter(id=pid)
            for x in product:
                price=x.newprice
            deliv=(int(price)*10)/100
            total=0
            total=int(deliv)+int(price)

            data1=cart.objects.filter(uid=usr,pid=prd,status="pending")
            if data1:
                total1=0
                for x in data1:
                    qty=int(x.quantity)
                    qty+=1
                    price=x.pid.newprice
                    price1=x.total
                    total1=total1+float(price1)
                total=0
                deliv=(float(price)*10)/100
                total=(float(deliv))+(float(price)*int(qty))
                add=cart.objects.filter(uid=usr,pid=prd,status="pending"). update(total=total,quantity=qty)
                datas=cart.objects.filter(uid=usr,status="pending")

                return render(request,"checkout.html",{"data2":datas,"total":total1})
            else:
                add=cart(pid=prd,uid=usr,quantity=1,total=total)
                add.save()
            datas=cart.objects.filter(uid=usr,status="pending")
            total=0
            for x in datas:
                price=x.total
                total=total+float(price)
            return render(request,"checkout.html",{"data2":datas,"total":total})
        else:
            pid=request.GET['pid']
            datas=product_tab.objects.filter(id=pid)
            return render(request,"single.html",{"data2":datas})
    else:
        return HttpResponseRedirect("/login/")


def cart_update(request):
    cid=request.GET['cid']
    quantity=request.POST['qty']
    carrt=cart.objects.filter(id=cid)
    for x in carrt:
        price=x.pid.newprice
    newprice=(float(price)*int(quantity))+((float(price)*10)/100)
    cart.objects.filter(id=cid).update(quantity=quantity,total=newprice)
    return HttpResponseRedirect("/check/")


def cart_del(request):
    cid=request.GET['cid']
    cart.objects.filter(id=cid).delete()
    return HttpResponseRedirect("/check/")




#p
def men(request):
    mydata=product_tab.objects.filter(catagory="Men")
    return render(request,'men.html',{"data1":mydata})


def women(request):
    mydata=product_tab.objects.filter(catagory="Women")
    return render(request,"women.html",{"data1":mydata})

def foot(request):
    mydata=product_tab.objects.filter(catagory="Football")
    return render(request,"football.html",{"data1":mydata})

def run(request):
    mydata=product_tab.objects.filter(catagory="Run")
    return render(request,"run.html",{"data1":mydata})


def cont(request):
    if request.method=='POST':
        name=request.POST["name"]
        email=request.POST["email"]
        message=request.POST['message']
        subject='Contact form'
        message=f'Theres a message from {name}, email {email}.The message is {message}.Thank you.'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[settings.EMAIL_HOST_USER,]
        send_mail(subject,message,email_from,recipient_list)
        subject='thanks for submitting contact form'
        message=f'Hi {name}, thank you for submitting contact form'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email, ]
        send_mail(subject,message,email_from,recipient_list)

        return render(request,'index.html')
    else:
        return render(request,'contact.html')

def msgs(request):

    if request.session.has_key('aid'):
       
        msgs=contform.objects.all()
        return render(request,'admin/message.html',{'mof':msgs})
    else:
        return HttpResponseRedirect('/adminlog/')
    
def msgdel(request):
    regid=request.GET['regid']
    contdata=contform.objects.filter(id=regid).delete()
    return redirect('/admin/message.html/')
