from django.conf.urls import url

from spider_app import views

app_name = 'spider_app'
urlpatterns = [
    url(r'^$', views.pages),
]
