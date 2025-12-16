import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# 1. Load your trained model
model = tf.keras.models.load_model('freshness_model (1).h5', compile=False)
# Create a custom loading function to handle the version mismatch
# def load_model_safe():
#     try:
#         # Try loading normally
#         return tf.keras.models.load_model('freshness_model.h5')
#     except TypeError:
#         # If that fails due to the 'batch_shape' error, try loading with compile=False
#         # and manually fixing the config if needed, OR just retraining.
#         # BUT, the easiest hack for this specific error is usually just:
#         return tf.keras.models.load_model('freshness_model.h5', compile=False)

# model = load_model_safe()

# If compile=False was used, you might need to recompile manually 
# (only needed if you plan to train more, for prediction it's usually fine)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

st.title("🍎 Smart Cold Storage Simulator")

# 2. Input: Webcam or File Upload
uploaded_file = st.file_uploader("Upload Fruit Image", type="jpg")

# 3. Simulation Sliders (Replacing Hardware Sensors)
st.sidebar.header("Storage Conditions (Simulation)")
temp = st.sidebar.slider("Temperature (°C)", -10, 40, 4)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 90)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Analyzed Fruit', use_column_width=True)
    
    # ==========================================
    # 1. PREPROCESS THE IMAGE
    # ==========================================
    # Resize to 224x224 (Standard for MobileNet/ResNet)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    # Convert to Numpy Array
    img_array = np.asarray(image)
    
    # Normalize (Scale pixel values from 0-255 to 0-1)
    # IMPORTANT: Check your Colab code. If you used resnet/mobilenet preprocessing, 
    # you might need a different scaler. This is the standard one:
    normalized_image_array = (img_array.astype(np.float32) / 255.0)
    
    # Create a batch of 1 (Shape: 1, 224, 224, 3)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # ==========================================
    # 2. MAKE THE PREDICTION
    # ==========================================
    prediction_array = model.predict(data)
    
    # Get the index of the highest score (e.g., Index 0 is Fresh, Index 1 is Rotten)
    max_index = np.argmax(prediction_array)
    
    # DEFINE YOUR CLASSES HERE (Must match your Training Folder order!)
    # Example: If your folder was A_Fresh, B_Rotten -> then 0=Fresh, 1=Rotten
    class_names = ['FreshApples', 'FreshBananas','FreshStrawberry','RottenApples', 'RottenBananas', 'RottenStrawberry'] 
    
    prediction = class_names[max_index]
    confidence = prediction_array[0][max_index]
    
    st.write(f"### Quality Status: {prediction}")
    #st.write(f"Confidence: {confidence * 100:.2f}%")
    
    # ==========================================
    # 3. LOGIC (Updated to use Real Prediction)
    # ==========================================
    if prediction == "Fresh":
        if temp > 25:
            st.error(f"⚠️ DANGER: Temp is {temp}°C! This fresh fruit will rot in <24 hours.")
        elif temp < 5:
            st.success(f"✅ SAFE: At {temp}°C, this fruit will last ~2 weeks.")
        else:
            st.info(f"ℹ️ Storage is okay.")
    else:
        st.warning("⛔ DISCARD: Fruit is already rotten. Temperature control irrelevant.")