# import numpy as np
import cv2
import openface
import os

file_dir = os.path.dirname(os.path.realpath(__file__))
model_dir = os.path.join(file_dir, '/root/openface/', 'models')
dlib_model_dir = os.path.join(model_dir, 'dlib')
openface_model_dir = os.path.join(model_dir, 'openface')

img_dim = 96
face_predictor = 'shape_predictor_68_face_landmarks.dat'
neural_net = 'nn4.small2.v1.t7'

align = openface.AlignDlib(os.path.join(dlib_model_dir, face_predictor))
net = openface.TorchNeuralNet(
    os.path.join(openface_model_dir, neural_net), img_dim, False)


def get_rep(input):
    img = cv2.imread(input)

    if img is None:
        return None

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bounding_box = align.getLargestFaceBoundingBox(rgb_img)

    if bounding_box is None:
        return None

    aligned_img = align.align(
        img_dim, rgb_img, bounding_box,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

    if aligned_img is None:
        return None

    rep = net.forward(aligned_img)
    return (rep, bounding_box)
