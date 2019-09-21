from django.db import models
from django.urls import path, include, reverse_lazy
from django import views
from django.views.generic import ListView, CreateView, UpdateView
from django import forms
from django.shortcuts import render

'''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
django.setup()
'''


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'load_cities.html', {'cities': cities})


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        # print('hi')

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(
                    country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by(
                'name')


class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'
    context_object_name = 'people'


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'person_create.html'
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'person_create.html'
    success_url = reverse_lazy('person_changelist')


urlpatterns = [
    path('', PersonListView.as_view(), name='person_changelist'),
    path('add/', PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
]
