from get_rep import get_rep
import numpy as np
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
    max_index = np.argmax(predictions)
    person = le.inverse_transform(max_index)
    confidence = predictions[max_index]

    return (person, confidence)
