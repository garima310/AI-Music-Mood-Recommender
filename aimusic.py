import streamlit as st
import requests
import json


st.set_page_config(page_title="AI Mood-Based Music Recommender", layout="centered")

API_KEY = "AIzaSyDpEGGhkNIWIQfdBk18jJzW6QfsZyy27nE"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + API_KEY


def get_music_recommendations(mood):
    try:
        payload = {
            "contents": [{
                "parts": [{"text": f"Recommend songs for a {mood} mood"}]
            }]
        }
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
           
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                return [part.get("text", "No song found") for part in parts]
            else:
                return ["No recommendations available"]
        else:
            st.error("Failed to fetch recommendations")
    except requests.RequestException as e:
        st.error(f"API Error: {e}")


st.title("🎵 AI Mood-Based Music Recommender")
user_mood = st.selectbox("Select Your Mood", ["Happy", "Sad", "Energetic", "Relaxed"])

if st.button("Get Recommendations"):
    songs = get_music_recommendations(user_mood)
    if songs:
        st.subheader("Recommended Songs:")
        for song in songs:
            st.write(f"- {song}")
    else:
        st.warning("No recommendations available.")