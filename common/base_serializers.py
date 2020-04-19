class ImmutableSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'is_removed'
    ]


class CurrentSerializerMeta():

    base_fields = [
        'id',
        'creator',
        'created',
        'modifier',
        'modified'
    ]
