# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response

import dns.message, dns.query, urllib2, json, random

def home(request):
    template_vars = {'request': request}

    if 'domain' in request.GET and 'server' in request.GET:
        domain = request.GET['domain']
        server = request.GET['server']

        query = dns.message.make_query(domain, dns.rdatatype.ANY, dns.rdataclass.IN)

        # Disable 'Recursion Desired' flag
        query.flags ^= dns.flags.RD

        try:
            response = dns.query.udp(query, server)

            def to_plain(rrsets):
                plain = []
                for rrset in rrsets:
                    for rr in rrset:
                        plain.append({
                            'name': str(rrset.name),
                            'ttl': rrset.ttl,
                            'class': dns.rdataclass.to_text(rr.rdclass),
                            'type': dns.rdatatype.to_text(rr.rdtype),
                            'data': str(rr.to_text())
                        })
                return plain

            template_vars['answer'] = to_plain(response.answer)
            template_vars['authority'] = to_plain(response.authority)
            template_vars['additional'] = to_plain(response.additional)
            template_vars['queried'] = True
        except Exception as error:

            template_vars['error'] = error


    return render_to_response('home.html', template_vars)

def weather(request):
    response = HttpResponse(content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"

    if "location" not in request.GET:
        response.content = "Missing location parameter"
        return response

    response.content = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+request.GET["location"]).read()
    return response

def quote(request):
    response = HttpResponse(content_type='text/plain')
    response["Access-Control-Allow-Origin"] = "*"

    quotes = [
"Ik was maar een voorstelling",
"De vroege vogel vangt de meeste vogels. Ofzo.",
"Waar je ook bent, je bent ergens",
"Alle wegen naar Rome beginnen met een kleine of grotere stap",
"Eenmaal meten, tweemaal zagen",
"Doodshoofdaapjes zijn slechte toehoorders",
"Eén stap voorwaarts, twee terug: de cha cha cha des levens",
"Het spel des levens kent geen winnaars",
"Geld is leuker als het rolt dan wanneer het gestapeld voor je ligt, kijk eens bij ons cursusaanbod",
"Als het pad vóór je duister lijkt, bedenk dan: achter je is het waarschijnlijk beter verlicht",
"Beter tien vogels in de lucht dan één in de hand: dat schept mogelijkheden en houdt je scherp",
"De morgenstond kan maar beter koffie in de mond hebben, anders ben ik niet te genieten",
"Soms wordt het beter voor het slechter wordt",
"Douchen is voor vieze mensen",
"Zoek problemen ook eens bij een ander",
"Leef groen, hark je vijver",
]
    response.content = random.choice(quotes)

    return response
