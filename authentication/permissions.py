from django.shortcuts import redirect
from .models import UserProfile


def user_type_required(user_type):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login_user')

            try:
                user_profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                return redirect('login_user')

            if user_profile.user_type != user_type:
                return redirect('access_denied')

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
