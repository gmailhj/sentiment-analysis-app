import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import cv2
import json
import modals

# Emoji mapping for emotions
getEmoji = {
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "disgust": "🤢",
    "surprise": "😲",
    "fear": "😨",
    "angry": "😠",
}


def showEmotionData(emotion, topEmotion, image, idx):
    """Display emotion data for a detected person"""
    x, y, w, h = tuple(emotion["box"])
    cropImage = image[y:y+h, x:x+w]
    
    keys = list(emotion["emotions"].keys())
    values = list(emotion["emotions"].values())
    emotions = sorted(emotion["emotions"].items(), key=lambda kv: (kv[1], kv[0]))
    
    st.components.v1.html(f"""
    <h3 style="color: #ef4444; font-family: Source Sans Pro, sans-serif; font-size: 20px; margin-bottom: 0px; margin-top: 0px;">
        Person detected {idx}
    </h3>
    """, height=30)
    
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        st.image(cropImage, width=200)
    
    with col2:
        st.metric(f"{keys[0].capitalize()} {getEmoji.get(keys[0], '')}", round(values[0], 2))
        st.metric(f"{keys[1].capitalize()} {getEmoji.get(keys[1], '')}", round(values[1], 2))
        st.metric(f"{keys[2].capitalize()} {getEmoji.get(keys[2], '')}", round(values[2], 2))
        st.metric(f"{keys[3].capitalize()} {getEmoji.get(keys[3], '')}", round(values[3], 2))
    
    with col3:
        st.metric(f"{keys[4].capitalize()} {getEmoji.get(keys[4], '')}", round(values[4], 2))
        st.metric(f"{keys[5].capitalize()} {getEmoji.get(keys[5], '')}", round(values[5], 2))
        st.metric(f"{keys[6].capitalize()} {getEmoji.get(keys[6], '')}", round(values[6], 2))
        st.metric(f"Top Emotion", f"{emotions[len(emotions)-1][0].capitalize()} {getEmoji.get(topEmotion[0], '')}")
    
    st.components.v1.html("<hr>", height=5)


def printResultHead():
    """Print result section header"""
    st.write("")
    st.write("")
    st.components.v1.html("""
    <h3 style="color: #0ea5e9; font-family: Source Sans Pro, sans-serif; font-size: 26px; margin-bottom: 10px; margin-top: 60px;">
        Result
    </h3>
    <p style="color: #57534e; font-family: Source Sans Pro, sans-serif; font-size: 16px;">
        Find below the sentiments we found in your given image. What do you think about our results?
    </p>
    """, height=150)


def printImageInfoHead():
    """Print image information section header"""
    st.write("")
    st.write("")
    st.components.v1.html("""
    <h3 style="color: #ef4444; font-family: Source Sans Pro, sans-serif; font-size: 22px; margin-bottom: 0px; margin-top: 40px;">
        Image information
    </h3>
    <p style="color: #57534e; font-family: Source Sans Pro, sans-serif; font-size: 14px;">
        Expand below to see the information associated with the uploaded image
    </p>
    """, height=100)


def load_image(image_file):
    """Load and return PIL image"""
    image = Image.open(image_file, 'r')
    return image


def uploadFile():
    """Handle file upload and emotion analysis"""
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        try:
            content = Image.open(uploaded_file)
            content = np.array(content)  # PIL to numpy array
            
            # Check image dimensions
            shape = np.shape(content)
            if len(shape) < 3:
                st.error('Your image has a bit-depth less than 24. Please upload an image with a bit-depth of 24.')
                return
            
            # Analyze emotions
            emotions, topEmotion, image = modals.imageEmotion(content)
            
            # Check if FER is available
            if not modals.FER_AVAILABLE:
                st.warning("⚠️ FER (Facial Emotion Recognition) library is not installed. Image emotion detection is disabled.")
                st.info("To enable image emotion detection, install FER: `pip install fer`")
                return
            
            # Display file information
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            
            printImageInfoHead()
            with st.expander("See JSON Object"):
                st.json(json.dumps(file_details))
            
            st.text("")
            st.subheader("Original Image")
            st.image(load_image(uploaded_file), caption=uploaded_file.name, width=250)
            
            # Handle results
            if emotions is not None and len(emotions) == 0:
                st.warning("No faces found in the image!")
                return
            
            if emotions is not None:
                printResultHead()
                
                with st.expander("Expand to see individual results"):
                    st.write("")
                    contentcopy = Image.open(uploaded_file)
                    contentcopy = np.array(contentcopy)
                    
                    for i in range(len(emotions)):
                        showEmotionData(emotions[i], topEmotion, contentcopy, i + 1)
                
                st.write("")
                st.write("")
                
                # Display final results
                col1, col2 = st.columns([4, 2])
                
                with col1:
                    st.subheader("Processed Image")
                    st.image(image, width=300)
                
                with col2:
                    st.metric("Top Emotion", f"{topEmotion[0].capitalize()} {getEmoji.get(topEmotion[0], '')}")
                    st.metric("Confidence", f"{round(topEmotion[1] * 100, 2)}%")
                    
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.info("Please make sure you uploaded a valid image file.")


def renderPage():
    """Main page rendering function"""
    st.title("Sentiment Analysis 🎭")
    components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333; margin-bottom: 10px" /> """)
    
    st.subheader("Image Analysis")
    st.text("Upload an image and let's find emotions in the faces detected.")
    st.text("")
    
    option = st.selectbox(
        'How would you like to provide an image?',
        ('Upload One',)
    )
    
    if option == "Upload One":
        uploadFile()
