import streamlit as st
import json
import os
import requests

# File to save/load library
LIBRARY_FILE = "library.txt"
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Function to load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            content = file.read().strip()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    st.warning("Invalid JSON in library.txt. Starting with an empty library.")
                    return []
            return []
    return []

# Function to save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Function to search Google Books API
def search_google_books(query):
    params = {"q": query, "maxResults": 10}
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    return []

# Function to add a book manually or from Google Books
def add_book(library, title, author, year, genre, read_status, cover_url=None):
    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status,
        "cover_url": cover_url  # Store cover URL if available
    }
    library.append(book)
    return library

# Function to remove a book
def remove_book(library, title):
    library[:] = [book for book in library if book["title"].lower() != title.lower()]
    return library

# Function to search local library
def search_local_books(library, search_by, query):
    if search_by == "Title":
        return [book for book in library if query.lower() in book["title"].lower()]
    elif search_by == "Author":
        return [book for book in library if query.lower() in book["author"].lower()]
    return []

# Function to format book details
def format_book(book):
    read_status = "Read" if book["read"] else "Unread"
    return f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"

# Function to calculate statistics
def get_statistics(library):
    total_books = len(library)
    if total_books == 0:
        return "Total books: 0\nPercentage read: 0.0%"
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100
    return f"Total books: {total_books}\nPercentage read: {percentage_read:.1f}%"

# Custom CSS for black background with white text
def local_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #000000;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
        border-radius: 5px;
    }
    .stTextInput>div>input {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 5px;
    }
    .book-card {
        background-color: #000000;
        padding: 10px;
        border: 1px solid #ffffff;
        border-radius: 5px;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown p {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app
def main():
    # Page configuration
    st.set_page_config(
        page_title="Personal Library Manager",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    local_css()

    # Load library
    if "library" not in st.session_state:
        st.session_state.library = load_library()

    # Sidebar menu
    st.sidebar.title("📚 Library Manager")
    menu_options = ["Add a Book", "Search & Add from Google", "Remove a Book", "Search Local Library", 
                    "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu_options)

    # Main content
    st.title("📖 Your Personal Library Manager")
    st.markdown("Organize your books in black and white! Search online or manage your collection below.")

    # Add a Book (Manual)
    if choice == "Add a Book":
        st.header("Add a New Book")
        with st.form(key="add_book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=0, max_value=2025, step=1)
            genre = st.text_input("Genre")
            read_status = st.checkbox("Have you read this book?")
            submit = st.form_submit_button(label="Add Book")
            
            if submit and title and author and year and genre:
                st.session_state.library = add_book(st.session_state.library, title, author, year, genre, read_status)
                st.success("Book added successfully!")
            elif submit:
                st.error("Please fill in all fields.")

    # Search & Add from Google Books
    elif choice == "Search & Add from Google":
        st.header("Search Books Online")
        query = st.text_input("Enter a book title or author to search Google Books")
        if st.button("Search Google Books"):
            if query:
                results = search_google_books(query)
                if results:
                    st.subheader("Search Results")
                    selected_books = []
                    for i, item in enumerate(results):
                        book_info = item.get("volumeInfo", {})
                        title = book_info.get("title", "Unknown Title")
                        authors = ", ".join(book_info.get("authors", ["Unknown Author"]))
                        year = book_info.get("publishedDate", "N/A")[:4] if book_info.get("publishedDate") else "N/A"
                        genre = ", ".join(book_info.get("categories", ["Unknown Genre"])) if book_info.get("categories") else "Unknown Genre"
                        cover_url = book_info.get("imageLinks", {}).get("thumbnail", None)
                        
                        with st.expander(f"{title} by {authors}"):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                if cover_url:
                                    st.image(cover_url, width=100)
                                else:
                                    st.write("No cover available")
                            with col2:
                                st.write(f"Year: {year}")
                                st.write(f"Genre: {genre}")
                                if st.checkbox(f"Add '{title}' to library", key=f"add_{i}"):
                                    selected_books.append((title, authors, year, genre, cover_url))
                    
                    if st.button("Add Selected Books"):
                        for title, author, year, genre, cover_url in selected_books:
                            year = year if year.isdigit() else 0
                            st.session_state.library = add_book(st.session_state.library, title, author, year, genre, False, cover_url)
                        st.success(f"Added {len(selected_books)} books to your library!")
                else:
                    st.info("No books found.")
            else:
                st.error("Please enter a search query.")

    # Remove a Book
    elif choice == "Remove a Book":
        st.header("Remove a Book")
        title_to_remove = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            if title_to_remove:
                initial_len = len(st.session_state.library)
                st.session_state.library = remove_book(st.session_state.library, title_to_remove)
                if len(st.session_state.library) < initial_len:
                    st.success("Book removed successfully!")
                else:
                    st.warning("Book not found.")
            else:
                st.error("Please enter a title.")

    # Search Local Library
    elif choice == "Search Local Library":
        st.header("Search Your Library")
        search_by = st.radio("Search by:", ["Title", "Author"])
        query = st.text_input(f"Enter the {search_by.lower()} to search")
        if st.button("Search"):
            if query:
                results = search_local_books(st.session_state.library, search_by, query)
                if results:
                    st.subheader("Matching Books:")
                    for i, book in enumerate(results, 1):
                        st.markdown(f"<div class='book-card'>{i}. {format_book(book)}</div>", unsafe_allow_html=True)
                else:
                    st.info("No matching books found.")
            else:
                st.error(f"Please enter a {search_by.lower()}.")

    # Display All Books
    elif choice == "Display All Books":
        st.header("Your Library")
        if st.session_state.library:
            cols = st.columns(2)
            for i, book in enumerate(st.session_state.library):
                with cols[i % 2]:
                    st.markdown(f"<div class='book-card'>{format_book(book)}</div>", unsafe_allow_html=True)
                    if book.get("cover_url"):
                        st.image(book["cover_url"], width=100)
                    else:
                        st.write("No cover available")
        else:
            st.info("Your library is empty.")

    # Display Statistics
    elif choice == "Display Statistics":
        st.header("Library Statistics")
        stats = get_statistics(st.session_state.library)
        st.text(stats)

    # Exit
    elif choice == "Exit":
        save_library(st.session_state.library)
        st.success("Library saved to file. Goodbye!")
        st.stop()

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Powered by Google Books API")

if __name__ == "__main__":
    main()