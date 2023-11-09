"""bdjProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from .views import summary_from_url ,summary_from_text, recent_summary, user_summaries

urlpatterns = [

    path('summary/url/', summary_from_url),
    path('summary/url', summary_from_url),
    
    path('summary/text/', summary_from_text),
    path('summary/text', summary_from_text),
    
    path('user/summaries/', user_summaries),
    path('user/summaries', user_summaries),
    
    path('summary/recent/', recent_summary),
    path('summary/recent', recent_summary),
]
