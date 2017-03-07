from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import ConfirmationForm
from .models import DeferredValidationError

def confirm(request, token, template='confirm.html', success_message=None, success_url=None, form_class=ConfirmationForm):
    '''
    If a valid token is provided (either through the url or through POST data),
    the following will happen:
        - If ``success_url`` is not provided, ``template`` will be rendered,
          having ``instance`` and (optionally) ``success_message`` set in
          its context.
          The former can be used to determine if a confirmation took place,
          or the user is returning to the url.
        - If ``success_url`` is provided, a redirection to it will happen
          and (optionally) ``success_message`` will be sent via the django
          messaging framework.

    If a valid token is not provided, then ``template`` will be rendered,
    having only ``form`` in its context.
    '''
    if request.method == 'POST':
        # get token from POST
        form = form_class(request.POST)
    elif token is not None:
        # token has been parsed by urlconf
        form = form_class({'token': token})
    else:
        # no token provided - just render the form
        form = form_class()
        return render_to_response(template, context=RequestContext(request, {'form': form}))

    if form.is_valid():
        try:
            instance = form.save()
        except DeferredValidationError:
            return render_to_response(template, context=RequestContext(request, {
                ### fix this
                'success': False,
                'message': 'le poul',
                'exception': None,
            }))
        if success_url is None:
            return render_to_response(template, context=RequestContext(request, {
                'success': True,
                'message': success_message,
                'instance': instance,
            }))
        else:
            if success_message is not None and request.user.is_authenticated():
                request.user.message_set.create(message=success_message)
            return HttpResponseRedirect(success_url)
    else:
        return render_to_response(template, context=RequestContext(request, {'form': form}))
