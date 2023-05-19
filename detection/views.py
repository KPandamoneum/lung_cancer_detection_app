import numpy as np
from django.shortcuts import render
from keras.models import load_model
from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import io
import asyncio
import aiohttp
from .forms import ImageUploadForm
import imghdr


model = load_model("mobnet_model_best.hdf5")

def process_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image


def predict_image(image_path):
    classes_dir = ["Adenocarcinoma", "Large cell carcinoma", "Normal", "Squamous cell carcinoma"]
    
    img = Image.open(image_path)
    processed_image = process_image(img, target_size=(224, 224))
    preds = model.predict(processed_image) # type: ignore
    pred_index = np.argmax(preds)
    pred_class = classes_dir[pred_index]
    prob = round(np.max(preds) * 100, 2)
    
    return pred_class, prob

async def predict_async_helper(image_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_path) as resp:
            image_content = await resp.content.read()
    image_bytes = io.BytesIO(image_content)
    pred_class, prob = predict_image(image_bytes)
    return pred_class, prob

def home(request):
    return render(request, 'home.html')

async def predict_async(image_path):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, predict_image, image_path)
    return result

async def home_async(request):
    context = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            if not imghdr.what(image_file):
                context['error'] = 'Uploaded file is not a valid image file.'
                return render(request, 'home_async.html', context)
            image_path = io.BytesIO(image_file.read())
            task = predict_async(image_path)
            preds = await task
            context['result'] = preds
    else:
        form = ImageUploadForm()
    context['form'] = form
    return render(request, 'home_async.html', context)
