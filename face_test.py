import boto3
SB = boto3.resource('s3').Bucket('kpuface')
StudentNum = 0
StudentList = []
PictureList = []
client = boto3.client('rekognition', 'ap-northeast-2')
for object in SB.objects.filter(Prefix = 'SourceImage/' ):
    StudentNum += 1
    StudentList.append(object.key)
    
StudentList.pop(0)
StudentNum -=1

for object in SB.objects.filter(Prefix = 'TargetImage/'):

    for i in range(9):
        if 'TargetImage/' + 'target3' + '.JPG' == str(object.key):
            PictureList.append(object.key)
Attendance = [[0 for col in range(4)] for row in range(StudentNum)]

for i in range(StudentNum):
    for j in range(9):
        response = client.compare_faces(
        SimilarityThreshold = 50,
        SourceImage = {'S3Object' : { 'Bucket' : 'kpuface', 'Name' : StudentList[i]} },
        TargetImage = {'S3Object' : { 'Bucket' : 'kpuface', 'Name' : 'TargetImage/target3.JPG'} },)

        if not(len(response["FaceMatches"])== 0):
            simly = response["FaceMatches"][0]["Similarity"]
            confidence = response["FaceMatches"][0]["Face"]["Confidence"]
            Attendance[i][0] = StudentList[i].split('/')[1].split('.')[0]
            Attendance[i][1] = simly
            Attendance[i][2] = confidence
            break
        else:
            Attendance[i][0] = StudentList[i].split('/')[1].split('.')[0]


for i in range(StudentNum):
    print("%d : %s" %(i+1, Attendance[i][0]))
    print("유사도 점수 : %.2f" %(Attendance[i][1]))
    print("인물 신뢰도 : %.2f" %(Attendance[i][2]))



