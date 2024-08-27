from rest_framework.decorators import api_view
from rest_framework.response import Response


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
