from django.shortcuts import render, get_object_or_404

from . import models


def all_vacancies(request):
    vacancies_list = models.Product.objects.all()
    return render(request,
                  'vacancies/all_vacancies.html',
                  {'vacancies': vacancies_list})

def vacancy_detail(request, id):
    vacancy = get_object_or_404(models.Product,
                                id=id,
                                )
    return render(request,
                  'vacancies/detail.html',
                  {'vacancy': vacancy})
