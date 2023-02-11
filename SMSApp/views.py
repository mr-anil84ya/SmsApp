from builtins import filter
from fileinput import filename

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
import mysql.connector
from django.core.files.storage import FileSystemStorage
from  datetime import datetime
#
from django.views.decorators.csrf import csrf_exempt

mydb=mysql.connector.connect(host="localhost",user="root",password="",database="VT01DB")
cur = mydb.cursor();
def index(request):
    msg="";
    cur.execute("select * from tbl_notification");
    result = cur.fetchall();
    a = cur.rowcount;
    if (a > 0):
        for r in result:
            msg+="<span>"+r[2]+"</span></br>";
    else:
        msg = "No Notification Available";
    return render(request,'index.html',{"Msg":msg});
def registration(request):
    res="";result="";show="";
    if(request.method=="POST"):
        name=request.POST.get("txtname");
        fname=request.POST.get("txtfname");
        roll=request.POST.get("txtroll");
        email=request.POST.get("txtemail");
        passwd=request.POST.get("txtpass");
        cpasswd=request.POST.get("txtcpass");
        mobile=request.POST.get("txtmobile");
        year=request.POST.get("ddlyear");
        branch=request.POST.get("ddlbranch");
        stype=request.POST.get("ddlsporttype");
        adhar=request.POST.get("txtadhar");
        pic=request.FILES["fupic"];
        fs=FileSystemStorage(location='media/');
        filename=fs.save(pic.name,pic);
        fs_url=fs.url(filename);
        if(passwd==cpasswd):
            cur=mydb.cursor();
            query="insert into tbl_registration values('"+name+"','"+fname+"','"+email+"','"\
                  +roll+"','"+branch+"','"+year+"','"+mobile+"','"+filename+"','"+adhar+"','"+stype+"','15/07/2020')";
            query2="insert into tbl_login values('"+roll+"','"+passwd+"','user','1','15/07/2020')";
            cur.execute(query);
            cur.execute(query2);
            res="Student Registration Successfully..";
        else:
            res = "password and confirm password Not match";
    else:
        cur=mydb.cursor();
        cur.execute("select * from tbl_registration");
        result=cur.fetchall();
        a=cur.rowcount;
        if(a>0):
            for i in result:
                show=i[7];
    return render(request,'registration.html',{'Res':res,"Sh":show})
def contact(request):
    r1='';r2='';r3='';r4='';
    if(request.method=='POST'):
        name=request.POST.get('txtname');
        email=request.POST.get('txtemail');
        mobile=request.POST.get('txtmobile');
        msg=request.POST.get('txtmsg');
        r1=name;r3=mobile;
        r2=email;r4=msg;
        # result="My Name is:"+name+"Email is:"+email+"Mobile is:"+mobile+"message:"+msg;
       # print(name+email+mobile+msg);
    # return render(request,'contact.html',{'res':result});
    return render(request,'contact.html',{'res1':r1,'res2':r2,'res3':r3,'res4':r4});

def Login(request):
    type="";result="";check="";
    if(request.method=="POST"):
        user=request.POST.get("txtuserid");
        passwd=request.POST.get("txtpass");
        cur=mydb.cursor();
        cmd="select * from tbl_login where userid='"+user+"' and passwd='"+passwd+"' and status='1'";
        cur.execute(cmd);
        result=cur.fetchall();
        a=cur.rowcount;
        if(a>0):
            for i in result:
                type=i[2];
                if(type=="user"):
                    request.session["uid"] = user;
                    return redirect("../StudentZone/index");
                elif(type=="admin"):
                    request.session["aid"] = user;
                    return redirect("../AdminZone/ViewContact");
                else:
                   check="Invalid Type";
        else:
            check = "Invalid UserId and password";
    else:
        #return redirect("Login");
        pass;
    return render(request,'Login.html',{'Result':check});
#create connection

