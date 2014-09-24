# -*- coding:utf-8 -*-
import random
import random_words


class BaseBuilder(object):
    model = None
    lorem = random_words.LoremIpsum()

    class __metaclass__(type):
        @property
        def tally(cls):
            if not hasattr(cls, '_tally'):
                setattr(cls, '_tally', 0)
            cls._tally += 1
            return cls._tally

    @property
    def tally(self):
        return self.__class__.tally

    @property
    def build_kwargs(self):
        raise NotImplementedError(u'build_kwargs() should be implemented')

    @property
    def random_bool(self):
        return bool(random.randint(0, 1))

    def get_random_choice(self, enumeration):
        return random.choice(enumeration)[0]

    def build(self):
        return self.model.objects.create(**self.build_kwargs)
