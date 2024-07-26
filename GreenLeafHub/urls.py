"""
URL configuration for GreenLeafHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from GreenWebsite.views import dashboard, logout_user, signup_view, login_user, CustomPasswordResetView, send_test_email,product,submit_review,add_to_cart,view_cart,add_product ,product_list,edit_product, payment_view, process_payment , search,product_gallery
from GreenWebsite.views import (Articles,
                                ArticleListView,
                                ArticleDetailView,
                                ArticleCreateView, ArticleUpdateView,
                                ArticleDeleteView,UserArticleListView)

from GreenWebsite.views import (dashboard, logout_user, signup_view, login_user,CustomPasswordResetConfirmView, CustomPasswordResetView,
                                send_test_email,product,submit_review,add_to_cart,remove_from_cart,view_cart,add_product ,
                                product_list,
                                update_cart , edit_product, payment_view, process_payment,search,order_history,product_gallery)
from GreenWebsite.views import subscribe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('send_mail/',send_test_email,name='send_mail'),
    path('product/<int:pk>',product,name='product'),
    path('search/', search, name='search'),

    path('product-gallery/',product_gallery,name='product_gallery'),

    path('submit_review/<int:product_id>/',submit_review,name='submit_review'),
    path('add_product', add_product, name='add_product'),
    path('product_list', product_list, name='product_list'),
    path('edit_product/<int:pk>', edit_product, name='edit_product'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', view_cart, name='cart'),
    path('payment/', payment_view, name='payment_page'),
    path('process_payment/', process_payment, name='process_payment'),
    path('article-home/', ArticleListView.as_view(), name='article-home'),
    path('article-detail/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article-new/', ArticleCreateView.as_view(), name='article-create'),
    path('article-detail/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article-detail/<int:pk>/delete', ArticleDeleteView.as_view(), name='article-delete'),
    path('user-articles/<str:username>', UserArticleListView.as_view(), name='user-articles'),
    path('order_history/', order_history, name='order_history'),
    path('payment/', payment_view, name='payment_page'),
path('update-cart/', update_cart, name='update_cart'),
path('subscribe/', subscribe, name='subscribe'),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)