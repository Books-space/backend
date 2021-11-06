import pytest

from webapp.searcher import WaterfallSearcher


@pytest.fixture
def searcher():
    return WaterfallSearcher()
