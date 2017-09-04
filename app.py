from flask import Flask
from api.v1 import webapi

app = Flask(__name__)
webapi.init_app(app)

app.run(debug=False, host='0.0.0.0', port=8080)
