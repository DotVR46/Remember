from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic

from news.models import Article
from users.forms import UserRegistrationForm
from django.contrib.auth.models import User


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


class ProfileView(generic.DetailView):
    model = User
    template_name = "pages/profile.html"
    context_object_name = "profile"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем профиль пользователя
        user = self.get_object()
        # Получаем все статьи, написанные этим пользователем
        user_articles = Article.objects.filter(author=user).order_by("-created_at")
        # Настраиваем пагинацию
        paginator = Paginator(user_articles, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # Добавляем данные пагинации в контекст
        context["page_obj"] = page_obj
        context["articles"] = page_obj.object_list
        context["user"] = user

        return context
