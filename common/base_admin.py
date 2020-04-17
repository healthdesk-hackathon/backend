class SaveCurrentUser():

    def save_model(self, request, obj, form, change):
        obj.current_user = request.user
        super().save_model(request, obj, form, change)
