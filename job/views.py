from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib import messages

# Create your views here.

def index(request):
    """Handles the index page request and renders the 'index.html' template."""
    return render(request, 'index.html')

def admin_login(request):
    """Handles the admin login page request and renders the 'admin_login.html' template."""
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
                                       
    return render(request, 'admin_login.html',{'error':error})

def employee_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request, user)
                    error="no"
                    return redirect('employee_home')  # Redirect to employee home page after successful login
                else:
                    error = "yes"
            except StudentUser.DoesNotExist:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'employee_login.html', {'error': error})

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != "pending":
                    login(request, user)
                    return redirect('recruiter_home')  # Redirect to recruiter dashboard after successful login
                else:
                    error = "yes"
            except Recruiter.DoesNotExist:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'recruiter_login.html', {'error': error})

def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES.get('image')
        p = request.POST['pwd']
        gen = request.POST['gender']
        e = request.POST['email']
        con = request.POST['contact']
        company = request.POST['company']
        try:
            # Create the User object with is_active=True to allow login
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p, is_active=True)
            # Create the Recruiter object with type as "recruiter" and status as "pending"
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type="recruiter", status="pending")
            messages.success(request, "Signup successful! Wait for admin approval.")
            return redirect('recruiter_login')  
        except Exception as e:
            print("Signup error:", e)
            error = "yes"
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'recruiter_signup.html', {'error': error})
    return render(request, 'recruiter_signup.html')

def employee_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES.get('image')
        p = request.POST['pwd']
        gen = request.POST['gender']
        e = request.POST['email']
        con = request.POST['contact']
        try:
            # Create the User object with is_active=True to allow login
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p, is_active=True)
            # Create the StudentUser object with type as "student"
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
            error="no"
            return render(request, 'employee_signup.html',{'error':error})
        except Exception as e:
            error="yes"
            d={'error':error}
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'employee_signup.html',d)
    return render(request, 'employee_signup.html')

def employee_home(request):
    if not request.user.is_authenticated:
        return redirect('employee_login') 
    user=request.user
    student=StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        
        
        gen = request.POST['gender']
        
        con = request.POST['contact']
        student.user.first_name =f
        student.user.last_name =l
        student.mobile =con
        student.gender =gen
        try:
            student.save()
            student.user.save()
            error="no"
            
        except Exception as e:
            error="yes"

        try:
            i = request.FILES.get('image')
            student.image=i
            student.save()
            error="no"
            
        except Exception as e:
            pass

    d={'student':student,'error':error}
    
    return render(request, 'employee_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    rcount=Recruiter.objects.all().count()
    scount=StudentUser.objects.all().count()
    d={'rcount':rcount,'scount':scount}   
    return render(request, 'admin_home.html',d)

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        
        
        gen = request.POST['gender']
        
        con = request.POST['contact']
        recruiter.user.first_name =f
        recruiter.user.last_name =l
        recruiter.mobile =con
        recruiter.gender =gen
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
            
        except Exception as e:
            error="yes"

        try:
            i = request.FILES.get('image')
            recruiter.image=i
            recruiter.save()
            error="no"
            
        except Exception as e:
            pass

    d={'recruiter':recruiter,'error':error}
    return render(request, 'recruiter_home.html',d)

def recruiter_dashboard(request):
    # This is a placeholder for your recruiter dashboard view
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    return render(request, 'recruiter_dashboard.html')

def logout_user(request):
    """Handles logout and redirects to the homepage."""
    logout(request)
    return redirect('index')  # Redirect to the index page after logout
def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    data=StudentUser.objects.all()
    return render(request, 'view_users.html',{'data':data})
def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    student=StudentUser.objects.get(id=pid)
    student.delete()
    return redirect('view_users')
def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    student=StudentUser.objects.get(id=pid)
    student.delete()
    return redirect('recruiter_all')
def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    data=Recruiter.objects.filter(status='pending')
    return render(request, 'recruiter_pending.html',{'data':data})
def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    error=""
    data=Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        data.status=s
        try:
            data.save()
            error="no"
        except:
            error="yes"
    d={'data':data,'error':error}
    return render(request, 'change_status.html',d)
def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    data=Recruiter.objects.filter(status='Accept')
    return render(request, 'recruiter_accepted.html',{'data':data})
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    data=Recruiter.objects.filter(status='Rejected')
    return render(request, 'recruiter_rejected.html',{'data':data})
def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    data=Recruiter.objects.all()
    return render(request, 'recruiter_all.html',{'data':data})
def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  # Redirect to login page if not authenticated
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
            else:   
               error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'change_passwordadmin.html',d)
def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')  # Redirect to login page if not authenticated
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
            else:   
               error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
            else:   
               error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'change_passwordrecruiter.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    error=""
    if request.method == 'POST':
        jd = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST.get('enddate')
        sal = request.POST['salary']
        l = request.FILES.get('logo')
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user=request.user
        recruiter=Recruiter.objects.get(user=request.user)
        try:
            # Create the User object with is_active=True to allow login
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,tittle=jd,salary=sal,image=l,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
            error = "no"
        except Exception as e:
             print("Error:", e)  # Debug ke liye
             error = "yes"    
    
    return render(request, 'add_job.html',{'error':error})

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    user=request.user
    recruiter=Recruiter.objects.get(user=request.user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request, 'job_list.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    error=""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST.get('enddate')
        sal = request.POST['salary']
        l = request.FILES.get('logo')
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        job.tittle = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            # Create the User object with is_active=True to allow login
            Job.objects.create_user(recruiter=request.user,start_date=sd,end_date=ed,tittle=jt,salary=sal,image=l,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
            error = "no"
        except:
            error = "yes"   
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:  
                pass
        else:
             pass      

        if ed:
            try:
                job.end_date=ed
                job.save()
            except:  
                pass
        else:
             pass              
    d={'error':error,'job':job}
    return render(request, 'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    error=""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
       
        cl = request.FILES['logo']
        job.image = cl
   
        try:
            job.save()
            error = "no"
        except:
            error = "yes"   
               
    d={'error':error,'job':job}
    return render(request, 'change_companylogo.html',d)

def latest_jobs(request):
    data=Job.objects.all().order_by('-start_date')
    return render(request, 'latest_jobs.html',{'data':data})

def employee_latestjobs(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter()
    li=[]
    for i in data:
        li.append(i.job.id)
    return render(request, 'employee_latestjobs.html',{'job':job,'li':li})

def job_detail(request,pid):
    job=Job.objects.all().get(id=pid)
    
    return render(request, 'job_detail.html',{'job':job})

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('employee_login')  # Redirect to login page if not authenticated
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date > date1:
        error="not open" 
    else:    
        if request.method == 'POST':
       
          r = request.FILES['resume']
          Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
          error="done"


    d={'error':error}
    return render(request, 'applyforjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  # Redirect to login page if not authenticated
    
    data=Apply.objects.all()
      
               
    d={'data':data}
    return render(request, 'applied_candidatelist.html',d)

def contact(request):
    return render(request, 'contact.html')
