from django.urls import path, include

from OnlineShopBackEnd.admin_panel.views import GetDashboardView, AddProductView, ProductsListView, DeleteProductView, \
    EditProductView, GetCategories, AddCategoryView, DeleteCategoryView, OrdersListView, OrderDetailsView, \
    change_order_status, DiscountCodeListView, CreateDiscountCodeView, GetCustomersListView

urlpatterns = (
    path('dashboard/', GetDashboardView.as_view(), name='dashboard view'),
    path('add-product/', AddProductView.as_view(), name='add product'),
    path('products/', include([
        path('', ProductsListView.as_view(), name='products list'),
        path('categories/', GetCategories.as_view(), name='categories list'),
        path('categories/create/', AddCategoryView.as_view(), name='add category'),
        path('categories/delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete category'),
        path('<str:slug>/delete/', DeleteProductView.as_view(), name='delete product'),
        path('<str:slug>/edit/', EditProductView.as_view(), name='edit product'),
    ])),
    path('orders/', include([
        path('', OrdersListView.as_view(), name='orders list'),
        path('<int:pk>/', OrderDetailsView.as_view(), name='order details'),
        path('<int:pk>/change-status/', change_order_status, name='change order status'),
    ])),
    path('discounts/', include([
        path('', DiscountCodeListView.as_view(), name='discount code list'),
        path('create-discount/', CreateDiscountCodeView.as_view(), name='create discount code'),
    ])),
    path('customers/', include([
        path('', GetCustomersListView.as_view(), name='customers list view'),
    ])),
)
