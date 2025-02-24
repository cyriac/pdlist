# -*- encoding: utf-8 -*-
# dplist v0.1.0
# A passive sudomain lister
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
utils functions for pdlist

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""
import re


def remove_unrelated_domains(subdomains, domains):
    """
    This function removes from the entire set hostnames found, the ones who
    do not end with the target provided domain name.
    So if in the list of domains we have example.com and our target/scope
    is example.it, then example.com will be removed because falls out of the
    scope.

    Args:
    domains -- the list of input target domains

    Returns:
    subdomains -- the set of subomains strictly respecting the scope
    """
    subdomains = [s for s in subdomains if s.endswith(tuple(domains))]
    return subdomains

def polish_subdomain_strings(subdomains):
    """
    This function is used to polish subdomain strings which may come out
    from some query service. Indeed some services provide hostnames with
    spaces or starting with dots.
    Hence this function returns a polished list of subdomains which are legal
    and can be queried further.
    Polishing in this context means:
    - removing spaces
    - removing initial or ending dots

    Args:
    subdomains -- the list of subdomains to polish

    Returns:
    subdomains -- the list of polished subdomains
    """
    subdomains = [item.strip() for item in subdomains]
    subdomains = [item.rstrip('.') for item in subdomains]
    subdomains = [re.sub(r'^.* ', '', item) for item in subdomains]
    subdomains = [re.sub(r'^[\.\*]\.', '', item) for item in subdomains]
    return subdomains

def find(key, dictionary):
    """
    This function is used to find the value associated to a key in an
    arbitrarily nested dictionary.

    Args:
    key        -- the key associated to the value we are interested in
    dictionary -- the (arbitrarily nested) dictionary in which to search for the
                  key

    Returns:
    value -- returns the value associated to the key we searched for
    """
    if isinstance(dictionary, dict):
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result

def clean_domain_strings(domains):
    """
    This function is used to normalize input domain passed from the command line
    by the user. Basically we want to be able to handle both domains passed in
    the form example.com but also domains passed erroneously with a scheme, such
    as https://example.com

    Args:
    domains -- the list of input domains

    Returns:
    subdomains -- the list of normalized domains
    """
    domains = [item.rstrip('/') for item in domains]
    domains = [re.sub(r'(http://|https://)', '', item) for item in domains]
    return domains
