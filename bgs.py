import numpy as np
import cv2

class BackGroundSubtractor:
	# We could take one argument, but you could modify it
	# 1) alpha - between 0 and 1: The higher the value, the more quickly
	# your program learns the changes in the background.
	def __init__(self, alpha):
		self.alpha  = alpha
		# self.backGroundModel = firstFrame

	# Takes 3 arguments (frames)
	# TODO - Put all frames into an collection to avoid code repetition
	def getForeground(self, firstFrame, secondFrame, thirdFrame):
		# apply the background averaging formula:
		# NEW_BACKGROUND = CURRENT_FRAME * ALPHA + OLD_BACKGROUND * (1 - APLHA)
		# self.backGroundModel =  frame * self.alpha + self.backGroundModel * (1 - self.alpha)
		
		# aplly the background median formula:
		# NEW_BACKGROUND = medianFrame * ALPHA + PREVIOUS_BACKGROUND * (1 - APLHA)
		finalFrame =  secondFrame * self.alpha + firstFrame * (1 - self.alpha)
		# self.backGroundModel = (frame + self.backGroundModel)

		# We acquire a copy of it in the uint8 dtype
		# and pass that to absdiff.

		# return cv2.absdiff(self.backGroundModel.astype(np.uint8),frame)
		return cv2.absdiff(finalFrame.astype(np.uint8), secondFrame)

cam = cv2.VideoCapture(0)

# Any filter we need to apply to all frames should be put here
def denoise(frame):
    frame = cv2.medianBlur(frame,5)
    frame = cv2.GaussianBlur(frame,(5,5),0)
    
    return frame

def initSubtraction(firstFrame, secondFrame, thirdFrame):
	# init our class instance
	backSubtractor = BackGroundSubtractor(0.01)

	# Read a frame from the camera
	ret,frame = cam.read()

	if ret is True:
		# Show the filtered image
		cv2.imshow('input',denoise(frame))

		# get the foreground
		# foreGround = backSubtractor.getForeground(denoise(frame))
		foreGround = backSubtractor.getForeground(denoise(firstFrame), denoise(secondFrame), denoise(thirdFrame))

		# Apply thresholding on the background and display the resulting mask
		# Note: The result is as RGB image, we could use a grayscale instead
		# Just convert 'foreGround' to a grayscale before apply threshold
		ret, mask = cv2.threshold(foreGround, 15, 255, cv2.THRESH_BINARY)

		cv2.imshow('mask', mask)

while (True):
	ret, firstFrame = cam.read()
	secondFrame = firstFrame
	thirdFrame = secondFrame

	# In this loop we can get each frame individually, to pass
	for i in range(3):
		if i == 0:
			firstRet, firstFrame = cam.read()
		if i == 1:
			secondRet, secondFrame = cam.read()
		if i == 2:
			thiddRet, thirdFrame = cam.read()
		else:
			initSubtraction(firstFrame, secondFrame, thirdFrame)	

	key = cv2.waitKey(10) & 0xFF
	
	if key == 27:
		break

cam.release()
cv2.destroyAllWindows()