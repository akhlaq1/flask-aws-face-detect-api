import csv
import  boto3

from modules import draw_func

access_id = 'AKIAXBICNCQYRD3P5GWK'
secret_key = '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'

img_path = './2.jpeg'

client = boto3.client('rekognition',
                    aws_access_key_id=access_id,
                    aws_secret_access_key=secret_key, region_name='us-east-2')


def convert_image(img_path,img_output_path):
    with open(img_path,'rb') as source_image:
        source_bytes = source_image.read()



    response = client.detect_faces(
        Image={
            'Bytes': source_bytes
        },

    )

    draw_func.draw_boxes(response,img_path,img_output_path)

