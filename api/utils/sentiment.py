from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

def clasificar_sentimiento(texto):
    score = analyzer.polarity_scores(texto)['compound']
    if score >= 0.05:
        return "Positivo"
    elif score <= -0.05:
        return "Negativo"
    return "Neutral"
