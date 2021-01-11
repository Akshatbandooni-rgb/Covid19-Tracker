from django.shortcuts import render, HttpResponse
import requests

# Create your views here.


def home(request):
    response = requests.get('https://api.covid19api.com/summary')
    countries = requests.get('https://api.covid19api.com/countries')
    response.close()
    countries.close()
    jsonResponse = response.json()
    jsonCountriesResponse = countries.json()
    globalCovidData = jsonResponse['Global']
    print(jsonCountriesResponse)

    context = {'globaldata': globalCovidData,
               'countries': jsonCountriesResponse}

    return render(request, 'home.html', context)


def dataByCountry(request):
    if request.method == "POST":
        countConfirmed = 0
        countDeath = 0
        countRecovered = 0
        country = request.POST['countries']
        print(country)
        confirmedCases = requests.get(
            'https://api.covid19api.com/dayone/country/'+country+'/status/confirmed/live')
        recoveredCases = requests.get(
            'https://api.covid19api.com/dayone/country/'+country+'/status/recovered/live')
        deadCases = requests.get(
            'https://api.covid19api.com/dayone/country/'+country+'/status/deaths/live')
        confirmedCases.close()
        recoveredCases.close()
        deadCases.close()
        confirmedCasesjson = confirmedCases.json()
        recoveredCasesjson = recoveredCases.json()
        deadCasesjson = deadCases.json()
        for i in confirmedCasesjson:
            countConfirmed = countConfirmed + i["Cases"]
        print("confirmed cases", countConfirmed)

        for i in recoveredCasesjson:
            countRecovered = countRecovered + i["Cases"]
        print("recovered cases", countRecovered)

        for i in deadCasesjson:
            countDeath = countDeath + i["Cases"]
        print("Dead cases", countDeath)
        context = {'confirmed': countConfirmed,
                   'recovered': countRecovered, 'death': countDeath, 'country': country.upper()}

        return render(request, 'countries.html', context)
    return HttpResponse("Error:404 Forbidden")
