import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import matplotlib.pyplot as plt
import io
import base64

def handle_uploaded_file(f):
    # Read the file into a Pandas DataFrame
    data = pd.read_csv(f)
    # Perform some data analysis
    summary = data.describe()
    return summary, data

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary, data = handle_uploaded_file(request.FILES['file'])
            # Convert summary to HTML
            summary_html = summary.to_html()

            # Generate a plot
            plt.figure(figsize=(10,6))
            data.plot(kind='line')
            plt.title('Data Plot')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = 'data:image/png;base64,' + string.decode('utf-8')

            return render(request, 'dataapp/results.html', {'summary': summary_html, 'plot': uri})
    else:
        form = UploadFileForm()
    return render(request, 'dataapp/upload.html', {'form': form})
