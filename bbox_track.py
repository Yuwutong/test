# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:11:27 2020

@author: mastaffs
"""

from __future__ import print_function
import sys
import cv2
from random import randint
import os
from PIL import Image
from skimage.measure import label, regionprops
from numpy import asarray
import time

src_folder = 'D:/data/291-350_C802'
save_folder = src_folder
fileid = '10375722802'

img = Image.open(os.path.join(src_folder,fileid+'(G)-R1-Darkfield-01.png'))
mask  =Image.open(os.path.join(src_folder,fileid+'_mask.png')).convert('L')
img = asarray(img)
mask = asarray(mask)

lbl = label(mask)
props = regionprops(lbl)
img_1 = img.copy()
bboxes = []
colors = [] 
for prop in props:
    print('Found bbox', prop.bbox)
    bboxes.append((prop.bbox[1], prop.bbox[0],(prop.bbox[3]-prop.bbox[1]),(prop.bbox[2]-prop.bbox[0])))
    cv2.rectangle(img_1, (prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]), (255, 0, 0), 2)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
img_1 = Image.fromarray(img_1)
img_1.save(os.path.join(save_folder,fileid+'_bbox.png'))

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)

  return tracker


# videoPath = './10377900422/10377900422.mp4'
cap = cv2.VideoCapture(os.path.join(src_folder,fileid+'_test.mp4'))


success, frame = cap.read()
if not success:
  print('Failed to read video')
  sys.exit(1)

'''
## draw bounding box
while True:
    bbox = cv2.selectROI('MultiTracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")
    k = cv2.waitKey(0) & 0xFF
    if (k == 113):  # q is pressed
      break
print('Selected bounding boxes {}'.format(bboxes))
'''
trackerType = "CSRT"    
multiTracker = cv2.MultiTracker_create() 
for bbox in bboxes:
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)


frame_width=1440
frame_height=1440
save_videoname = os.path.join(save_folder,fileid+'_'+time.strftime('%m%d')+'.avi')
track = cv2.VideoWriter(save_videoname,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

savetxt_folder = os.path.join(save_folder,'txt_'+str(fileid)+'_'+time.strftime('%m%d'))
os.makedirs(save_folder, exist_ok=True)
os.makedirs(savetxt_folder, exist_ok=True)

# Process video and track objects
while cap.isOpened():
  success, frame = cap.read()
  if not success:
    break

  success, boxes = multiTracker.update(frame)

  # draw tracked objects
  for i, newbox in enumerate(boxes):
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    center = (int(newbox[0] + newbox[2]/2), int(newbox[1] + newbox[3]/2))
    filename = open(os.path.join(savetxt_folder,str(i)+'.txt'),'a+')
    filename.write(str(center[0])+' '+str(center[1]))
    filename.write('\n')
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    # cv2.putText(frame,'center:{}'.format(center),center,cv2.FONT_HERSHEY_COMPLEX, 0.5, colors[i])


  # show frame
  cv2.imshow('MultiTracker', frame)
  track.write(frame)

  # quit on ESC button
  if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
    break
cap.release()
track.release()
filename.close()

k = cv2.waitKey(0)
if k == 27:
    cv2.destoryAllWindows