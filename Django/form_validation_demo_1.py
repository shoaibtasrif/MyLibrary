from django import forms, views
from django.shortcuts import render, HttpResponse
from django.urls import path, include


class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)

    def clean_name(self):
        name = self.cleaned_data.get('name', None)

        if name:
            if len(name) < 8:
                raise forms.ValidationError([
                    forms.ValidationError("at least 8 chars"),
                    forms.ValidationError("too short hahahhahahahah"),
                    forms.ValidationError("too short hahahhahahahah"),
                    forms.ValidationError("too short hahahhahahahah"),
                    forms.ValidationError("too short hahahhahahahah")
                ])

        print('myform clean name')
        return name  # always return a value even if not been changed to replace the value n cleaned data

    def clean(self):
        name = self.cleaned_data.get('name', None)
        title = self.cleaned_data.get('title', None)

        if name and title:
            if len(name) < len(title):
                raise forms.ValidationError("name to be gte title")


class MyView(views.View):

    def get(self, request):
        form = MyForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = MyForm(request.POST or None)

        if form.is_valid():
            print(form.as_table())
            return HttpResponse('yes')
        else:
            print(form.as_table())
            return render(request, 'form.html', {'form': form})


urlpatterns = [
    path('', MyView.as_view(), name='fvd1')
]


'''
-> form.html

{% extends 'base.html' %}

{% block content_1 %}
<title>Form</title>
{% endblock %}

{% block content_2 %}

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <table>
        <tr>
            <td></td>
            <td>{{ form.non_field_errors }}</td>
        </tr>
        <tr>
            <td> {{ form.name.label_tag }} </td>
            <td> {{ form.name }} </td>

        </tr>
        <tr>
            <td></td>
            <td>{{ form.name.errors }}</td>
        </tr>
        <tr>
            <td> {{ form.title.label_tag }} </td>
            <td> {{ form.title }} </td>

        </tr>
        <tr>
            <td></td>
            <td>{{ form.title.errors }}</td>
        </tr>

        <tr>
            <td></td>
            <td><input type="submit" value="Enter"></td>
        </tr>
    </table>
</form>
{% endblock %}


'''
