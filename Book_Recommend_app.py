import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))
user_similarity = pickle.load(open("user_similarity.pkl", "rb"))


def recommend_item(book_name, top_n):
    if book_name not in pt.index:
        return []

    index = np.where(pt.index == book_name)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]

    data = []

    for i in similar_items:
        temp_df = books[books["Book-Title"] == pt.index[i[0]]].drop_duplicates("Book-Title")

        if temp_df.empty:
            continue

        data.append({
            "Book-Title": temp_df["Book-Title"].values[0],
            "Book-Author": temp_df["Book-Author"].values[0],
            "Image-URL-M": temp_df["Image-URL-M"].values[0]
        })

    return data


def recommend_user(user_id, top_n, threshold, similar_user_count):
    if user_id not in pt.columns:
        return []

    user_index = list(pt.columns).index(user_id)

    similar_users = sorted(
        list(enumerate(user_similarity[user_index])),
        key=lambda x: x[1],
        reverse=True
    )[1:similar_user_count + 1]

    similar_user_ids = [pt.columns[i[0]] for i in similar_users]
    user_rated_books = set(pt[pt[user_id] > 0].index)

    recommended_books = {}

    for sim_user in similar_user_ids:
        liked_books = pt[pt[sim_user] >= threshold][sim_user]

        for book_title, rating in liked_books.items():
            if book_title not in user_rated_books:
                recommended_books[book_title] = max(
                    recommended_books.get(book_title, 0),
                    rating
                )

    top_books = sorted(
        recommended_books.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    data = []

    for book_title, rating in top_books:
        temp_df = books[books["Book-Title"] == book_title].drop_duplicates("Book-Title")

        if temp_df.empty:
            continue

        data.append({
            "Book-Title": temp_df["Book-Title"].values[0],
            "Book-Author": temp_df["Book-Author"].values[0],
            "Image-URL-M": temp_df["Image-URL-M"].values[0],
            "Predicted-Rating": rating
        })

    return data


def display_books(recommendations, show_rating=False):
    cols = st.columns(len(recommendations))

    for i, book in enumerate(recommendations):
        with cols[i]:
            st.image(book["Image-URL-M"], width=150)
            st.markdown(f"**{book['Book-Title']}**")
            st.caption(book["Book-Author"])

            if show_rating:
                st.write("⭐ Predicted Rating:", book["Predicted-Rating"])


st.title("📚 Book Recommendation System")
st.write("Interactive book recommendation app using collaborative filtering.")

with st.expander("ℹ️ About this project"):
    st.write("""
    This app provides two types of recommendations:

    **Item-Based Recommendation:**  
    Recommends books similar to the selected book based on user rating patterns.

    **User-Based Recommendation:**  
    Finds users with similar reading behavior and recommends books liked by those users.
    """)

st.sidebar.title("⚙️ Controls")

recommendation_type = st.sidebar.selectbox(
    "Select Recommendation Type",
    ["Item-Based Recommendation", "User-Based Recommendation"]
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    min_value=1,
    max_value=5,
    value=5
)

st.sidebar.markdown("---")

if recommendation_type == "User-Based Recommendation":
    threshold = st.sidebar.slider(
        "Minimum Rating Threshold",
        min_value=1,
        max_value=10,
        value=5
    )

    similar_user_count = st.sidebar.slider(
        "Number of Similar Users",
        min_value=5,
        max_value=20,
        value=10
    )

if recommendation_type == "Item-Based Recommendation":
    st.header("📖 Item-Based Recommendation")

    selected_book = st.selectbox(
        "Search or select a book",
        pt.index.values
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        recommend_btn = st.button("🔍 Recommend")

    if recommend_btn:
        recommendations = recommend_item(selected_book, top_n)

        if len(recommendations) == 0:
            st.warning("No recommendations found.")
        else:
            st.success(f"Top {len(recommendations)} recommendations for: {selected_book}")
            display_books(recommendations)

else:
    st.header("👤 User-Based Recommendation")

    selected_user = st.selectbox(
        "Select User ID",
        pt.columns.values
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        recommend_btn = st.button("👤 Recommend")

    if recommend_btn:
        recommendations = recommend_user(
            selected_user,
            top_n,
            threshold,
            similar_user_count
        )

        if len(recommendations) == 0:
            st.warning("No recommendations found. Try lowering the rating threshold or increasing similar users.")
        else:
            st.success(f"Top {len(recommendations)} recommendations for User ID: {selected_user}")
            display_books(recommendations, show_rating=True)