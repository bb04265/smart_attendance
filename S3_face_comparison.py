import boto3


def face_comparision():
  


    client = boto3.client('rekognition','ap-northeast-2')
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'kpuface',               
                'Name': 'Target.jpg'
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': 'kpuface',
                'Name': 'Target2.JPG'
            }
        },SimilarityThreshold=0

    )
    return (response['FaceMatches'])


face_comparision()
for record in face_comparision():
    face = record
    confidence = face['Face']

    print("유사도는  {}""%"" 이만큼".format(face['Similarity']))
    print("신뢰도는  {}""%"" 이만큼".format(confidence['Confidence']))

    c = float(format(face['Similarity']))


    if(c > 95):{
            print("같은사람")
        }
    else:
        print("다른사람")
