from textblob import TextBlob
import nltk
try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except ImportError:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import text2emotion as te
import cv2
import numpy as np

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

# Initialize models (with error handling)
try:
    from flair.models import TextClassifier
    from flair.data import Sentence
    sia = TextClassifier.load('en-sentiment')
    FLAIR_AVAILABLE = True
except ImportError:
    FLAIR_AVAILABLE = False
    print("Flair not available - some features will be disabled")

try:
    from fer import FER
    emo_detector = FER(mtcnn=True)
    FER_AVAILABLE = True
except ImportError:
    FER_AVAILABLE = False
    print("FER not available - image emotion detection will be disabled")


def flair(text):
    """
    Sentiment analysis using Flair
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Sentiment classification (POSITIVE/NEGATIVE/NEUTRAL)
    """
    if not FLAIR_AVAILABLE:
        return "NEUTRAL - Flair not available"
    
    sentence = Sentence(text)
    sia.predict(sentence)
    score = str(sentence.labels[0])
    
    startIdx = int(score.rfind("("))
    endIdx = int(score.rfind(")"))
    percentage = float(score[startIdx+1:endIdx])
    
    if percentage < 0.60:
        return "NEUTRAL"
    elif "POSITIVE" in str(score):
        return "POSITIVE"
    elif "NEGATIVE" in str(score):
        return "NEGATIVE"


def textBlob(text):
    """
    Sentiment analysis using TextBlob
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Sentiment classification (Positive/Negative/Neutral)
    """
    tb = TextBlob(text)
    polarity = round(tb.polarity, 2)
    
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"


def vader(text):
    """
    Sentiment analysis using VADER
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Sentiment classification (Positive/Negative/Neutral)
    """
    scores = SentimentIntensityAnalyzer().polarity_scores(text)
    
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def text2emotion(text):
    """
    Emotion analysis using text2emotion
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Dominant emotion(s)
    """
    emotion = dict(te.get_emotion(text))
    emotion = sorted(emotion.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    
    emotionStr = list(emotion)[0][0]
    
    if (list(emotion)[1][1] >= 0.5 or list(emotion)[1][1] == list(emotion)[0][1]):
        emotionStr += " - {}".format(list(emotion)[1][0])
    
    print(emotion, emotionStr)
    return emotionStr


def imageEmotion(image):
    """
    Emotion detection in images using FER
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        tuple: (detected_emotions, top_emotion, annotated_image)
    """
    if not FER_AVAILABLE:
        return [], ("neutral", 0.0), image
    
    captured_emotions = emo_detector.detect_emotions(image)
    topEmotion = emo_detector.top_emotion(image)
    
    print(captured_emotions, topEmotion)
    
    img = image.copy()
    
    # Font settings for annotation
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1.2
    color = (255, 0, 0)  # Blue color in BGR
    thickness = 2
    
    # Annotate image with emotion detection results
    for emotion in captured_emotions:
        x, y, w, h = tuple(emotion["box"])
        org = (x + w + 4, y + 5)
        emotions = emotion["emotions"]
        emotions = sorted(emotions.items(), key=lambda kv: (kv[1], kv[0]))
        
        # Draw rectangle around face
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Add emotion label
        cv2.putText(img, emotions[len(emotions) - 1][0], org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
    
    return captured_emotions, topEmotion, img
