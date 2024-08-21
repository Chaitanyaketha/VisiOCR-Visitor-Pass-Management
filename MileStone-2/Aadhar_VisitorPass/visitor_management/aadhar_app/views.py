from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Aadhar
from .utils.aadhar_ocr import Aadhar_OCR

def upload_aadhar(request):
    if request.method == 'POST' and request.FILES['aadhar_image']:
        aadhar_image = request.FILES['aadhar_image']
        fs = FileSystemStorage()
        filename = fs.save(aadhar_image.name, aadhar_image)
        uploaded_file_url = fs.url(filename)
        
        # Extract data from the image
        aadhar_ocr = Aadhar_OCR(fs.path(filename))
        aadhar_data = aadhar_ocr.extract_data()
        
        if all(aadhar_data):
            aadhar_record = Aadhar(
                aadhar_no=aadhar_data[0],
                name=aadhar_data[3],
                gender=aadhar_data[1],
                dob=aadhar_data[2]
            )
            aadhar_record.save()
            return redirect('visitor_pass', aadhar_id=aadhar_record.id)
        else:
            return render(request, 'aadhar_app/upload.html', {'error': 'Failed to extract Aadhar data'})
    
    return render(request, 'aadhar_app/upload.html')

def create_visitor_pass(request, aadhar_id):
    aadhar_info = Aadhar.objects.get(id=aadhar_id)
    context = {
        'aadhar_no': aadhar_info.aadhar_no,
        'name': aadhar_info.name,
        'gender': aadhar_info.gender,
        'dob': aadhar_info.dob,
    }
    return render(request, 'aadhar_app/visitor_pass.html', context)
