from django.shortcuts import render
from django.views import generic

from users.forms import UserRegistrationForm


class UserRegister(generic.CreateView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.clean_password2())
            new_user.save()
            return render(
                request, "registration/register_done.html", {"user": new_user}
            )
        return render(request, "registration/register.html", {"form": user_form})
