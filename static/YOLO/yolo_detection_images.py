import numpy as np
import cv2

def YOLO(inputimage = 'person.jpg', path = ''):
    confidenceThreshold = 0.5
    NMSThreshold = 0.3

    # https://pjreddie.com/media/files/yolov3.weights
    modelWeights = path + 'yolov3.weights'

    modelConfiguration = path + 'yolov3.cfg'
    labelsPath = path + 'coco.names'

    labels = open(labelsPath).read().strip().split('\n')
    np.random.seed(10)

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    image = cv2.imread(inputimage)
    (H, W) = image.shape[:2]

    layerName = net.getLayerNames()
    layerName = [layerName[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB = True, crop = False)
    net.setInput(blob)
    layersOutputs = net.forward(layerName)

    boxes = []
    confidences = []
    classIDs = []
    detector = []
    
    for output in layersOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidenceThreshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY,  width, height) = box.astype('int')
                x = int(centerX - (width/2))
                y = int(centerY - (height/2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
    if(len(detectionNMS) > 0):

        for i in detectionNMS.flatten():
            detected = labels[classIDs[i]]
            detector.append(detected)
    return detector

# print(YOLO())
