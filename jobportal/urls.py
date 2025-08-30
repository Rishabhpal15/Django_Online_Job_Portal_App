"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from job.views import employee_login, employee_signup, index, admin_login,latest_jobs,applied_candidatelist, recruiter_login,employee_home,recruiter_home,logout_user, recruiter_signup,admin_home,delete_user,recruiter_pending,change_status,recruiter_accepted,recruiter_rejected,recruiter_all,delete_recruiter,change_passwordadmin,view_users,change_passworduser,add_job,change_passwordrecruiter,job_list,edit_jobdetail,change_companylogo,employee_latestjobs,job_detail,applyforjob,recruiter_dashboard,contact # Explicitly import the views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', index, name="index"),  # Home page route
    path('admin_login', admin_login, name="admin_login"),  # Admin login route
    path('employee_login', employee_login, name="employee_login"),
    path('recruiter_login', recruiter_login, name="recruiter_login"),
    path('recruiter_signup', recruiter_signup, name="recruiter_signup"),
    path('employee_signup', employee_signup, name="employee_signup"),
    path('employee_home', employee_home, name="employee_home"),
    path('recruiter_home', recruiter_home, name="recruiter_home"),
    path('admin_home', admin_home, name="admin_home"),
    path('admin_login', admin_login, name="admin_login"),
    path('Logout', logout_user, name="Logout"),
    path('view_users/', view_users, name="view_users"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('recruiter_pending', recruiter_pending, name="recruiter_pending"),
    path('change_status/<int:pid>', change_status, name="change_status"),
    path('recruiter_accepted', recruiter_accepted, name="recruiter_accepted"),
    path('recruiter_rejected', recruiter_rejected, name="recruiter_rejected"),
    path('recruiter_dashboard', recruiter_dashboard, name="recruiter_dashboard"),
    path('recruiter_all', recruiter_all, name="recruiter_all"),
    path('delete_recruiter/<int:pid>', delete_recruiter, name="delete_recruiter"),
    path('change_passwordadmin', change_passwordadmin, name="change_passwordadmin"),
    path('change_passworduser', change_passworduser, name="change_passworduser"),
    path('change_passwordrecruiter', change_passwordrecruiter, name="change_passwordrecruiter"),
    path('add_job', add_job, name="add_job"),
    path('job_list', job_list, name="job_list"),
    path('edit_jobdetail/<int:pid>', edit_jobdetail, name="edit_jobdetail"),
    path('change_companylogo/<int:pid>', change_companylogo, name="change_companylogo"),
    path('latest_jobs', latest_jobs, name="latest_jobs"),
    path('employee_latestjobs', employee_latestjobs, name="employee_latestjobs"),
    path('job_detail/<int:pid>', job_detail, name="job_detail"),
    path('applied_candidatelist', applied_candidatelist, name="applied_candidatelist"),
    path('applyforjob/<int:pid>', applyforjob, name="applyforjob"),
    path('contact', contact, name="contact"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

