# from sklearn.mixture import GMM
from get_rep import get_rep
import numpy as np
# import openface
import pickle


def classify(img, args):
    with open('generated-embeddings/classifier.pkl', 'r') as f:
        (le, clf) = pickle.load(f)

    rep, bounding_box = get_rep(img)

    try:
        rep = rep.reshape(1, -1)
    except:
        print("No face detected")
        return None

    predictions = clf.predict_proba(rep).ravel()
    maxI = np.argmax(predictions)
    person = le.inverse_transform(maxI)
    confidence = predictions[maxI]

    # if isinstance(clf,GMM):
    #     dist = np.linalg.norm(rep - clf.means_[maxI])

    return (person, confidence)
