
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from uploads import views
from django_private_chat import urls as django_private_chat_urls
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator




urlpatterns = [
    url(r'^', include('django_private_chat.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^',include('mysite.urls')),
    url(r'^home/',include('home.urls')),
    url(r'^profile/',include('profiledet.urls')),
    url(r'^test/',include('testres.urls')),
    url(r'^view/$',views.home),
    url(r'^view/uploads/$',views.upl),
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': '../templates/registration/logout.html'}, name='logout'),
    url(r'^forum/',include('forum.urls')),
    url(r'^presc/',include('presc.urls')),
    url(r'^schedule/', include('scheduler.urls')),
    url(r'^admin/shell/', include('django_admin_shell.urls')),
             ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
