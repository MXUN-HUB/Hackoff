from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///databse.db'

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)