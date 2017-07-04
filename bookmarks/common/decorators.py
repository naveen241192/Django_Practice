from django.http import HttpResponseBadRequest

"""
ajax_required is the custom decorator, returns httpresponsebadrequest if the request is not ajax
else returns decorated function.
"""
def ajax_required(f):
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap