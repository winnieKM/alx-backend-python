from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # use email instead of username

    def validate(self, attrs):
        # Map 'email' input to 'username' for the parent class
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
