"""SMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from SMSApp.views import index,registration,contact,Login,demo,ViewContact,dashboard,MyProfile,Schangepassword,AddNotification,feedback
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index),
    path('index/',index),
    path('register/',registration),
    path('contact/',contact),
    path('login/',Login),
    path('demo/',demo),
    path('AdminZone/ViewContact/',ViewContact),
    path('StudentZone/index/', dashboard),
    path('StudentZone/MyProfile/',MyProfile),
    path('StudentZone/feedback/', feedback),
    path('StudentZone/Changepassword/',Schangepassword),
    path('AdminZone/AddNotification/',AddNotification),

]
