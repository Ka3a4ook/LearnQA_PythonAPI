def test_short_phrase():
    phrase = input("Set a less than 15 symbols phrase: ")
    assert len(phrase) < 15
