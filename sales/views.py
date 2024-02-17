from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_salesman_from_id, get_customer_from_id, get_chart
from reports.models import Report
from reports.forms import ReportForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required(login_url='/login')
def home_view(request):
    merged_df = pd.DataFrame()
    df = None
    sales_df = None
    position_df = None
    chart = None
    no_data = None
    hello = 'hello world from the view'
    search_form =  SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_by = request.POST.get('result_by')
        # print (f'{date_from} {date_to} {chart_type}')

        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs)>0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id']=sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['saleman_id'] = sales_df['saleman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'saleman_id':'saleman', 'customer_id': 'customer', 'id':'sale_id'}, axis=1, inplace=True)
            positions_data = []
            for sale in sale_qs:
                for pos in sale.positions.all():
                    obj = {
                        'position_id': pos.id,
                        'product_name': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sale_id':sale.id,
                        'sale_id2':pos.get_sales_id(),

                    }
                    positions_data.append(obj)
            position_df =  pd.DataFrame(positions_data)

            # merged_df = pd.merge(sales_df,  position_df).sort_values(['sale_id','position_id'])
            merged_df = pd.merge(sales_df,  position_df, on='sale_id')
            
            df =  merged_df.groupby('transaction_id', as_index = False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, result_by)
            # print(position_df)

            sales_df = sales_df.to_html()
            position_df = position_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
            
            # print(sales_df)
        else:
            no_data = "No data found!"
            print("no data")
        
    

    context ={
        'h' :  hello,
        'search_form':search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'position_df':position_df,
        'merged_df':merged_df,
        'df':df,
        'chart':chart,
        'no_data':no_data
    }
    return render(request, 'sales/home.html', context)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name =  "sales/main.html"  # <app>/<model>_<viewtype
    # context_object_name= 'lists'


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name =  "sales/detail.html"
    context_object_name = 'sale'
