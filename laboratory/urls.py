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
    path(r'', views.index_html),
    path(r'index', views.index_html),
    path(r'uploadfile',views.uploadfile),

    #guide
    path(r'guide', views.guide_html),

    #question
    path(r'question', views.question_html),

    #todo
    path(r'todo', views.todo_html),
    path(r'getdirsbyupload',views.getdirsbyupload),
    path(r'openfolder',views.openfolder),
    path(r'backtoprevious',views.backtoprevious),
    path(r'deletefile',views.deletefile),
    path(r'synfolderlist',views.synfolderlist),
    path(r'renamefile',views.renamefile),

    #doing
    path(r'doing', views.doing_html),
    path(r'progress',views.progress),

    #done
    path(r'done', views.done_html),
    path(r'resultfiles',views.resultfiles),
    path(r'downloadbigfile',views.downloadbigfile),

    #stop thread
    path(r'stop', views.stop_task),

    #aboutus
    path(r'aboutus', views.aboutus_html),

    #contactus
    path(r'contactus', views.contactus_html),

    #settings
    path(r'settings', views.settings_html),
    path(r'settingsvalue',views.settingsvalue),
    path(r'getDefaultConfig',views.getDefaultConfig),

    #navbar
    path(r'navbar', views.navbar_html),

    #header
    path(r'header', views.header_html),
]