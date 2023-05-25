# Lung Cancer Detection Web App

This is a web application built with Django and Python that utilizes a Mobile Net model based of a pre-trained InceptionV3 model to predict whether a chest CT scan is normal or shows signs of a particular type of lung cancer. The model was built by Arjit Gupta, whose Kaggle profile can be found [here](https://www.kaggle.com/arjitgupta00).

# Dataset

The dataset used for training the model is the Chest CT scan dataset by Mohammed Hanney, which can be found [here](https://www.kaggle.com/datasets/mohamedhanyyy/chest-ctscan-images). Images are not in dcm format, the images are in jpg or png to fit the model
Data contain 3 chest cancer types which are Adenocarcinoma, Large cell carcinoma, Squamous cell carcinoma , and 1 folder for the normal cell
Data folder is the main folder that contain all the step folders
inside Data folder are test , train , valid

test represent testing set
train represent training set
valid represent validation set.

# Usage

To run the application, you will need to have Python 3 installed on your system. You can install all the necessary dependencies by running the following command in your terminal:

```python
pip install -r requirements.txt
```

After installing the dependencies, you can start the development server by running the following command:

```python
python manage.py runserver
```

You can also use the `run.bat` file by double clicking it. Please make sure you have all the dependencies installed.

This will start the server at http://localhost:8000/home_async. You can access the application by visiting this URL in your web browser.

To make a prediction, upload a chest CT scan in JPEG or PNG format by clicking the "Choose File" button, then click the "Detect" button. The application will use the  model to predict whether the scan is normal or shows signs of adenocarcinoma, large cell carcinoma, or squamous cell carcinoma.

# License

This project is licensed under the MIT License. Please see the [LICENSE](LICENSE.txt) file for more details.
