import hashlib
from django.core.cache import cache
from django.shortcuts import render,redirect


def compute_ip_hash(ip_address):                                                                                     
    ip_hash = hashlib.sha224(ip_address.encode("utf-8")).hexdigest()  
    return ip_hash

def validate_device(func):
    def inner_func(request):
        user = request.user
        retrieve_hash = cache.get(request.user)
        if retrieve_hash is None:
            computed_hash = compute_ip_hash(request.META["REMOTE_ADDR"])
            cache.set(user,computed_hash)
        else:
            computed_hash = compute_ip_hash(request.META["REMOTE_ADDR"])
            retrieve_hash = cache.get(request.user)
            if computed_hash == retrieve_hash:
                return func(request)
            else:
                return redirect("")

        return func
    return inner_func
