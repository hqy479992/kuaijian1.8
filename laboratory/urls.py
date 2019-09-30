"""laboratory URL Configuration

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
from kuaijian import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #index
    path(r'',views.indexhtml),
    path(r'index',views.indexhtml),
    path(r'uploadfile',views.uploadfile),

    #guide
    path(r'guide',views.guidehtml),

    #question
    path(r'question',views.questionhtml),

    #todo
    path(r'todo',views.todohtml),
    path(r'getdirsbyupload',views.getdirsbyupload),
    path(r'openfolder',views.openfolder),
    path(r'backtoprevious',views.backtoprevious),
    path(r'deletefile',views.deletefile),
    path(r'synfolderlist',views.synfolderlist),
    path(r'renamefile',views.renamefile),

    #doing
    path(r'doing',views.doinghtml),
    path(r'progress',views.progress),

    #done
    path(r'done',views.donehtml),
    path(r'resultfiles',views.resultfiles),
    path(r'downloadbigfile',views.downloadbigfile),

    #aboutus
    path(r'aboutus',views.aboutushtml),

    #contactus
    path(r'contactus',views.contactushtml),

    #settings
    path(r'settings',views.settingshtml),
    path(r'settingsvalue',views.settingsvalue),
    path(r'getDefaultConfig',views.getDefaultConfig),

    #navbar
    path(r'navbar',views.navbarhtml),

    #header
    path(r'header',views.headerhtml),
]