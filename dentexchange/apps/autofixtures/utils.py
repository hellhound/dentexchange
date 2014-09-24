# -*- coding:utf-8 -*-
import os
import sys
import random
import decimal
import datetime
import random_words

from libs import constants as libs_constants
from location.models import ZipCode


class RandomPerson(object):
    nicknames = random_words.RandomNicknames()
    words = random_words.RandomWords()
    emails = random_words.RandomEmails()

    def __init__(self, *args, **kwargs):
        self._zip_code_object = None

    def get_name(self, any_gender=False):
        if any_gender:
            return self.nicknames.random_nick(gender='u')
        return self.nicknames.random_nick(gender='m')

    @property
    def first_name(self):
        return self.get_name(any_gender=True)

    @property
    def last_name(self):
        return self.get_name()

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def email(self):
        return self.emails.randomMail()

    @property
    def company_name(self):
        if random.choice([True, False]):
            name = RandomCompanyName()
        else:
            name = '%s%s%s' % (RandomCompanyName(), RandomLigature(),
                RandomCompanyName())
        return '%s%s' % (name, RandomCompanySuffix())

    @property
    def address(self):
        number = random.randint(100, 1000)
        name_selector = random.randint(0, 3)
        name_format = '%s Street'
        if name_selector == 0:
            street = name_format % self.first_name
        elif name_selector == 1:
            street = name_format % self.last_name
        elif name_selector == 2:
            street = name_format % self.full_name
        else:
            bits = [self.first_name, self.last_name,
                self.words.random_words()[0].title()]
            street = ' '.join(bits)
        return '%i %s' % (number, street)

    @property
    def zip_code_object(self):
        if self._zip_code_object is None:
            self._zip_code_object = ZipCode.objects.all().order_by('?')[0]
        return self._zip_code_object

    @property
    def zip_code(self):
        return self.zip_code_object.code

    @property
    def city(self):
        return self.zip_code_object.city

    @property
    def state(self):
        return self.zip_code_object.state

    @property
    def country(self):
        return 'US'


class BaseRandomLine(object):
    db_file = None

    class __metaclass__(type):
        @property
        def db_file_cache(cls):
            if not hasattr(cls, '_db_file_cache'):
                base_dir = os.path.realpath(os.path.dirname(__file__))
                setattr(cls, '_db_file_cache',
                    open(os.path.join(base_dir, cls.db_file)))
            return cls._db_file_cache

        def __call__(cls):
            base_dir = os.path.realpath(os.path.dirname(__file__))
            cls.db_file_cache.seek(0)
            lines = cls.db_file_cache.readlines()
            selection = random.randint(0, len(lines) - 1)
            return lines[selection].strip().replace('\s', ' ')


class RandomCity(BaseRandomLine):
    db_file = 'cities.txt'


class RandomExperienceWord(BaseRandomLine):
    db_file = 'experience-words.txt'


class RandomOpening(BaseRandomLine):
    db_file = 'openings.txt'


class RandomProfession(BaseRandomLine):
    db_file = 'professions.txt'


class RandomSpecialty(BaseRandomLine):
    db_file = 'specialties.txt'


class RandomCompanyName(BaseRandomLine):
    db_file = 'company-names.txt'


class RandomCompanySuffix(BaseRandomLine):
    db_file = 'company-suffixes.txt'


class RandomLigature(BaseRandomLine):
    db_file = 'ligatures.txt'


class RandomRequirement(BaseRandomLine):
    db_file = 'requirements.txt'


class RandomDentalSchool(BaseRandomLine):
    db_file = 'dental-schools.txt'


class CliProgressBar(object):
    SYMBOL = '#'
    PROGRESS_BAR_FORMAT = \
        '\rPercent: [{bar}] {percent}% ETA: {eta} | Duration: {duration}\r'
    TIME_FORMAT = '{hours:02}:{minutes:02}:{seconds:02}'
    ETA_REFRESH_INTERVAL = datetime.timedelta(seconds=1)

    def __init__(self, size, bar_length=20):
        self._size = size
        self._bar_length = bar_length
        self._index = 0
        self._start_time = datetime.datetime.now()
        self._eta_cache = None
        self._last_time_eta = None

    def _get_duration(self):
        duration = (datetime.datetime.now() - self._start_time).seconds
        return dict(
            hours=duration // 3600, minutes=duration % 3600 // 60,
            seconds=duration % 60)

    def _get_eta(self, percent):
        now = datetime.datetime.now()
        if self._eta_cache is None or \
                now - self._last_time_eta >= self.ETA_REFRESH_INTERVAL:
            duration = (now - self._start_time).seconds
            eta = int(round(
                (duration / percent if percent > 0 else 0) - duration))
            self._eta_cache = dict(
                hours=eta // 3600, minutes=eta % 3600 // 60, seconds=eta % 60)
            self._last_time_eta = now
        return self._eta_cache

    def render(self):
        percent = float(self._index) / self._size
        hashes = self.SYMBOL * int(round(percent * self._bar_length))
        spaces = ' ' * (self._bar_length - len(hashes))
        sys.stdout.write(self.PROGRESS_BAR_FORMAT.format(
            bar=hashes + spaces,
            percent=int(round(percent * 100)),
            eta=self.TIME_FORMAT.format(**self._get_eta(percent)),
            duration=self.TIME_FORMAT.format(**self._get_duration())))
        sys.stdout.flush()
        self._index += 1

    def update(self, func, *args, **kwargs):
        self.render()
        return func(*args, **kwargs)
