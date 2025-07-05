from api.schemas.wikipedia_title_extraction import WikipediaTitleExtraction


def test_wikipedia_title_extraction():
    titles = ["Python (programming language)", "Django (web framework)"]
    extraction = WikipediaTitleExtraction(titles=titles)
    assert extraction.titles == titles