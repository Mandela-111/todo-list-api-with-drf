from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

# TODO: Implement login view for users; we will create a new branch for that.
#  Let's start with the name of the endpoint. // To login we would need data from the user to verify of they're
#  authenticated. Which would mean we would need a Login serializer for that, a UserListSerialzier to display users.

@api_view(['POST'])
def login(request):
    return Response(
        {
            "message": True
        }
    )
