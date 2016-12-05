from django.conf.urls import url
from . import views

app_name = 'elections'
urlpatterns = [
    url(r'^$', views.index, name = 'home'),
    url(r'^areas/(?P<area>[가-힣]+)/$', views.areas), #url에 있는 area는 views.areas 로 넘겨주는 매개변수가 된다. 따라서 받을 때도 area 로 받아주면 된다.
    url(r'^areas/(?P<area>[가-힣]+)/results$', views.results),
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls),
    url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates),
]
