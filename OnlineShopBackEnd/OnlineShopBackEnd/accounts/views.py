from django.contrib.auth import get_user_model
from rest_framework.authtoken import views as authtoken_views
from rest_framework.authtoken import models as authtoken_models
from rest_framework import generics as rest_generic_views, views as rest_views
from rest_framework.response import Response

from OnlineShopBackEnd.accounts.serializers import SignUpSerializer

UserModel = get_user_model()


class SignUpView(rest_generic_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = SignUpSerializer


class SignInView(authtoken_views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = authtoken_models.Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            'user_id': user.pk,
            'username': user.username,
        })


class SignOutView(rest_views.APIView):
    def get(self, request):
        return self.__perform_logout(request)

    def post(self, request):
        return self.__perform_logout(request)

    @staticmethod
    def __perform_logout(request):
        try:
            request.user.auth_token.delete()
            return Response({
                'message': "User signed out!"
            })
        except AttributeError as e:
            return Response({
                'message': "No signed in user, cant perform sign-out!"
            })
