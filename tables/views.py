import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from tables.forms import UploadFileForm
from tables.models import Campaign


class FileUploadView(View):
    template_name = 'upload.html'

    def get(self, request):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, 'Непідтримуваний формат файлу.')
                    return redirect('file_upload')

                required_columns = {'Advertiser', 'Brand', 'Start', 'End', 'Format', 'Platform', 'Impr'}
                if not required_columns.issubset(set(df.columns)):
                    messages.error(request, 'Некоректна структура файлу.')
                    return redirect('file_upload')

                for _, row in df.iterrows():
                    Campaign.objects.create(
                        advertiser=row['Advertiser'],
                        brand=row['Brand'],
                        start_date=row['Start'],
                        end_date=row['End'],
                        format=row['Format'],
                        platform=row['Platform'],
                        impressions=row['Impr']
                    )
                messages.success(request, 'Файл успішно завантажено та оброблено.')
                return redirect('file_upload')

            except Exception as e:
                messages.error(request, f'Помилка при обробці файлу: {e}')
                return redirect('file_upload')

        return render(request, self.template_name, {'form': form})


class CampaignListView(View):
    template_name = 'campaign_list.html'

    def get(self, request):
        campaigns = Campaign.objects.all()
        return render(request, self.template_name, {'campaigns': campaigns})
