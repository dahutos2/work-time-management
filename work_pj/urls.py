
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from work_time import views
from django.views.generic import TemplateView
from django.contrib.auth.models import Group


admin.site.site_header = 'システム管理サイト'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)

urlpatterns = [
    path('dahutos-admin/', admin.site.urls),
    path("", login_required(views.Index.as_view()), name="index"),
    path('', include("django.contrib.auth.urls")),
    path("sign-up/", views.SignUpView.as_view(), name="signup"),
    path('user_update/<pk>', views.UserUpdate.as_view(), name="user_update"),
    path('work_time/', views.MyWork.as_view(), name='mywork'),
    path('work_time/<int:year>/<int:month>/<int:day>/', views.MyWork.as_view(), name='mywork'),
    path('update/<pk>', views.Update.as_view(), name="update"),
    path('work_index/', views.WorkIndex.as_view(), name='work_index'),
]
