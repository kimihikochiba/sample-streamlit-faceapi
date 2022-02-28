import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

st.title("顔認識アプリ")

subscription_key = "55bda7be291540cfa7ed20bac453253f"
assert subscription_key
    
face_api_url = "https://20220206kimihiko.cognitiveservices.azure.com/face/v1.0/detect"   

upload_file = st.file_uploader("Choose an image...", type="jpg")
if upload_file is not None:
    img = Image.open(upload_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "returnFaceId": "true",
        "returnFaceAttributes": "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise", 
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()

    textsize = 60
    font = ImageFont.truetype("arial.ttf", size=textsize)
        
    for result in results:
        rect =  result["faceRectangle"]
        gender = result["faceAttributes"]["gender"].capitalize()
        if gender == "Male":
            fontcolor = "blue"
        else:
            fontcolor = "red"
        age = int(result["faceAttributes"]["age"])
        text = gender + "  " + "Age:" + str(age)
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect["left"], rect["top"]), (rect["left"]+rect["width"], rect["top"]+rect["height"])], fill=None, outline="green", width=5)
        draw.text([rect["left"], rect["top"]-textsize], text=text, fill=fontcolor, font=font)
    st.image(img, caption="Uploaded Image", use_column_width=True)