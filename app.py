from flask import Flask
import os
app = Flask(__name__)

"""template_dir =  os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(template_dir, '/templates')
# hard coded absolute path for testing purposes
#working = "C:/ETmaids/templates"
#print(working == template_dir)
templates = template_dir"""
#app = Flask(__name__)

ImageDir = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(ImageDir, 'static/uploads')
if not os.path.isdir(target):
    os.mkdir(target)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])
app.secret_key = "loginto"
app.config['UPLOAD_FOLDER'] = target
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'loginto'
app.config['MYSQL_DB'] = 'etmaids'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



