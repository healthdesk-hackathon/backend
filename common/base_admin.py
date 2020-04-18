class SaveCurrentUser():

    def save_model(self, request, obj, form, change):
        obj.current_user = request.user
        super().save_model(request, obj, form, change)


class SaveCurrentUserAdmin():

    def save_model(self, request, obj, form, change):
        obj.current_user = request.user
        super().save_model(request, obj, form, change)

    readonly_fields = [
        'creator',
        'created',
        'modifier',
        'modified'
    ]
