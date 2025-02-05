# Create your views here.
# analysis/views.py

import os
import chardet  
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DatasetForm
from .models import Dataset
from .nlp_model import preprocess_pdf, extract_budget_allocations
import matplotlib.pyplot as plt
from .sentimentanalysis import analyze_sentiments
import fitz  # PyMuPDF
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from nltk.util import ngrams
from textblob import TextBlob


# Ensure NLTK resources are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def home(request):
    return render(request, 'analysis/home.html')

def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_datasets')
    else:
        form = DatasetForm()
    return render(request, 'analysis/upload_dataset.html', {'form': form})

def view_datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'analysis/view_datasets.html', {'datasets': datasets})

def view_analysis(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    file_path = dataset.file.path

    # Preprocess the PDF file
    text = preprocess_pdf(file_path)

    # Analyze the text
    allocations = extract_budget_allocations(text)
    
    return render(request, 'analysis/result.html', {'allocations': allocations})

# Sentiment analysis view
def sentiment_analysis(request):
    #datasets = Dataset.objects.all()
    if request.method == "POST":
        dataset_id = request.POST.get('dataset')
        selected_dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset_path = os.path.join(settings.MEDIA_ROOT, selected_dataset.file.name)  # Assuming your Dataset model has a file_name field

        try:
            # Pass the dataset path to the sentiment analysis function
            word_freq_path, word_cloud_path, bigram_freq_path, most_common_words, most_common_bigrams, sentence_sentiments, sentiment, sentiment_dist_path, word_polarity_path, bigram_polarity_path = analyze_sentiments(dataset_path)

            # Create context dictionary to pass to the template
            context = {
                'sentiment': sentiment,
                'sentiment_polarity_dist' : sentiment_dist_path,
                'most_common_words': most_common_words,
                'most_common_bigrams': most_common_bigrams,
                'word_freq_image': word_freq_path,
                'bigram_freq_image': bigram_freq_path,
                'word_polarities' : word_polarity_path,
                'word_cloud' : word_cloud_path,
                'bigram_polarities' : bigram_polarity_path,
            }

            # Render the results on the page
            return render(request, 'analysis/sentiment_analysis_result.html', context)
        except Exception as e:
            # Print the exception for debugging
            print(e)

            # Render an error page
            return render(request, 'error.html', {'error': str(e)})

    # If not POST, display the dataset selection page
    datasets = Dataset.objects.all()  # Assuming you have a Dataset model listing available datasets
    # Render the sentiment analysis form
    return render(request, 'analysis/sentiment_analysis.html', {'datasets': datasets})
    

def reports_dashboard(request):
    return render(request, 'analysis/reports_dashboard.html')
