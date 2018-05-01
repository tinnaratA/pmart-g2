from django import views


class BaseView(views.View):

    def check_permissions(self, request):
        return eval(" and ".join([str(t(request)) for t in self.permissions]))
