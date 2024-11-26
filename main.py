# coding=utf-8

import os
from bottle import Bottle

# Create Bottle app
app = Bottle()

# INDEX
@app.get('/')
def index():
	return "Hello"

# Run app
if os.environ.get('APP_LOCATION') == 'heroku':
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)