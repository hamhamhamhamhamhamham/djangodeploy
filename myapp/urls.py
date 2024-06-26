
from django.contrib import admin
from django.urls import path,include
from . import views

# name space : url NAME
app_name="my_papp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index),
    path("products/",views.products,name="products"),
    path("products/<int:pk>/",views.ProductDetailView.as_view(),name="product_detail"),
    path("products/add/",views.ProductCreateView.as_view(),name="product_add"),
    path("products/update/<int:pk>/",views.ProductUpdateView.as_view(),name="update_product"),
    path("products/delete/<int:pk>/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("myproducts/",views.my_products,name="my_products"),
    path("success/",views.PaymentSuccessView.as_view(),name="success"),
    path("failed/",views.PaymentFailedView.as_view(),name="failed"),
    path("api/checkout_session/<id>/",views.create_checkout_session,name="api_checkout_session")
]