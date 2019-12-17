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

PresentList=[]
AbsenceList=[]
for i in range(StudentNum):
    attend = float(Attendance[i][1])
    if (attend > 90) :
        PresentList.append(Attendance[i][0])
    else :
        AbsenceList.append(Attendance[i][0])
print("출석한 사람 : %s" % PresentList)
print("빠진 사람 : %s " % AbsenceList)

