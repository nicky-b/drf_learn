from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer, LoginSerializer, RegisterSerializer
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from rest_framework.decorators import action


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'error': "invalid credentials"
            }, status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = serializer.data["username"], password = serializer.data["password"])

        if not user:
            return Response({
                'status': False,
                'error': "invalid credentials"
            }, status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user) # Get or create the token
        print(token)

        return Response({
            'status': True,
            'message': "login successful",
            "token": str(token)
        }, status.HTTP_202_ACCEPTED)

class RegisterAPI(APIView):
    #creating a post req to fetsch the data 
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'error': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        return Response({'status': True, 'message': 'user created'}, status.HTTP_201_CREATED) 

    



class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #creating API CRUD Operations using APIVIew Class
    def get(self, request):
        objs = Person.objects.filter(color__isnull = False)
        try:
            print(request.user) # Prints authenticaated users

            page = request.GET.get('page', 1) # no page no mentioned returns page 1
            page_size = 3 #No of records in each page
            
            paginator = Paginator(objs, page_size)

            print(paginator.page(page))

            # Only serialize the objects o n the current page
            serializer = PersonSerializer(paginator.page(page), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "status": False,
                "message": "invalid page"
            })
    
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)  
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({"message": "person deleted"})

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        print(data) # To debugu the data 
        data = serializer.validated_data
        return Response({'message':'success'})
    else:
        # Log the errors to the console or return them in the response
        print(serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['Get', 'POST']) #Pass the menthod that this function accepts
def index(request):
    courses = {
        'course_name' : 'Python',
        'Learn' : ['Flask', 'Django', 'FastAPI'],
        'Duration' : '20 Hours'
    }

    if request.method == 'GET':
        print('You requested a GET method')
        return Response(courses)
    elif request.method == 'POST':
        print('You requested a POST method')
        return Response(courses)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    #creating API CRUD Operations using @api_view decorator with a function
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull = False)
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({"message": "person deleted"})


class PersonViewSet(viewsets.ModelViewSet):
    #creating API CRUD Operations using ModelVIewSet 
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    #If you want to limit the api methods, you need to only accept GET and POST but not PUT/Patch/DELETE, use below and can make modofications as well
    http_method_name = ['get', 'post']
    #Search feature
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer = PersonSerializer(queryset, many = True) 
        return Response({"status": 200, "data": serializer.data})

    @action(detail=True, methods=['post']) #use GET or POST
    def send_mail_to_person(self, request, pk):
        #url used api/people/15/send_mail_to_person/
        obj = Person.objects.get(pk = pk)
        serializer = PersonSerializer(obj)
        return Response({
            "status":True,
            "message": "email sent successfully",
            "data": serializer.data
        })