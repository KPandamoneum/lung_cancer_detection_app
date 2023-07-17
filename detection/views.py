import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from keras.models import load_model
from keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image # type: ignore
from PIL import Image
from .forms import ImageUploadForm
import imghdr


ct_scan_model = load_model("mobnet_n_v_c.h5")
cancer_model = load_model("mobnet_model_best.hdf5")


def process_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image


def predict_ct_scan(image_path):
    classes_dir = ["ctscan", "normal"]
    img = Image.open(image_path)
    processed_image = process_image(img, target_size=(224, 224))
    preds = ct_scan_model.predict(processed_image) # type: ignore
    pred_index = np.argmax(preds)
    pred_class = classes_dir[pred_index]
    prob = round(np.max(preds) * 100, 2)
    return pred_class, prob


def predict_cancer(image_path):
    classes_dir = ["Adenocarcinoma", "Large cell carcinoma", "Normal", "Squamous cell carcinoma"]
    img = Image.open(image_path)
    processed_image = process_image(img, target_size=(224, 224))
    preds = cancer_model.predict(processed_image) # type: ignore
    pred_index = np.argmax(preds)
    pred_class = classes_dir[pred_index]
    prob = round(np.max(preds) * 100, 2)
    return pred_class, prob


def home(request):
    return render(request, 'home.html')


def home_async(request):
    context = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            if not imghdr.what(image_file):
                context['error'] = 'Uploaded file is not a valid image file.'
                return render(request, 'home_async.html', context)
            # Save the image to the media folder
            file_path = default_storage.save('uploads/' + image_file.name, ContentFile(image_file.read()))
            image_url = default_storage.url(file_path)
            
            print("Image URL:", image_url)  # Debugging statement
            
            preds = predict_ct_scan(image_file)
            if preds[0] == "ctscan":
                cancer_pred = predict_cancer(image_file)
                context['result'] = {
                    'is_ct_scan': preds[0],
                    'ct_scan_pred': preds[1],
                    'cancer_pred': cancer_pred[0],
                }
            else:
                context['result'] = {
                    'is_ct_scan': preds[0],
                }
            context['image_path'] = image_url
    else:
        form = ImageUploadForm()
    context['form'] = form
    return render(request, 'home_async.html', context)
