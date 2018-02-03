import flask
import os

from classify import classify

app = flask.Flask(__name__)


@app.route('/get_user', methods=['POST'])
def get_user():
    image = flask.request.files['image']
    image.save(os.path.join('/root/haven/', 'image.jpg'))
    user, confidence = classify(os.path.join('/root/haven/', 'image.jpg'))

    if user is None:
        return flask.Response(
            'No match found.',
            204)

    data = {
        'user': user,
        'confidence': confidence
    }

    return flask.jsonify(data)
