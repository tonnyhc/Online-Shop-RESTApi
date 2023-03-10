from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken import views as authtoken_views
from rest_framework.authtoken import models as authtoken_models
from rest_framework import generics as rest_generic_views, views as rest_views, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from OnlineShopBackEnd.accounts.serializers import SignUpSerializer, AccountDetailsSerializer

UserModel = get_user_model()


class SignUpView(rest_generic_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, created = authtoken_models.Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class AccountDetails(rest_generic_views.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDetailsSerializer
    queryset = UserModel.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user.username)

        return obj
