from django.shortcuts import HttpResponse 
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings
from .models import ToDo
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

def get_csrf_token(request):
    # Generate and return the CSRF token
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


# Create your views here.
def index(request):
    return HttpResponse("index")


def history(request,userName,status):
    data = ToDo.objects.filter(user_name=userName, status=status)
    tasks = []
    files = []
    description = []
    for item in data:
        tasks.append(item.task)
        file_url = request.build_absolute_uri(item.file.url)
        files.append(file_url) 
        description.append(item.description)
    response_data = {
        "tasks": tasks,
        "files": files,
        "description": description,
    }
    return response_data


def delete_tasks(request):
    selected_tasks = request.data.get('tasks', [])
    ToDo.objects.filter(task__in=selected_tasks).delete()
    return "deleted"
    
    
def create_task(request,userName,task,description,status):
    data = ToDo.objects.all()
    boolean = True
    for item in data:
        if item.task == task and item.status == "Pending" and item.user_name == userName:
            boolean = False
    if boolean:
        ToDo.objects.create(
            user_name=userName,
            task=task,
            description=description,
            status=status
            )
        
    return JsonResponse({"SUCCESS":"WOW"})

    
def read_task(request,userName):
    data = ToDo.objects.filter(user_name=userName,status="Pending")
    task = []
    for item in data:
        task.append(item.task)       
    response_data = {
        "task" : task,
    }       
    return response_data


def upload_file(request,userName,task,description,status,uploaded_file):
    updating_obj = ToDo.objects.filter(user_name=userName, task=task, status="Pending").first()
    updating_obj.description = description
    updating_obj.status = status
    save_directory = 'files/'
    updating_obj.file = default_storage.save(save_directory + uploaded_file.name, uploaded_file)
    updating_obj.save()
    response_data={'message': 'File uploaded successfully'}
    return response_data

@csrf_exempt
def fetch_saved_data_from_session(request):
    if request.method == "GET":
        print("checking if the call is being made")
        try:
            saved_data = request.session.get('saved_data')
            print(saved_data,"###############################################")
            response = {"saved_data":saved_data}
            return JsonResponse(response)
        except:
            print("exception occured")
            return JsonResponse({"saved_data":""})

@csrf_exempt
def save_data_in_session(request):
    if request.method == "POST":
        user_input = request.GET.get('user_input')
        # print(user_input)
        # Store user input in session
        request.session['user_input'] = user_input
        
        if (request.session['user_input']):
            print("*"*10, user_input,"*"*10)
        return JsonResponse({"input":user_input})
    

def get_user_id(request):
    if request.user.is_authenticated:
        return JsonResponse({"response":True})
    else:
        return JsonResponse({"response":False})

class Todo(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            discription = self.request.GET.get('discription')           
            if Type == "history":
                response = history(request,userName,status)
            elif Type == "delete":
                response = delete_tasks(request)
            elif Type == "create":
                response = create_task(request,userName,task,discription,status)
            elif Type == "read":
                response = read_task(request,userName) 
            elif Type == "fetch_session_data": 
                response = fetch_saved_data_from_session(request)
                return HttpResponse(response)           
            return JsonResponse(response,safe=False)           
        except Exception as e:
            return Response({'error': str(e)})

    def post(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            description = self.request.GET.get('description')
            uploaded_file = self.request.FILES.get('file')
            data = self.request.POST.get('data')
            print(data)
            if Type == "history":
                response = history(request,userName)
            elif Type == "create":
                response = create_task(request,userName,task,description,status)
            elif Type == "read":
                response = read_task(request,userName)
            elif Type == "uploadfile":
                response = upload_file(request,userName,task,description,status,uploaded_file)
            elif Type == "save_session_data":
                response = save_data_in_session(request,data)
                
            return JsonResponse(response,safe=False)
        except Exception as e:
            return Response({'error': str(e)})
            
    
    
class DataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            data = {"Userid":user_id}
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=401)
        
        