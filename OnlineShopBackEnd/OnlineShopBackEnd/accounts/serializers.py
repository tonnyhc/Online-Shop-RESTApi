from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers, exceptions

UserModel = get_user_model()
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password', 'gender')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def validate(self, data):
        user = UserModel
        password = data.get('password')
        errors = {}
        try:
            password_validation.validate_password(password, user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

    def to_representation(self, instance):
        user_representation = super().to_representation(instance)
        user_representation.pop('password')
        return user_representation

"""This serializer was for use when the required field for login was the email, but it throwed some errors so i changed it to username
    can try fixing it later on """
# class LoginSerializer(serializers.py.ModelSerializer):
#     email = serializers.py.EmailField(max_length=255, min_length=3)
#     password = serializers.py.CharField(max_length=68, min_length=6, write_only=True)
#
#     # tokens = serializers.py.SerializerMethodField()
#     #
#     # def get_tokens(self, obj):
#     #     user = UserModel.objects.get(email=obj['email'])
#     #
#     #     return {
#     #         'refresh': user.tokens()['refresh'],
#     #         'access': user.tokens()['access']
#     #     }
#
#     class Meta:
#         model = UserModel
#         fields = ['email', 'password', ]
#                   # 'tokens']
#
#     def validate(self, attrs):
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')
#         filtered_user_by_email = UserModel.objects.filter(email=email)
#         user = auth.authenticate(email=email, password=password)
#
#         if not user:
#             raise AuthenticationFailed('Invalid credentials, try again')
#         if not user.is_active:
#             raise AuthenticationFailed('Account disabled, contact admin')
#         # if not user.is_verified:
#         #     raise AuthenticationFailed('Email is not verified')
#
#         return {
#             'email': user.email,
#             'username': user.username,
#             # 'tokens': user.tokens()
#         }
#
#         return super().validate(attrs)