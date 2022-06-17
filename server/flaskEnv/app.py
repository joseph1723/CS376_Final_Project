from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello World / Heroku'

@app.route('/model')
@cross_origin(origin='*')
def detection():
    data = request.args.get('data')

    if(data == ''):
        return 'hi'

    else:
         return 'Hello World'

if __name__ == '__main__' :
    app.run(debug=True, port=5000)







