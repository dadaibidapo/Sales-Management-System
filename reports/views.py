from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, HttpResponse
from .utils import get_report_image
from .models import Report
from .forms import  ReportForm
from django.views.generic import ListView,  DetailView, TemplateView

from django.conf import settings
# from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from profiles.models import Profile
from sales.models import  Sale,Position,CSV
from products.models import Product
from customers.models import Customer

import csv
from django.utils.dateparse import parse_date

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name='reports/main.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model=Report
    template_name="reports/detail.html"

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required(login_url='/login')
def csv_upload_view(request):
    if request.method == 'POST':
        CSV_file_name = request.FILES.get('file').name
        CSV_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name = CSV_file_name)

        if created:
            obj.CSV_file = CSV_file
            obj.save()
            with open(obj.CSV_file.path, 'r')as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    # print(row, type(row))
                    # data = "".join(row)
                    # print(data, type(data))
                    # data = data.split(';')
                    data = row
                    # print(data, type(data))

                    transaction_id = data[1]
                    product = data[2]
                    quantity = int(data[3])
                    customer = data[4]
                    date = parse_date(data[5])
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except ObjectDoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, saleman=salesman_obj, created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                return JsonResponse({"ex":False})
        else:
            return JsonResponse({"ex": True})            
                    
                    # print(product_obj)


    return HttpResponse()


@login_required(login_url='/login')
def create_report_view(request):
    # if request.is_ajax():
    form = ReportForm(request.POST or None)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # name = request.POST.get('name')
        # remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)
        user=request.user
        if user.is_authenticated:
            # profile, created = Profile.objects.get_or_create(user=user)
            author = Profile.objects.get(user=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author =  author
            instance.save()
        # report = Report(name=name, remarks=remarks, image=img,  author=author)
        # report.save()

        return JsonResponse({'msg': 'send'})
    return JsonResponse({'msg':'error'})

@login_required(login_url='/login')
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    # obj = Report.objects.get(pk=pk)
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if to display it on the web page 
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# class RenderPDFView(View):
#     template_name = 'reports/pdf.html'
#     context = {'hello': 'Hello world i am writing my first pdf application'}

#     def get(self, request, *args, **kwargs):
#         # Create a Django response object, and specify content_type as pdf
#         response = HttpResponse(content_type='application/pdf')

#         # If you want the PDF to be downloaded
#         # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
#         # If you want the PDF to be displayed in the browser
#         response['Content-Disposition'] = 'filename="report.pdf"'

#         # Find the template and render it
#         template = get_template(self.template_name)
#         html = template.render(self.context)

#         # Create a PDF
#         pisa_status = pisa.CreatePDF(html, dest=response)
        
#         # If there was an error, show some message
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>', content_type='text/html')
        
#         return response
