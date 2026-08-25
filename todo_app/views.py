from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

# TODO: Implement login view for users; we will create a new branch for that

@api_view(['GET'])
def test_api(request):
    return Response(
        {
            "message": True
        }
    )
