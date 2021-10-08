from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/signup', views.handlesignup, name='handlesignup'),
    path('profile/login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('addnote', views.addnote, name='addnote'),
    path('edit/note/<str:note_id>', views.editnote, name='editnote'),
    path('update/note/<str:note_id>', views.updatenote, name='updatenote'),
    path('delete/note/<str:note_id>', views.deletenote, name='deletenote')
]
