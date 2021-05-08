from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class IsAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect(self.get_object().get_absolute_url())
        return super().dispatch(request, *args, **kwargs)
