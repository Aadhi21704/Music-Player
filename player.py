# import streamlit as st
# import os
# import pygame

# # Initialize Pygame mixer
# pygame.mixer.init()

# # Get list of MP3 files and album art images
# mp3_files = [file for file in os.listdir("mp3_files") if file.endswith(".mp3")]
# album_art_files = [file for file in os.listdir("album_art") if file.endswith(".jpg")]

# # Create a dictionary to map song filenames to album art filenames
# song_to_album_art = {}
# for song in mp3_files:
#     song_name = os.path.splitext(song)[0]
#     for album_art in album_art_files:
#         if song_name in album_art:
#             song_to_album_art[song] = album_art

# def play_song(song_path):
#     pygame.mixer.music.load(song_path)
#     pygame.mixer.music.play()

# def main():
#     st.title("Playfy Music Player")

#     st.sidebar.title("Search Song")
#     search_query = st.sidebar.text_input("Search for a song:")

#     filtered_mp3_files = [file for file in mp3_files if search_query.lower() in os.path.splitext(file)[0].lower()]

#     if not filtered_mp3_files:
#         st.warning("No songs found.")
#         return

#     # Initialize session state index
#     if "current_song_index" not in st.session_state:
#         st.session_state.current_song_index = 0

#     song_changed = False  # Flag to track song change

#     # Adjust index on button clicks
#     if st.button("⏮️ Previous") and st.session_state.current_song_index > 0:
#         st.session_state.current_song_index -= 1
#         song_changed = True
#     if st.button("⏭️ Next") and st.session_state.current_song_index < len(filtered_mp3_files) - 1:
#         st.session_state.current_song_index += 1
#         song_changed = True

#     current_song_index = st.session_state.current_song_index
#     current_song = filtered_mp3_files[current_song_index]

#     st.header("All Songs:")
#     song_selection = st.radio("Select Song", filtered_mp3_files, index=current_song_index)

#     # Update index if user selects a different song manually
#     if song_selection != current_song:
#         st.session_state.current_song_index = filtered_mp3_files.index(song_selection)
#         current_song = song_selection
#         song_changed = True

#     song_path = os.path.join("mp3_files", current_song)

#     # Play song if it changed
#     if song_changed:
#         play_song(song_path)

#     st.sidebar.audio(song_path, format="audio/mp3", start_time=0)

#     # Display album art
#     album_art_image = song_to_album_art.get(current_song, "album_cover.jpeg")
#     album_art_path = f"album_art/{album_art_image}"
#     st.sidebar.image(album_art_path, use_column_width=True)

#     st.success(f"Now playing: {current_song}")


# if __name__ == "__main__":
#     main()




import streamlit as st
import os
import pygame
import re


# Initialize mixer once
if 'mixer_initialized' not in st.session_state:
    pygame.mixer.init()
    st.session_state.mixer_initialized = True

# Sorted song and art files
def natural_sort_key(s):
    # Split string into list of strings and integers
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

mp3_files_all = sorted([f for f in os.listdir("mp3_files") if f.endswith(".mp3")], key=natural_sort_key)

album_art_files = sorted([f for f in os.listdir("album_art") if f.endswith(".jpg")])

# Map songs to album art
song_to_album_art = {}
for song in mp3_files_all:
    base = os.path.splitext(song)[0]
    for art in album_art_files:
        if base in art:
            song_to_album_art[song] = art

# Functions
def play_song(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def pause_song():
    pygame.mixer.music.pause()

def resume_song():
    pygame.mixer.music.unpause()

def stop_song():
    pygame.mixer.music.stop()

def get_progress():
    pos = pygame.mixer.music.get_pos()
    return pos / 1000 if pos > 0 else 0

def main():
    st.title("🎧 Playfy Music Player")

    # Sidebar: Search
    st.sidebar.title("Search Song")
    search = st.sidebar.text_input("Search for a song:")

    # Filter and sort results
    if search:
        filtered_mp3_files = sorted([f for f in mp3_files_all if search.lower() in f.lower()], key=natural_sort_key)
    else:
        filtered_mp3_files = mp3_files_all[:]


    if not filtered_mp3_files:
        st.warning("No songs found.")
        return

    # Init session state
    if "current_song_index" not in st.session_state:
        st.session_state.current_song_index = 0
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "is_paused" not in st.session_state:
        st.session_state.is_paused = False

    # Clamp index
    st.session_state.current_song_index = min(st.session_state.current_song_index, len(filtered_mp3_files) - 1)
    idx = st.session_state.current_song_index
    current_song = filtered_mp3_files[idx]
    song_path = os.path.join("mp3_files", current_song)

    # --- Controls ---
    # --- Controls ---
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("⏮️Prev", key="prev"):
            if idx > 0:
                st.session_state.current_song_index -= 1
                idx -= 1
                current_song = filtered_mp3_files[idx]
                play_song(os.path.join("mp3_files", current_song))
                st.session_state.is_playing = True
                st.session_state.is_paused = False

    with col2:
        if st.button("▶️Play", key="play"):
            play_song(song_path)
            st.session_state.is_playing = True
            st.session_state.is_paused = False

    with col3:
        toggle_label = "⏸️/▶️" if st.session_state.is_playing and not st.session_state.is_paused else "⏸️/▶️"
        if st.button(toggle_label, key="pause_resume"):
            if st.session_state.is_playing and not st.session_state.is_paused:
                pause_song()
                st.session_state.is_paused = True
            elif st.session_state.is_playing and st.session_state.is_paused:
                resume_song()
                st.session_state.is_paused = False

    with col4:
        if st.button("⏹️Stop", key="stop"):
            stop_song()
            st.session_state.is_playing = False
            st.session_state.is_paused = False

    with col5:
        if st.button("⏭️Next", key="next"):
            if idx < len(filtered_mp3_files) - 1:
                st.session_state.current_song_index += 1
                idx += 1
                current_song = filtered_mp3_files[idx]
                play_song(os.path.join("mp3_files", current_song))
                st.session_state.is_playing = True
                st.session_state.is_paused = False


    st.success(f"Now playing: {current_song}")

    # Progress
    # if st.session_state.is_playing and not st.session_state.is_paused:
    #     prog = get_progress()
    #     st.write(f"⏱️ {int(prog)} sec")
    #     st.progress(min(prog / 180, 1.0))

    # Song List
    st.header("All Songs:")
    try:
        song_selection = st.radio("Select Song", filtered_mp3_files, index=idx)
    except st.errors.StreamlitAPIException:
        song_selection = filtered_mp3_files[0]
        st.session_state.current_song_index = 0
        idx = 0

    if song_selection != current_song:
        st.session_state.current_song_index = filtered_mp3_files.index(song_selection)
        play_song(os.path.join("mp3_files", song_selection))
        st.session_state.is_playing = True
        st.session_state.is_paused = False

    # Album Art
    album_img = song_to_album_art.get(current_song, "album_cover.jpeg")
    st.sidebar.image(f"album_art/{album_img}", use_column_width=True)

if __name__ == "__main__":
    main()
