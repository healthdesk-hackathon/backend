from custom_auth.utils import get_user_model
import random


class TestUser():

    @property
    def test_user(self):
        if not hasattr(self, '_test_user'):
            self._test_user = get_user_model().objects.create_superuser('test-admin{}'.format(random.random()), '98wiuqnhiu87')
            self._test_user.save()

        return self._test_user
