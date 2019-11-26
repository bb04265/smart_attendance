from picamera import PiCamera
import time
import json
import boto3
import datetime

camera = PiCamera()

def photo():
    print('try to take picture')
    global camera
    camera.start_preview()

    time.sleep(1)

    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d_%H%M%S')
    file_name = 'image_{}.jpg'.format(nowDatetime)
    print('file_name: {}'.format(file_name))
    name = '/home/pi/project/{}'.format(file_name)
    
    global upload_file_name
    upload_file_name = file_name

    camera.capture(name)

    camera.stop_preview()

    s3 = boto3.client('s3')
    s3.upload_file(name, 'kpuface', file_name)

    s3 = boto3.resource('s3')
    object_acl = s3.ObjectAcl('kpuface',file_name)
    response = object_acl.put(ACL='public-read')
    print('file upload success. filename: {}'.format(file_name))
    time.sleep(2)

photo()
