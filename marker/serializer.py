from PIL import ImageChops, Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

from rest_framework import serializers
from .models import Pothole

actual_error = 0


class PantholeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pothole
        fields = ['id','pot_photo','pot_latitude','pot_longitude','status']



class Checker:

    # def compare_image(image,dataset_images,result_data):
    #     im1 = Image.open(image)
    #     x = np.array(im1.histogram())
    #
    #     for file in glob.glob(dataset_images + '*'):
    #         im2 = Image.open(file)
    #         y = np.array(im2.histogram())
    #
    #         try:
    #             if len(x) == len(y):
    #                 error = np.sqrt(((x - y) ** 2).mean())
    #                 error = str(error)[:2]
    #                 actual_error = float(100) - float(error)
    #             diff = ImageChops.difference(im1, im2).getbbox()
    #             if diff:
    #                 result_data.append(actual_error)
    #             else:
    #                 result_data.append(actual_error)
    #         except ValueError as identifier:
    #             result_data.append(actual_error)

    def compare_image(image, dataset_images, result_data):
        im1 = Image.open(image)
        x = np.array(im1.histogram())
        w, h = im1.size

        for file in glob.glob(dataset_images + '*'):
            im2 = Image.open(file)
            y = np.array(im2.histogram())

            try:
                if len(x) == len(y):
                    error = np.sqrt(((x - y) ** 2).mean())
                    error = str(error)[:2]
                    actual_error = float(100) - float(error)
                im2 = im2.resize((w, h))
                diff = ImageChops.difference(im1, im2).getbbox()
                if diff:
                    result_data.append(actual_error)
                else:
                    result_data.append(actual_error)
            except ValueError as identifier:
                result_data.append(actual_error)

    def check(result_data_1,result_data_2):
        if (max(result_data_1) >= max(result_data_2)):
            return True
        else:
            return False

