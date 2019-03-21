"""stereo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from app.views import Home, StereotypeQ, PersonalQ, TemplateTest, SubmitStereo, SubmitPersonal, load_countries, Results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view()),
    path('sform/',StereotypeQ.as_view(), name='s_form'),
    path('pform/', PersonalQ.as_view(), name='p_form'),
    path('test/', TemplateTest.as_view()),
    path('submits/<int:answer>', SubmitStereo.as_view(), name='submit-s'),
    path('submitp/<str:answer>', SubmitPersonal.as_view(), name='submit-p'),
    path('results', Results.as_view(), name='results'),

    path('ajax/load-cities/', load_countries, name='ajax_load_countries'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()