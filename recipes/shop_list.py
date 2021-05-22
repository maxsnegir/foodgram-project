from django.conf import settings


class ShopListSession:

    def __init__(self, request):
        self.session = request.session
        sl = self.session.get(settings.SHOP_LIST_SESSION_ID)
        if not sl:
            sl = self.session[settings.SHOP_LIST_SESSION_ID] = {}
        self.sl = sl

    def add(self, recipe_id):
        if recipe_id not in self.sl:
            self.sl[recipe_id] = int(recipe_id)
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, recipe_id):
        if recipe_id in self.sl:
            del self.sl[recipe_id]
            self.save()
