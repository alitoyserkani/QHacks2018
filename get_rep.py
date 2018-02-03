import cv2
import openface
import os

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '/root/openface/', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')

imgDim = 96
face_predictor = 'shape_predictor_68_face_landmarks.dat'
neural_net = 'nn4.small2.v1.t7'

align = openface.AlignDlib(os.path.join(dlibModelDir, face_predictor))
net = openface.TorchNeuralNet(neural_net, imgDim, False)


def getRep(input):
    img = cv2.imread(input)

    if img is None:
        return None

    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bb = align.getLargestFaceBoundingBox(rgbImg)

    if bb is None:
        return None

    alignedImg = align.align(
        imgDim, rgbImg, bb,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

    if alignedImg is None:
        return None

    rep = net.forward(alignedImg)
    return (rep, bb)
