from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response

import dns.message, dns.query
from pprint import pprint

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
