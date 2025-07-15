import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import modals

# OMDB API configuration
baseURL = 'http://www.omdbapi.com'
apiKey = '38a7a5fd'  # Your OMDB API key

# Emoji mapping for emotions/sentiments
getEmoji = {
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "disgust": "🤢",
    "surprise": "😲",
    "fear": "😨",
    "angry": "😠",
    "positive": "😊",
    "negative": "😞",
    "POSITIVE": "😊",
    "NEGATIVE": "😞",
    "NEUTRAL": "😐"
}

# Cache for API responses
lastSearched = ""
cacheData = {}


def plotPie(labels, values):
    """Create a pie chart for sentiment distribution"""
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=[value * 100 for value in values],
            hoverinfo="label+percent",
            textinfo="value"
        )
    )
    st.plotly_chart(fig, use_container_width=True)


def getMovies(movieName):
    """Get movies from OMDB API based on search query"""
    try:
        response = requests.get(f'{baseURL}/?s={movieName}&apikey={apiKey}')
        response = response.json()
        
        if response.get("Response") == "True":
            movies = [
                {
                    "id": result['imdbID'],
                    "title": result['Title'],
                    "image": result.get("Poster", "N/A"),
                    "description": f"{result['Year']} - {result['Type'].title()}",
                    "year": result['Year'],
                    "type": result['Type']
                }
                for result in response["Search"]
            ]
            return movies
        else:
            st.error(response.get("Error", "Unknown error occurred"))
            return []
    except Exception as e:
        st.error(f"Error fetching movies: {str(e)}")
        return []


def getFirst200Words(string):
    """Truncate string to first 200 characters"""
    if len(string) > 200:
        return string[:200]
    return string


def getMovieDetails(id):
    """Get detailed movie information from OMDB API"""
    try:
        response = requests.get(f'{baseURL}/?i={id}&apikey={apiKey}')
        response = response.json()
        
        if response.get("Response") == "True":
            # Create sample reviews from movie details
            plot = response.get("Plot", "")
            genre = response.get("Genre", "")
            actors = response.get("Actors", "")
            director = response.get("Director", "")
            
            # Generate sample text content for sentiment analysis
            reviews = []
            if plot and plot != "N/A":
                reviews.append(f"The plot is interesting: {plot}")
            
            if genre and genre != "N/A":
                reviews.append(f"Great {genre.lower()} movie with excellent storytelling")
            
            if actors and actors != "N/A":
                reviews.append(f"Amazing performances by {actors}. Outstanding acting throughout.")
            
            if director and director != "N/A":
                reviews.append(f"Brilliant direction by {director}. Masterful filmmaking.")
            
            # Add some generic positive and negative reviews for demonstration
            reviews.extend([
                "This movie was absolutely fantastic! Great story and characters.",
                "One of the best films I've seen. Highly recommend.",
                "Excellent cinematography and soundtrack. Loved every minute.",
                "The movie was okay, nothing special but watchable.",
                "Not bad, but could have been better. Average at best.",
                "Disappointing. Expected more from this film."
            ])
            
            return reviews[:10]  # Return first 10 reviews
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching movie details: {str(e)}")
        return []


def getData(movieName):
    """Get movie data and reviews"""
    print("Sending request to get movies!!!!!!")
    movies = getMovies(movieName)
    data = []
    
    for movie in movies:
        reviews = getMovieDetails(movie["id"])
        data.append({
            "title": movie["title"],
            "image": movie["image"],
            "description": movie["description"],
            "reviews": reviews
        })
    
    return json.dumps({"userSearch": movieName, "result": data})


def displayMovieContent(movie):
    """Display movie information"""
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.image(movie["image"], width=200)
    
    with col2:
        st.components.v1.html(f"""
        <h3 style="color: #1e293b; font-family: Source Sans Pro, sans-serif; font-size: 20px; margin-bottom: 10px; margin-top: 60px;">
            {movie["title"]}
        </h3>
        <p style="color: #64748b; font-family: Source Sans Pro, sans-serif; font-size: 14px;">
            {movie["description"]}
        </p>
        """, height=150)


def getEmojiString(head):
    """Get emoji string for emotion/sentiment"""
    emojiHead = ""
    emotions = head.split("-")
    for emotion in emotions:
        emo = emotion.strip()
        emojiHead += getEmoji.get(emo.lower(), getEmoji.get(emo, ""))
    return head + " " + emojiHead


