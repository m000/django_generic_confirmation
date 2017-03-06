from django.dispatch import Signal

# sender is the class which is edited, instance is the DeferredAction instance
# user is the user who edited the sender instance or None. user is only not
# None if passed to form form.save(user=request.user) method ... 
confirmation_required = Signal(providing_args=["instance", "user"])

confirmation_occured = Signal(providing_args=["instance",])
