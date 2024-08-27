from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['Get']) #Pass the menthod that this function accepts
def index(request):
    courses = {
        'course_name' : 'Python',
        'Learn' : ['Flask', 'Django', 'FastAPI'],
        'Duration' : '20 Hours'
    }
    return Response(courses)