import pandas as pd
from dateutil.parser import parse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum, Count
from django.db.models.functions import Lower, TruncMonth
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from tables.forms import UploadFileForm
from tables.models import Campaign, FileUpload
from users.utils import log_to_model


class FileUploadView(LoginRequiredMixin, View):
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
                    log_to_model('WARNING', f"Непідтримуваний формат файлу: {file.name}", self.request.user)
                    return redirect('file_upload')

                required_columns = {'Advertiser', 'Brand', 'Start', 'End', 'Format', 'Platform', 'Impr'}
                if not required_columns.issubset(set(df.columns)):
                    messages.error(request, 'Некоректна структура файлу.')
                    log_to_model('ERROR', f"Некоректна структура файлу: {file.name}", self.request.user)
                    return redirect('file_upload')

                if df[['Start', 'End']].isnull().any().any():
                    messages.error(request, 'Некоректні або відсутні дані в колонках Start та/або End.')
                    log_to_model('ERROR', f"Некоректні дані в колонках Start/End: {file.name}", self.request.user)
                    return redirect('file_upload')

                file_upload = FileUpload.objects.create()

                for _, row in df.iterrows():
                    try:
                        start_date = parse(str(row['Start']), dayfirst=True)
                        end_date = parse(str(row['End']), dayfirst=True)
                        Campaign.objects.create(
                            file_upload=file_upload,
                            advertiser=row['Advertiser'],
                            brand=row['Brand'],
                            start_date=start_date,
                            end_date=end_date,
                            format=row['Format'],
                            platform=row['Platform'],
                            impressions=row['Impr']
                        )
                    except ValueError:
                        messages.error(request, f"Невірний формат дати в рядку: {row.to_dict()}")
                        log_to_model('WARNING', f"Невірний формат дати в рядку: {row.to_dict()}", self.request.user)
                        continue

                messages.success(request, 'Файл успішно завантажено та оброблено.')
                log_to_model('INFO', f"Файл {file.name} успішно оброблено", self.request.user)
                return redirect(reverse('aggregated_results', args=[file_upload.id]))

            except Exception as e:
                messages.error(request, f'Помилка при обробці файлу: {e}')
                log_to_model('ERROR', f"Помилка при обробці файлу {file.name}: {e}", self.request.user)
                return redirect('file_upload')

        return render(request, self.template_name, {'form': form})


class AggregatedResultsView(LoginRequiredMixin, View):
    template_name = 'aggregated_results.html'

    def get(self, request, file_upload_id):
        try:
            file_upload = FileUpload.objects.get(id=file_upload_id)
        except FileUpload.DoesNotExist:
            messages.error(request, 'Завантаження не знайдено.')
            log_to_model('ERROR', f"Завантаження з ID {file_upload_id} не знайдено.", self.request.user)
            return redirect('file_upload')

        campaigns = Campaign.objects.filter(file_upload=file_upload)
        if campaigns.exists():
            log_to_model('INFO', f"Агрегування даних для файлу з ID {file_upload_id}", self.request.user)

            monthly_data = (
                campaigns
                .annotate(month=TruncMonth('start_date'))
                .values('month')
                .annotate(
                    total_impressions=Sum('impressions'),
                    avg_impressions_brand=Sum('impressions') / Count('brand', distinct=True),
                    avg_impressions_platform=Sum('impressions') / Count('platform', distinct=True),
                    avg_impressions_format=Sum('impressions') / Count('format', distinct=True)
                )
                .order_by('month')
            )

            yearly_totals = campaigns.aggregate(
                total_impressions=Sum('impressions'),
                avg_impressions_brand=Sum('impressions') / Count('brand', distinct=True),
                avg_impressions_platform=Sum('impressions') / Count('platform', distinct=True),
                avg_impressions_format=Sum('impressions') / Count('format', distinct=True)
            )

            platform_distribution = (
                campaigns
                .annotate(platform_lower=Lower('platform'))
                .values('platform_lower')
                .annotate(total_impressions=Sum('impressions'))
                .order_by('-total_impressions')
            )

            top_15_platforms = list(platform_distribution[:15])
            other_platforms = [entry['platform_lower'] for entry in platform_distribution[15:]]
            other_impressions = sum(entry['total_impressions'] for entry in platform_distribution[15:])

            if other_impressions > 0:
                top_15_platforms.append({'platform_lower': 'Інше', 'total_impressions': other_impressions})

            format_distribution = (
                campaigns
                .annotate(format_lower=Lower('format'))
                .values('format_lower')
                .annotate(total_impressions=Sum('impressions'))
                .order_by('-total_impressions')
            )

            monthly_distribution = (
                campaigns
                .annotate(month=F('start_date__month'))
                .values('month')
                .annotate(total_impressions=Sum('impressions'))
                .order_by('month')
            )

            advertiser_distribution = (
                campaigns
                .annotate(advertiser_lower=Lower('advertiser'))
                .values('advertiser_lower')
                .annotate(total_impressions=Sum('impressions'))
                .order_by('-total_impressions')
            )

            top_5_advertisers = list(advertiser_distribution[:5])
            other_total_impressions = sum(entry['total_impressions'] for entry in advertiser_distribution[5:])

            if other_total_impressions > 0:
                top_5_advertisers.append({'advertiser_lower': 'Інше', 'total_impressions': other_total_impressions})

            brand_distribution = (
                campaigns
                .annotate(brand_lower=Lower('brand'))
                .values('brand_lower')
                .annotate(total_impressions=Sum('impressions'))
                .order_by('-total_impressions')
            )

            top_20_brands = list(brand_distribution[:20])
            other_total_impressions = sum(entry['total_impressions'] for entry in brand_distribution[20:])

            if other_total_impressions > 0:
                top_20_brands.append({'brand_lower': 'Інше', 'total_impressions': other_total_impressions})

            log_to_model('INFO', f"Агреговані дані для файлу з ID {file_upload_id} успішно обчислені", self.request.user)
        else:
            monthly_data = []
            yearly_totals = {}
            top_15_platforms = []
            other_platforms = []
            format_distribution = []
            monthly_distribution = []
            top_20_brands = []
            top_5_advertisers = []
            log_to_model('WARNING', f"Немає даних для файлу з ID {file_upload_id}", self.request.user)

        return render(request, self.template_name, {
            'monthly_data': monthly_data,
            'yearly_totals': yearly_totals,
            'top_15_platforms': top_15_platforms,
            'other_platforms': other_platforms,
            'format_distribution': format_distribution,
            'monthly_distribution': monthly_distribution,
            'top_5_advertisers': top_5_advertisers,
            'top_20_brands': top_20_brands,
        })