def applyModal(movie, packageName):
    """Apply sentiment analysis model to movie reviews"""
    try:
        if packageName == "Flair":
            predictionList = [modals.flair(review) for review in movie["reviews"]]
        elif packageName == "TextBlob":
            predictionList = [modals.textBlob(review) for review in movie["reviews"]]
        elif packageName == "Vader":
            predictionList = [modals.vader(review) for review in movie["reviews"]]
        elif packageName == "Text2emotion":
            predictionList = [modals.text2emotion(review) for review in movie["reviews"]]
        else:
            return {}
        
        valueCounts = dict(pd.Series(predictionList).value_counts())
        print(valueCounts)
        return valueCounts
    except Exception as e:
        st.error(f"Error analyzing reviews: {str(e)}")
        return {}


def process(movieName, packageName):
    """Process movie search and sentiment analysis"""
    global lastSearched, cacheData
    
    if lastSearched != movieName:
        data = getData(movieName)
        lastSearched = movieName
        cacheData = data
    else:
        data = cacheData
    
    try:
        data_dict = json.loads(data) if isinstance(data, str) else data
        movies = data_dict.get("result", [])
        
        if len(movies) > 0:
            st.text("")
            st.components.v1.html("""
            <h3 style="color: #ef4444; font-family: Source Sans Pro, sans-serif; font-size: 22px; margin-bottom: 0px; margin-top: 40px;">
                API Response
            </h3>
            <p style="color: #57534e; font-family: Source Sans Pro, sans-serif; font-size: 14px;">
                Expand below to see the API response received for the search
            </p>
            """, height=100)
            
            with st.expander("See JSON Response"):
                st.json(data)
            
            # Display results
            st.components.v1.html("""
            <h3 style="color: #0ea5e9; font-family: Source Sans Pro, sans-serif; font-size: 26px; margin-bottom: 10px; margin-top: 60px;">
                Result
            </h3>
            <p style="color: #57534e; font-family: Source Sans Pro, sans-serif; font-size: 16px;">
                Below are the movies we received related to your search. We have analyzed each and every one for you. Enjoy!
            </p>
            """, height=150)
            
            for movie in movies:
                if len(movie.get("reviews", [])) > 0:
                    with st.expander(movie["title"]):
                        result = applyModal(movie, packageName)
                        
                        if result:
                            keys = list(result.keys())
                            values = list(result.values())
                            
                            st.write("")
                            st.write("")
                            displayMovieContent(movie)
                            
                            # Display metrics in rows of 4
                            for i in range(0, len(keys), 4):
                                if (i + 3) < len(keys):
                                    cols = st.columns(4)
                                    for j in range(4):
                                        if i + j < len(keys):
                                            cols[j].metric(
                                                getEmojiString(keys[i + j]),
                                                round(values[i + j], 2)
                                            )
                                else:
                                    cols = st.columns(4)
                                    for j in range(len(keys) - i):
                                        cols[j].metric(
                                            getEmojiString(keys[i + j]),
                                            round(values[i + j], 2)
                                        )
                            
                            st.write("")
                            st.write("")
                            
                            # Display pie chart
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.subheader("Visual Representation")
                                plotPie(
                                    list(result.keys()),
                                    [value / len(movie["reviews"]) for value in list(result.values())]
                                )
                else:
                    st.warning(f"No reviews found for {movie['title']}")
        else:
            st.warning("No movies found for your search query.")
    except Exception as e:
        st.error(f"Error processing results: {str(e)}")


def renderPage():
    """Main page rendering function"""
    st.title("Sentiment Analysis 🎭")
    components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333; margin-bottom: 10px" /> """)
    
    st.subheader("Movie Analysis with OMDB API")
    st.text("Search for movies using OMDB API and analyze generated content for sentiments.")
    st.info("💡 This demo uses movie details from OMDB API to generate sample content for sentiment analysis.")
    st.text("")
    
    movieName = st.text_input('Movie Name', placeholder='Input name HERE')
    # Check available packages
    available_packages = ['Vader', 'TextBlob', 'Text2emotion']
    if modals.FLAIR_AVAILABLE:
        available_packages.insert(0, 'Flair')
    
    packageName = st.selectbox(
        'Select Package',
        available_packages
    )
    
    # Show warning if Flair is not available
    if not modals.FLAIR_AVAILABLE:
        st.info("💡 Flair is not available. Install it with: `pip install flair` to get more sentiment analysis options.")
    
    if st.button('Search'):
        if movieName:
            process(movieName, packageName)
        else:
            st.warning("Please enter a movie name")
