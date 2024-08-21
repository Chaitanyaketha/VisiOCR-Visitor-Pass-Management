
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Aadhar
from .utils.aadhar_ocr import Aadhar_OCR
import qrcode
from io import BytesIO
import base64
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, timedelta

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
            return render(request, 'aadhar_app/upload.html', {'error': 'Invalid File : Please Ensure that you are uploading proper file'})

    return render(request, 'aadhar_app/upload.html')

def create_visitor_pass(request, aadhar_id):
    aadhar_info = Aadhar.objects.get(id=aadhar_id)

    # Generate expiration time
    expiration_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(f"Aadhar No: {aadhar_info.aadhar_no}\nName: {aadhar_info.name}\nGender: {aadhar_info.gender}\nDOB: {aadhar_info.dob}\nExpires: {expiration_time}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'aadhar_no': aadhar_info.aadhar_no,
        'name': aadhar_info.name,
        'gender': aadhar_info.gender,
        'dob': aadhar_info.dob,
        'qr_image': img_base64,
        'expiration_time': expiration_time,
    }

    if 'download' in request.GET:
        template = get_template('aadhar_app/visitor_pass_pdf.html')
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
        if not pdf.err:
            # Generate dynamic filename
            filename = f"Visitor_Pass_{aadhar_info.name.replace(' ', '_')}.pdf"
            return HttpResponse(response.getvalue(), content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
        else:
            return HttpResponse('Error generating PDF')

    return render(request, 'aadhar_app/visitor_pass.html', context)
