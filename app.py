import flask
import os

from classify import classify

app = flask.Flask(__name__)


@app.route('/verify', methods=['POST'])
def verify():
    image = flask.request.files['image']
    image.save(os.path.join('/root/haven/', 'image.jpg'))
    user, confidence = classify(os.path.join('/root/haven/', 'image.jpg'))

    if user is None:
        return flask.Response(
            'No match found.',
            204)

    data = {
        'user': user if confidence > 0.92 else 'unknown',
        'confidence': confidence if confidence > 0.92 else 1
    }

    return flask.jsonify(data)
