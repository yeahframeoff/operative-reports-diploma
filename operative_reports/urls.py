"""operative_reports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from remote_db import views as remote_db_views


from .view import hello, db_test
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^hello', hello),
    url(r'^db_info/', db_test),
    url(r'^api/diagram-types/?', remote_db_views.get_types),
    url(r'^remote-db/(?P<pk>\d+)/?', remote_db_views.DatabaseConnectionAPIView.as_view()),
    url(r'^remote-db/', remote_db_views.DatabaseConnectionCreateAPIView.as_view()),
    url(r'^widgets/(?P<pk>\d+)/?', remote_db_views.WidgetConfigAPIView.as_view()),
    url(r'^widgets/', remote_db_views.WidgetConfigCreateAPIView.as_view()),
]
