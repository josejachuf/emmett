# -*- coding: utf-8 -*-
"""
    tests.translator
    ----------------

    Test Emmett translator module
"""

import os
import pytest

from emmett import App, T
from emmett.ctx import current
from emmett.language import _instance as Tinstance


@pytest.fixture(scope='module')
def app():
    app = App(__name__)
    app.language_write = True
    delattr(Tinstance, '_t')
    return app


def _make_translation(language):
    return str(T('partly cloudy', language=language))


def test_translation(app):
    current.language = 'en'
    assert _make_translation('it') == 'nuvolosità variabile'
    assert _make_translation('de') == 'teilweise bewölkt'
    assert _make_translation('ru') == 'переменная облачность'


def test_write(app):
    current.language = 'en'
    #: get original content
    translated_file = os.path.join(app.root_path, 'languages', 'ru.py')
    with open(translated_file, encoding='utf8') as f:
        ocontents = f.read()
    #: write to file
    assert str(T('perché', language='ru')) == 'perché'
    #: get new contents and write back the original
    with open(translated_file, encoding='utf8') as f:
        contents = f.read()
    with open(translated_file, 'w', encoding='utf8') as f:
        f.write(ocontents)
    #: verify
    assert '"%s": "%s"' % ('perché', 'perché') in contents


# def test_cache():
#     pass
