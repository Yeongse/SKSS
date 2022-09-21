from django.urls import path

from . import views

app_name = 'substitute'

urlpatterns = [
    path('', views.index, name='index'), 
    path('login', views.login, name='login'), 
    path('initialize', views.initialize, name='initialize'), 
    path('home/<int:year>/<int:month>', views.home, name='home'), 
    path('past', views.past, name='past'), 
    path('specification/<int:ask_id>', views.specification, name='specification'), 
    path('revise/<int:ask_id>', views.revise, name='revise'), 
    path('make', views.make, name='make'), 
    path('confirmAsk', views.confirmAsk, name='confirmAsk'), 
    path('confirmEntry', views.confirmEntry, name='confirmEntry'), 
    path('logout', views.logout, name='logout'), 
]