import pickle
import os
from features import extract_features
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

websites = []  # List to hold the websites
while True:
    website = input('Enter a website:')
    websites.append(website)
    all_features = [extract_features(url) for url in websites]  # Extract features of URLs
    url_df = pd.DataFrame(all_features)  # DataFrame for features
    option = input('Do you want to enter another website? (y/n)\n')
    if option in ['n', 'NO', 'no', 'No']:
        break

path = 'C:/Users/user/PycharmProjects/phishing_websites'
all_files = os.listdir(path)  # Directory to access all files in the project
models = [model for model in all_files if model.endswith('.h5')]  # Models are files that end with .h5

for model in models:
    model_path = os.path.join(path, model)  # Join the main directory to each model's path
    with open(model_path, 'rb') as file:
        classifier = pickle.load(file)  # Load models

    predictions = classifier.predict(url_df)
    model_names = " ".join(model.split("_")).replace('.h5','').capitalize()

    print(f'\nPredictions using {model_names}:')
    for url, prediction in zip(websites, predictions):
        if prediction == 'good':
            print(f'{url}: Benign URL')
        else:
            print(f'{url}: Phishing URL')
