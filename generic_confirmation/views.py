from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import ConfirmationForm

def confirm(request, token, template_name='confirm.html', success_template_name='confirmed.html',
                    success_url=None, success_message=None, form_class=ConfirmationForm):
    '''
    If ``success_url`` is not None a redirect to ``success_url`` will
    be issued, once the entered confirmation code was confirmed successfully.
    Optionally, of ``success_message`` is not None, it will be set via
    Django's message system.

    If ``success_url`` is None the template ``success_template_name`` will
    be rendered once the confirmation is complete. The ``success_message``
    will then be added to the template context instead of the message_set.
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
        return render_to_response(template_name, context=RequestContext(request, {'form': form}))

    if form.is_valid():
        instance = form.save()
        if success_url is None:
            return render_to_response(success_template_name, context=RequestContext(request, {
                'success_message': success_message,
                'instance': instance,
            }))
        else:
            if success_message is not None and request.user.is_authenticated():
                request.user.message_set.create(message=success_message)
            return HttpResponseRedirect(success_url)
    else:
        return render_to_response(template_name, context=RequestContext(request, {'form': form}))
