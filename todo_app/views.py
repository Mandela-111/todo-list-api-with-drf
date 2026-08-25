from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from todo_app.serializers import LoginSerializer


# Create your views here.

# TODO: LoginView is now what we've got to do. We get the incoming request data and serialize it, check if it's valid
#  or not and do what needs to be done

@api_view(['POST'])
def login(request):

    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": True,
            "user": UserListSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_200_OK)



    return Response(
        {
            "message": False,
            "errors": serializer.errors
        },
        status= status.HTTP_400_BAD_REQUEST
    )
