
class BaseSaveSerializer():

    def save(self, **kwargs):
        """Pass the current user from the `context` into the serializer `save`
        so that the instance save will contain it.

        If you use `serializer =` rather than `serializer_class =` then you need to
        add the request context explicitly.
        """
        super().save(current_user=self.context['request'].user, **kwargs)


class ImmutableSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'is_removed'
    ]

    read_only_fields = ['creator', 'created', 'is_removed', ]


class CurrentSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'modifier',
        'modified'
    ]

    read_only_fields = ['creator', 'created', 'modifier', 'modified', ]
