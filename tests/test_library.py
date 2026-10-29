from app.data.sample_documents import search_library


def test_hba1c_search_returns_note():
    results = search_library("What does HbA1c measure?")
    assert results
    assert any("HbA1c" in item["title"] for item in results)


def test_unknown_search_returns_empty():
    assert search_library("volcanic geology") == []
