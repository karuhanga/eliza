from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from app.models import Action


class ActionView1(APIView):
    def post(self, request):
        data = request.data
        message = data.message
        
        action = Action(name=message.body)
        action.save()
