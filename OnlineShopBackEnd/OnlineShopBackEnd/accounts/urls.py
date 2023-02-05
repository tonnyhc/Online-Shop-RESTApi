from django.urls import path
from OnlineShopBackEnd.accounts.views import SignUpView, SignInView, SignOutView


urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign up view'),
    path('sign-in/', SignInView.as_view(), name='sign in view'),
    path('sign-out/', SignOutView.as_view(), name='sign out view'),
]