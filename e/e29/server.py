from flask import Flask, render_template, request, Response
from PIL import Image

from face_tracker import get_nearest_face_10
from image_loader import preprocess

app = Flask(__name__, template_folder="./templates/", static_url_path="/images", static_folder="images")

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/healthz", methods=["GET"])
def healthCheck():
   return "", 200

@app.route("/image", methods = ['POST', 'GET'])
def get_result():
   if request.method == "POST":
      width, height = 72, 72
      try:           
         source = Image.open(request.files['source'])
         source = source.resize((width, height))
         top = get_nearest_face_10(source)
        
      except Exception as e:
         print("error : %s" % e)
         return Response("fail", status=400)
   
   else: pass

   return top

if __name__ == '__main__':
   app.run(host='0.0.0.0', port='80', debug=True)