# coding=utf-8

from bottle import Bottle

# Create Bottle app
app = Bottle()

# INDEX
@app.get('/')
def index():
	return "Hello"