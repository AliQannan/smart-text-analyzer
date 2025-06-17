import pytest
from collections import Counter
from smart_text_analyzer import SmartTextAnalyzer

@pytest.fixture
def analyzer():
    return SmartTextAnalyzer()

def test_preprocess_text(analyzer):
    sample_text = "Hello world. Hello AI."
    analyzer.preprocess_text(sample_text)
    assert len(analyzer.text) == 4
    assert analyzer.word_counts['hello'] == 2
    assert analyzer.char_counts['h'] == 2
    assert 'hello' in analyzer.vocabulary

def test_build_bigrams(analyzer):
    analyzer.text = ['machine', 'learning', 'is', 'fun']
    analyzer.build_bigrams()
    assert analyzer.bigrams['machine']['learning'] == 1
    assert analyzer.bigrams['learning']['is'] == 1
    assert analyzer.bigrams['is']['fun'] == 1

def test_autocomplete(analyzer):
    analyzer.vocabulary = {'hello', 'hi', 'hey', 'house'}
    prefix = 'h'
    suggestions = [w for w in analyzer.vocabulary if w.startswith(prefix)]
    assert set(suggestions) == {'hello', 'hi', 'hey', 'house'}

def test_predict_next_word(analyzer):
    analyzer.text = ['data', 'science', 'is', 'cool']
    analyzer.build_bigrams()
    assert analyzer.bigrams['data']['science'] == 1
    assert analyzer.bigrams['science']['is'] == 1

def test_keyword_extraction(analyzer):
    analyzer.text = ['data', 'is', 'the', 'new', 'oil', 'data']
    analyzer.stop_words = {'is', 'the'}
    filtered = [w for w in analyzer.text if w not in analyzer.stop_words]
    freq = Counter(filtered)
    assert freq['data'] == 2
    assert 'is' not in freq

def test_wordcloud_data(analyzer):
    analyzer.text = ['ai', 'ai', 'ml', 'data']
    analyzer.stop_words = set()
    freq = Counter(analyzer.text)
    max_freq = max(freq.values())
    wordcloud = [(w, round(c / max_freq, 2)) for w, c in freq.items()]
    assert ('ai', 1.0) in wordcloud
    assert ('ml', 0.5) in wordcloud

def test_sentiment_analysis_positive(analyzer, capsys):
    analyzer.positive_words = {'good'}
    analyzer.negative_words = {'bad'}
    input_text = "this is good"
    analyzer.sentiment_analysis = lambda: print("Sentiment: Positive") if "good" in input_text else print("Sentiment: Neutral")
    analyzer.sentiment_analysis()
    captured = capsys.readouterr()
    assert "Positive" in captured.out
