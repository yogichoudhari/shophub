from django.urls import path , re_path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm ,CustomPasswordResetForm

urlpatterns = [
    path('',views.home,name = 'home'),
    path('product_desc/<int:id>',views.product_desc,name='product_desc'),
    path('cart/' ,views.cart,name='cart'),
    path('add_to_cart/<int:id>' ,views.add_to_cart,name='add_to_cart'),
    path('cart_plus/',views.cart_plus,name='cart_plus'),
    path('cart_minus/',views.cart_minus,name='cart_minus'),
    path('remove_product/',views.remove_product,name='remove_product'),
    path('checkout/',views.checkout,name='checkout'),
    path('profile/',views.profile,name='profile'),
    path('signup/',views.signup,name='signup'),
    path('verify/<str:token>', views.verify,name='verify'),
    path('login/',views.login,name='login'),
    # path('password_change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html',form_class=MyPasswordChangeForm,success_url='/'),name='password_change'),
    path('password_change/',views.CustomPasswordChangeView.as_view(),name='password_change'),
    path('password_success/',views.password_success,name='password_success'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',views.CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('orders/',views.orders,name='orders'),
    path('addresses/',views.addresses,name='addresses'),
    path('all_product/',views.all_product,name='all_product'),
    path('mens_wear/',views.mens_wear,name='mens_wear'),
    path('womens_wear/',views.womens_wear,name='womens_wear'),
    path('mobile/',views.mobile,name='mobile'),
    path('home_appliances/',views.home_appliances,name='home_appliances'),
    path('search_item/',views.search_item,name='search_item')
]  