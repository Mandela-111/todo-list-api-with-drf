from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from todo_app.serializers import LoginSerializer, RegisterSerializer, UserListSerializer
from todo_app.models import Tasks
from todo_app.serializers import TasksSerializer
from django.shortcuts import get_object_or_404


# Create your views here.

# TODO: LoginView is now what we've got to do. We get the incoming request data and serialize it, check if it's valid
#  or not and do what needs to be done.
#  Step 2: We move on to the serializers, make sure we inherit, timestamps. It's bad practice to for a check authorization
#  with data from the client side. We should stick to auth_tokens and JWTs. Since we want each user to own their tasks,
#  we set the owner here in the server side by 'serializer.save(user=request.user)'




class RegisterAPI(APIView):
    def post(self, request):

        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            try:
                user = serializer.save()

                token, _ = Token.objects.get_or_create(user=user)

            except IntegrityError:
                status_message = f"{data.username} is already taken"
                return Response(
                    {
                        "success": False,
                        "errors": {
                            "username": status_message
                        }
                    }
                )


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


    def get(self, request):
        users = User.objects.all()

        serializer = UserListSerializer(users, many=True)

        return Response({
            "message": True,
            "users": serializer.data,
        }, status=status.HTTP_200_OK)


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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TasksAPI(APIView):
    def get(self, request, task_id = None):

        user = request.user

        if task_id is None:

            tasks = Tasks.objects.filter(user=user)
            serializer = TasksSerializer(tasks, many=True)

            return Response({
                "message": True,
                "tasks": serializer.data,
            }, status=status.HTTP_200_OK)
        else:

            # foreign key objects are always tied to (user) are tied to their tasks. The user has to be the same as the
            # one that owns the task. If not, we return a 404 error.
            task = get_object_or_404(Tasks, id=task_id, user=user)
            serializer = TasksSerializer(task)

            return Response({
                    "message": True,
                    "task": serializer.data,
                }, status=status.HTTP_200_OK)




    def post(self, request):
        data = request.data

        serializer = TasksSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": True,
                "task": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": False,
                "errors": serializer.errors

            },
            status= status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, task_id):
        user = request.user
        task = get_object_or_404(Tasks, id=task_id, user=user)

        serializer = TasksSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Task edited successfully",
                "task": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(
            {
                "message": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, task_id):
        user = request.user
        task = get_object_or_404(Tasks, id=task_id, user=user)

        task.delete()

        return Response({
            "message": "Task deleted successfully"
        }, status=status.HTTP_200_OK)

# TODO: a new api for marking if a task is complete or not. Now we're receiving data from our client
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def is_completed(request, task_id):
    user = request.user
    data = request.data

    task = get_object_or_404(Tasks, id=task_id, user=user)

    serializer = TasksSerializer(task, data=data, partial=True)

    if serializer.is_valid():
        task.isCompleted = data['isCompleted']
        serializer.save()

        return Response({
            "message": "Task completion edited successfully",
            "task": serializer.data
        }, status=status.HTTP_200_OK)

    return Response(
            {
                "message": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# TODO: One last api to retrieve all completed tasks by a user. Filtering is what we've got to do.
#  We know what to do, we add the permission classes and everything. We filter both user and isCompleted.
#  We serialize, then we return a  response.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def completed_tasks(request):
    user = request.user
    data = request.data

    tasks = Tasks.objects.filter(user=user, isCompleted=True)

    serializer = TasksSerializer(tasks, many=True)

    return Response({
        "message": "Retrieved all completed tasks successfully",
        "data": [serializer.data]
    }, status=status.HTTP_200_OK)