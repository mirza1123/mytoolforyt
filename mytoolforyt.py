import streamlit as st
from googleapiclient.discovery import build
import openai  

# Set up YouTube API (AIzaSyDo00DFPKss9jjiwGGl2pD6St32wujR4j8)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Set up OpenAI API (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)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
openai.api_key = OPENAI_API_KEY

# Function to get video data from a YouTube channel
def get_channel_videos(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=5,
        order="date"
    )
    response = request.execute()
    return response["items"]

# Function to generate AI content
def generate_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("YouTube Automation Tool")

channel_id = st.text_input("Enter YouTube Channel ID:")
if st.button("Fetch Videos"):
    if channel_id:
        videos = get_channel_videos(channel_id)
        for video in videos:
            st.subheader(video["snippet"]["title"])
            st.image(video["snippet"]["thumbnails"]["high"]["url"])
            st.write(f"Video ID: {video['id']['videoId']}")

            # Generate title, script, description, and tags
            title_prompt = f"Generate a viral YouTube title for this video: {video['snippet']['title']}"
            script_prompt = f"Generate a video script for this video: {video['snippet']['title']}"
            desc_prompt = f"Generate a YouTube description for this video: {video['snippet']['title']}"
            tags_prompt = f"Generate relevant tags for this video: {video['snippet']['title']}"

            title = generate_content(title_prompt)
            script = generate_content(script_prompt)
            description = generate_content(desc_prompt)
            tags = generate_content(tags_prompt)

            st.write("*AI-Generated Title:*", title)
            st.write("*AI-Generated Script:*", script)
            st.write("*AI-Generated Description:*", description)
            st.write("*AI-Generated Tags:*", tags)

    else:
        st.error("Please enter a valid YouTube Channel ID.")
