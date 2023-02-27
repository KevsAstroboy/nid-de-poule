from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import PantholeSerializer,Checker
from .models import Pothole
from django.http import JsonResponse
from rest_framework import status
import boto3

import os

from django.views.decorators.csrf import csrf_exempt


path = 'My Dataset'
ndp_path = os.path.join(path + '/train/Pothole/')
bit_path = os.path.join(path + '/train/Plain/')

ndp_pro = []
bit_pro = []

# Create your views here.
class PantholeView(APIView):

    serializer_class = PantholeSerializer

    def get_queryset(self):
        potholes = Pothole.objects.all()
        return potholes


    def get(self, request, *args , **kwargs ):
        potholes = self.get_queryset()
        serializer = PantholeSerializer(potholes,many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = PantholeSerializer(data=request.data)
        if serializer.is_valid():
            # Initialiser le client Rekognition
            rekognition = boto3.client('rekognition')

            # Spécifier l'ARN de votre modèle Rekognition Custom Labels
            model_arn = 'arn:aws:rekognition:us-east-1:559990806063:project/potholes/version/potholes.2023-02-21T20.11.46/1677010305726'

            # Spécifier le nom du fichier image à partir duquel vous voulez faire des prédictions
            filename = request.FILES['pot_photo']
            #print(filename.content)
            # Charger l'image à partir du fichier
            # with open(filename, 'rb') as image_file:
            #     image = image_file.read()

            # Faire des prédictions sur l'image à l'aide de votre modèle
            response = rekognition.detect_custom_labels(
                Image={
                    'Bytes': filename.read()
                },
                ProjectVersionArn=model_arn,
                MinConfidence=50
            )

            # Récupérer les prédictions
            predictions = response['CustomLabels']

            # Afficher les prédictions
            for prediction in predictions:
                if prediction['Name'] == "potholes" and prediction['Confidence'] > 70:
                    serializer.save()
                    return Response({"hasError": False, "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"hasError": True, "data": "Ceci n'est pas un nid-de-poule."}, status=status.HTTP_400_BAD_REQUEST)
                # print(f"Label: {prediction['Name']}")
                # print(f"Confidence: {prediction['Confidence']}")
            #serializer.save()

        else:
            return Response({"hasError": True, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


