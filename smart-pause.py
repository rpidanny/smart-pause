import cv
import time
import Image
import os

playFlag = True
pauseFlag = False
playCount=0
pauseCount=0

cv.NamedWindow("Smart-Pause", 1)
cameraSelect=input("""Enter Camera Number (Default Camera is 0):""")
capture = cv.CreateCameraCapture(cameraSelect)

width = None
height = None

faceCascade = cv.Load("face.xml")
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,0.4,0.4,1,1,1)
fontLogo = cv.InitFont(cv.CV_FONT_HERSHEY_TRIPLEX,0.6,0.6,1,1,1)


if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

if height is None:
	height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 


def FaceDetect(image, faceCascade):
	global playFlag,pauseFlag,playCount,pauseCount
	
	min_size = (20,20)
	image_scale = 2
	haar_scale = 1.2
	min_neighbors = 2
	haar_flags = 0

	gray = cv.CreateImage((image.width, image.height), 8, 1)
	smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)
	cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
	cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)
	cv.EqualizeHist(smallImage, smallImage)


	faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
	haar_scale, min_neighbors, haar_flags, min_size)


	if faces:
		playCount=playCount+1
		pauseCount=0
		if(playCount>105):playCount=0
		if(playFlag==False and playCount>3):
			pauseFlag=False
			playFlag=True
			print "Play"
			os.system("xdotool key space")
			playCount=0
		faceCount=0

		for ((x, y, w, h), n) in faces: 
			faceCount=faceCount+1
			pt1 = (int(x * image_scale), int(y * image_scale))
			pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
			textPos= (int(x * image_scale), int(y * image_scale)-20)
			cv.Rectangle(image, pt1, pt2, cv.RGB(255, 155, 15), 3, 8, 0)
			Textdata=str("Face Detected at "+ "("+str(int((x+w)*image_scale/2))+" , "+str(int((y+h)*image_scale/2))+ ")")
			if(faceCount==1):
				cv.PutText(image,Textdata,textPos,font,cv.RGB(255,255,255))
			elif(faceCount==2):
				cv.PutText(image,Textdata,textPos,font,cv.RGB(50,155,255))
			elif(faceCount==3):
				cv.PutText(image,Textdata,textPos,font,cv.RGB(50,125,0))
			elif(faceCount==4):
				cv.PutText(image,Textdata,textPos,font,cv.RGB(0,125,50))
			elif(faceCount==5):
				cv.PutText(image,Textdata,textPos,font,cv.RGB(255,25,5))
			else:
				cv.PutText(image,Textdata,textPos,font,cv.RGB(255,255,255))
				

	else:
		pauseCount=pauseCount+1
		playCount=0
		if(pauseCount>105):pauseCount=0
		if(pauseFlag==False and pauseCount>3):
			pauseFlag=True
			playFlag=False
			print "Pause"
			os.system("xdotool key space")
			pauseCount=0
	cv.PutText(image,"Smart-Pause V1.1", (10,30),fontLogo,cv.RGB(0, 0, 0))
	return image



while True:
	img = cv.QueryFrame(capture)
	cv.Flip(img,img,1)
	image = FaceDetect(img, faceCascade)
	cv.ShowImage("Smart-Pause", image)
	k = cv.WaitKey(50);
	if k in [27, ord('Q'), ord('q')]:
		break
