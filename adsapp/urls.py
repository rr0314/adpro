
from django.urls import path 
from .import views

urlpatterns = [
    path('',views.index),



    path('login/',views.login),
    path('logout/',views.logout),
    path('cont/',views.cont), 
   
    path('shop/',views.shop),
    path('single/',views.single),
    path('addcart/',views.addcart),
    path('check/',views.checkout),
    path('cart_update/',views.cart_update),
    path('cart_del/',views.cart_del),

    # path('reg/',views.reg),
    path('signform/',views.signupform),
    
    





    path('adminlog/',views.adminlog),
    path('adsign/',views.adsign),
    path('adlogout/',views.adlogout),

    path('dash/',views.dash),
    path('addproduct/',views.addproduct),
    path('upprod/',views.upprod),
    path('prodtab/',views.prodtab),
    path('prodel/',views.prodel),
    path('msgs/',views.msgs),
    path('msgdel/',views.msgdel),




    path('men/',views.men),
    path('women/',views.women),
    path('foot/',views.foot),
    path('run/',views.run),




    
]