def demo(request):
    name='';email='';mobile='';pic='';res='';
    if(request.method=="POST"):
        name=request.POST.get("txtname");
        email=request.POST.get("txtemail");
        mobile=request.POST.get("txtmobile");
        pic=request.FILES["fupic"].name;
        cur=mydb.cursor();
        query="insert into tbl_demo values('"+name+"','"+email+"','"+mobile+"','"+pic+"')";
        cur.execute(query);
        res = "Data save successfully";
    else:
        pass
    return render(request,'demo.html',{'Res':res});
def display(request):
    return render(request,'display.html');
def ViewContact(request):
    res="";
    cur=mydb.cursor();
    cur.execute("select * from tbl_demo");
    result=cur.fetchall();
    r=cur.rowcount;
    if(r>0):
        res="<table class='table table-responsive'><tr style='background:brown;height:35px;color:white'>" \
            "<th>Name</th><th>Email</th><th>Mobile</th><th>Picture</th><th>Delete</th><tr>";
        for r in result:
            res+="<tr><td>"+r[0]+"</td><td>"+r[1]+"</td><td>"+r[2]+"</td><td>"+r[3]+"</td>" \
             "<td><span class='fa fa-trash' style='color:brown;font-size:22px;'></span></td></tr>";
        res+="</table>";
    else:
        res="No record found";
    return render(request,'AdminZone/ViewContact.html',{'Res':res});

def ViewRegistration(request):
    return render(request,'AdminZone/ViewRegistration.html');
#All views start of student zone here
def dashboard(request):
    id=request.session.get('uid');
    return render(request,'StudentZone/dashboard.html',{'ROll':id});
def MyProfile(request):
    return render(request,'StudentZone/MyProfile.html');
def Schangepassword(request):
    msg="";
    if request.method=="POST":
        oldpass=request.POST.get("txtoldpass");
        newpass=request.POST.get("txtnewpass");
        cpass=request.POST.get("txtcpass");
        if(newpass==cpass):
            id = request.session.get('uid');
            cur=mydb.cursor();
            query="update tbl_login set passwd='"+newpass+"' where userid='"+id+"' and passwd='"+oldpass+"'";
            cur.execute(query);
            msg="password change successfully..";
        else:
            msg="New password and confirm password not match";
    return render(request,'StudentZone/Schangepassword.html',{"Msg":msg});
# def feedback(request):
#     return render(request,'StudentZone/feedback.html');
@csrf_exempt
def feedback(request):
    id = request.session.get('uid');
    res="";
    if request.is_ajax():
        total=request.POST.get("Total");
        msg=request.POST.get("Msg");
        cur=mydb.cursor();
        cur.execute("insert into tbl_feedback values('"+total+"','"+msg+"','"+id+"')");
        res="feedback Submit succesfully";
        return HttpResponse(res);
    return render(request,'StudentZone/feedback.html');
#Adminzone calculations
def AddNotification(request):
    msg="";res="";
    if(request.method=="POST"):
        name=request.POST.get("txtnoti");
        desc=request.POST.get("txtdesc");
        cur.execute("insert into tbl_notification (NName,Ndesc) values('"+name+"','"+desc+"')")
        msg="Add Notification succsssfully..";
    else:
        cur.execute("select * from tbl_notification");
        result=cur.fetchall();
        a=cur.rowcount;
        if(a>0):

            res = "<table class='table table-responsive'><tr style='background:brown;height:35px;color:white'>" \
                  "<th>S.No</th><th>Name</th><th>Description</th><th>Delete</th><th>Update</th><tr>";
            for r in result:
                res += "<tr><td>"+str(r[0])+"</td><td>" + r[1] + "</td><td>" + r[2] + "</td><td><span class='fa fa-trash'></span></td><td><span class='fa fa-eye'></span></td></tr>";"<td><span class='fa fa-trash' style='color:brown;font-size:22px;'></span></td></tr>";
            res += "</table>";

        else:
            msg="No Record Found";
    return render(request,'AdminZone/AddNotification.html',{"Msg":msg,"Res":res});