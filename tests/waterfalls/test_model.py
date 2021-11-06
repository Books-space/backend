import pytest

from webapp.searcher import WaterfallSearcher


@pytest.mark.parametrize('text, expected', [
    ('медвежий', 'Медвежий водопад'),
    ('ниагара', 'Ниагарский водопад'),
    ('Ниагара', 'Ниагарский водопад'),
])
def test_waterfall_found(searcher: WaterfallSearcher, text, expected):
    waterfall = searcher.search(text)
    assert waterfall
    assert waterfall.title == expected


@pytest.mark.parametrize('text', [
    'волчий',
    '131232',
])
def test_waterfall_notfound(searcher: WaterfallSearcher, text):
    waterfall = searcher.search(text)
    assert not waterfall


def test_waterfall_found_multi_words(searcher: WaterfallSearcher):
    waterfall = searcher.search('медвежий водопад')
    assert waterfall
    assert waterfall.title == 'Медвежий водопад'
