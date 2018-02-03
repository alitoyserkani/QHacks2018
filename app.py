import flask

from get_rep import get_rep
from classify import classify

app = flask.Flask(__name__)


@app.route('/get_user', methods=['POST'])
def get_user():
    image = flask.request.form['image']
    rep = get_rep(image)
    if rep is None:
        return flask.Response(
            'No face found.',
            204)

    rep, bounding_box = rep
    user, confidence = classify(rep, bounding_box)

    if rep is None:
        return flask.Response(
            'No match found.',
            204)

    data = {
        'user': user,
        'confidence': confidence
    }

    return flask.Response(
            data,
            200)
