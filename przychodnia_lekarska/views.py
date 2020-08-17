import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View

from przychodnia_lekarska.models import render_to_pdf
from wizyty.models import Wizyty


def index(request):
    return render(request, 'index.html', {})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists() or u.is_superuser, redirect_field_name='#')
def konto(request):
    return render(request, 'konto.html', {})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists(), redirect_field_name='#')
def deactivate(request):
    return render(request, 'deactivate.html', {})


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        queryset = Wizyty.objects.all()
        template = get_template('pdf/pdf_template.html')
        context = {
            "object_list": queryset,
            "data": datetime.date.today()
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/pdf_template.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Przychodnia_raport_{datetime.date.today()}.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
