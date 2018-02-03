import flask

# from get_rep import get_rep
from classify import classify

app = flask.Flask(__name__)


@app.route('/get_user', methods=['POST'])
def get_user():
    image = flask.request.files['image']
    import pdb; pdb.set_trace
    user, confidence = classify(image)

    if user is None:
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
