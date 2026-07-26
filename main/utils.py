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

def validate_matric_number(matric_number : str):
    import re
    to_lower = matric_number.lower()
    pattern = r'^[a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+_\d{2}+_\d+$'
    is_matched = bool(re.match(pattern,to_lower))
    if is_matched and to_lower.startswith("lascoco"):
        return True
    
    