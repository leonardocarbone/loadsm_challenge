from flask import Flask
from v1 import webapi

app = Flask(__name__)
webapi.init_app(app)

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=8080)