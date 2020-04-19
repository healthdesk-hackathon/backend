from rest_framework import request


class BaseSaveSerializer():

    def save(self, **kwargs):
        super().save(current_user=request.user, **kwargs)


class ImmutableSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'is_removed'
    ]

    read_only_fields = ['creator', 'created', ]


class CurrentSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'modifier',
        'modified'
    ]

    read_only_fields = ['creator', 'created', 'modifier', 'modified', ]
