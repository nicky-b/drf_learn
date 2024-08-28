from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer, LoginSerializer


class PersonAPI(APIView):
    #creating API CRUD Operations using APIVIew Class
    def get(self, request):
        objs = Person.objects.filter(color__isnull = False)
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    
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

    #Search feature
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer = PersonSerializer(queryset, many = True) 
        return Response({"status": 200, "data": serializer.data})