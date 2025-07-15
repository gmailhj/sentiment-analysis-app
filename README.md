# 🎭 Sentiment Analysis App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sentiment-analysis-app-iusftka3xxnktmdsyq5foy.streamlit.app/)

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/gmailhj/sentiment-analysis-app)

A comprehensive sentiment analysis application built with Streamlit that supports multiple types of input: text, images, and movie analysis using OMDB API.

## 🚀 Live Demo

**[🔗 Try the app live here!](https://sentiment-analysis-app-iusftka3xxnktmdsyq5foy.streamlit.app/)** - Your app is now live and ready to use!

## 📸 Screenshots

![App Screenshot](https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=Sentiment+Analysis+App)

## Features

### 1. Text Analysis
- **TextBlob**: Analyzes polarity and subjectivity for positive/negative/neutral sentiment
- **Text2emotion**: Detects emotions like happy, sad, angry, fear, and surprise

### 2. Image Analysis
- **Face Detection**: Automatically detects faces in uploaded images
- **Emotion Recognition**: Identifies emotions from facial expressions
- **Visual Results**: Shows cropped faces with emotion scores and annotated images

### 3. IMDb Movie Reviews Analysis
- **Movie Search**: Search for movies using IMDb API
- **Review Analysis**: Analyze up to 20 reviews per movie
- **Multiple Models**: Choose from Flair, Vader, TextBlob, or Text2emotion
- **Visual Charts**: Pie charts showing sentiment distribution

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download additional NLTK data** (if needed):
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

## Configuration

### IMDb API Setup
1. Get an API key from [IMDb API](https://imdb-api.com/)
2. Replace the API key in `imdbReviewsPage.py`:
   ```python
   apiKey = 'your_api_key_here'
   ```

## Usage

1. **Run the application**:
   ```bash
   streamlit run main.py
   ```

2. **Navigate through the sidebar**:
   - **Text**: Enter text for sentiment analysis
   - **Image**: Upload images for emotion detection
   - **IMDb movie reviews**: Search movies and analyze reviews

## File Structure

```
sentiment_analysis_app/
├── main.py                 # Main application entry point
├── sidebar.py             # Navigation sidebar
├── textPage.py            # Text analysis page
├── imagePage.py           # Image analysis page
├── imdbReviewsPage.py     # IMDb reviews analysis page
├── modals.py              # ML models and analysis functions
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Models Used

- **Flair**: Pre-trained sentiment analysis model
- **TextBlob**: Simple sentiment analysis library
- **VADER**: Valence Aware Dictionary and sEntiment Reasoner
- **Text2emotion**: Emotion detection from text
- **FER**: Facial Emotion Recognition for images

## Dependencies

- `streamlit`: Web app framework
- `flair`: NLP library with pre-trained models
- `textblob`: Text processing library
- `text2emotion`: Emotion detection from text
- `fer`: Facial emotion recognition
- `opencv-python`: Computer vision library
- `plotly`: Interactive plotting library
- `pandas`: Data manipulation library
- `pillow`: Image processing library
- `requests`: HTTP library for API calls
- `nltk`: Natural language processing library

## Notes

- The first run might take time as models need to be downloaded
- For image analysis, ensure uploaded images have faces visible
- IMDb API has rate limits, so use responsibly
- The app supports PNG, JPG, and JPEG image formats

## Troubleshooting

1. **Model loading errors**: Ensure all dependencies are installed
2. **API errors**: Check your IMDb API key and internet connection
3. **Image processing errors**: Ensure image format is supported and has sufficient quality
4. **Memory issues**: Close other applications if running on limited memory systems

## License

This project is for educational and demonstration purposes.
