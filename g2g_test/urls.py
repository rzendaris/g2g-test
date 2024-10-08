"""g2g_test URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from services.order.views import OrderView
from services.user.views import CustomerInfoView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API V1 endpoints
    url(
        r'^api/v1/',
        include([
            url(r'^customer/info/', CustomerInfoView.as_view(), name='customer-info-v1'),
            url(r'^order/', OrderView.as_view(), name='order-v1'),
        ]),
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
