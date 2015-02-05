from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response

import dns.message, dns.query

def home(request):
    if 'domain' in request.GET and 'server' in request.GET:
        domain = request.GET['domain']
        server = request.GET['server']

        query = dns.message.make_query(domain, dns.rdatatype.SOA, dns.rdataclass.IN)

        # Disable 'Recursion Desired' flag
        query.flags ^= dns.flags.RD

        answers = dns.query.udp(query, server)


    return render_to_response('templates/home.html')
