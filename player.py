# import streamlit as st
# import os
# import re

# # --- Utility for natural sorting ---
# def natural_sort_key(s):
#     return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# # --- Load files ---
# mp3_files_all = sorted(
#     [f for f in os.listdir("mp3_files") if f.endswith(".mp3")],
#     key=natural_sort_key
# )

# album_art_files = sorted(
#     [f for f in os.listdir("album_art") if f.endswith(".jpg")],
#     key=natural_sort_key
# )

# # --- Map songs to album art ---
# song_to_album_art = {}
# for song in mp3_files_all:
#     base = os.path.splitext(song)[0]
#     for art in album_art_files:
#         if base in art:
#             song_to_album_art[song] = art

# # --- Streamlit App ---
# def main():
#     st.title("🎧 Playfy Music Player")

#     # --- Sidebar: Search ---
#     st.sidebar.title("Search Song")
#     search = st.sidebar.text_input("Search for a song:")

#     if search:
#         filtered_mp3_files = sorted(
#             [f for f in mp3_files_all if search.lower() in f.lower()],
#             key=natural_sort_key
#         )
#     else:
#         filtered_mp3_files = mp3_files_all[:]

#     if not filtered_mp3_files:
#         st.warning("No songs found.")
#         return

#     # --- Session state ---
#     if "current_song_index" not in st.session_state:
#         st.session_state.current_song_index = 0

#     # Clamp index
#     st.session_state.current_song_index = min(
#         st.session_state.current_song_index, len(filtered_mp3_files) - 1
#     )

#     idx = st.session_state.current_song_index
#     current_song = filtered_mp3_files[idx]

#     # --- Controls ---
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button("⏮️ Prev", key="prev"):
#             if idx > 0:
#                 st.session_state.current_song_index -= 1
#             st.experimental_rerun()
#             return

#     with col2:
#         st.markdown(f"**Now Playing:** `{current_song}`")

#     with col3:
#         if st.button("⏭️ Next", key="next"):
#             if idx < len(filtered_mp3_files) - 1:
#                 st.session_state.current_song_index += 1
#             st.experimental_rerun()
#             return

#     # --- Audio Player (auto plays due to rerun with new file) ---
#     st.sidebar.audio(f"mp3_files/{current_song}", format="audio/mp3", start_time=0)

#     # --- Album Art ---
#     album_img = song_to_album_art.get(current_song, "album_cover.jpeg")
#     st.sidebar.image(f"album_art/{album_img}", use_container_width=True)

#     # --- Song List ---
#     st.header("All Songs:")
#     try:
#         song_selection = st.radio("Select Song", filtered_mp3_files, index=idx)
#     except st.errors.StreamlitAPIException:
#         song_selection = filtered_mp3_files[0]
#         st.session_state.current_song_index = 0

#     if song_selection != current_song:
#         st.session_state.current_song_index = filtered_mp3_files.index(song_selection)
#         st.experimental_rerun()

# if __name__ == "__main__":
#     main()

import streamlit as st
import os
import re

# --- Utility for natural sorting ---
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# --- Load files ---
mp3_files_all = sorted(
    [f for f in os.listdir("mp3_files") if f.endswith(".mp3")],
    key=natural_sort_key
)

album_art_files = sorted(
    [f for f in os.listdir("album_art") if f.endswith(".jpg")],
    key=natural_sort_key
)

# --- Map songs to album art ---
song_to_album_art = {}
for song in mp3_files_all:
    base = os.path.splitext(song)[0]
    for art in album_art_files:
        if base in art:
            song_to_album_art[song] = art

# --- Streamlit App ---
def main():
    st.title("🎧 Playfy Music Player")

    # --- Top center: Search bar ---
    st.markdown(
        """
        <style>
        .top-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        </style>
        """, unsafe_allow_html=True
    )
    with st.container():
        st.markdown('<div class="top-container">', unsafe_allow_html=True)
        search = st.text_input("Search for a song:", key="search_input")
        st.markdown('</div>', unsafe_allow_html=True)

    # Filter songs based on search
    if search:
        filtered_mp3_files = sorted(
            [f for f in mp3_files_all if search.lower() in f.lower()],
            key=natural_sort_key
        )
    else:
        filtered_mp3_files = mp3_files_all[:]

    if not filtered_mp3_files:
        st.warning("No songs found.")
        return

    # --- Session state ---
    if "current_song_index" not in st.session_state:
        st.session_state.current_song_index = 0

    # Clamp index
    st.session_state.current_song_index = min(
        st.session_state.current_song_index, len(filtered_mp3_files) - 1
    )

    idx = st.session_state.current_song_index
    current_song = filtered_mp3_files[idx]

    # --- Audio Player centered below search ---
    # Use key with current song so Streamlit reloads the player when song changes
    st.audio(f"mp3_files/{current_song}", format="audio/mp3", start_time=0, key=f"audio_{current_song}")

    # --- Song List ---
    st.header("All Songs:")
    try:
        song_selection = st.radio("Select Song", filtered_mp3_files, index=idx)
    except st.errors.StreamlitAPIException:
        song_selection = filtered_mp3_files[0]
        st.session_state.current_song_index = 0

    if song_selection != current_song:
        st.session_state.current_song_index = filtered_mp3_files.index(song_selection)
        # No explicit rerun here — Streamlit will rerun automatically on session state change

    # --- Album Art in sidebar ---
    album_img = song_to_album_art.get(current_song, "album_cover.jpeg")
    st.sidebar.image(f"album_art/{album_img}", use_container_width=True)

if __name__ == "__main__":
    main()

