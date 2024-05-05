from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'srt/index.html')


def trainlist(request):
    return render(request, 'srt/srt_train_list.html')