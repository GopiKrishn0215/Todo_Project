from django.db import models
from django.conf import settings

class ToDo(models.Model):
    user_name = models.CharField(max_length=20)
    task  = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,blank=True,null=True)
    status = models.CharField(max_length=20,default="Pending")
    file = models.FileField(upload_to="files/",max_length=150,null=True,default=None)



# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from myapp.models import MyModel

# def download_file_view(request, pk):
#     instance = get_object_or_404(MyModel, pk=pk)
#     file_url = instance.file_field.url

#     # Open the file and read its content
#     with open(file_url, 'rb') as file:
#         file_content = file.read()

#     # Create the HttpResponse object with the file content
#     response = HttpResponse(file_content, content_type='application/octet-stream')
    
#     # Set the Content-Disposition header to force download
#     response['Content-Disposition'] = f'attachment; filename="{instance.file_field.name}"'

#     return response

# Replace "<URL_TO_VIEWS_PY>" with the actual URL to your Django view
# url_to_views = "<URL_TO_VIEWS_PY>"

# response = requests.get(url_to_views)



