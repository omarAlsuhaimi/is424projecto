from django.urls import path,include
from . import views
urlpatterns=[
    path("",views.login,name='login'),
    path("validateLogin", views.validate_login, name='validate_login'),
    path("register", views.register, name='register'),
    path("trip/<int:id>",views.displayBus,name="trip"),
    path("displayBusses",views.displayBusses,name="displayBusses")
]