# PYTHON LIBRARY MANAGER
 
# Personal Library Manager

Welcome to the **Personal Library Manager**, a sleek and interactive Streamlit application designed to help you organize your book collection. This app allows you to add, remove, search, and display books, with an optional integration of the Google Books API to fetch book details and cover images. The UI features a modern black-and-white theme with red accents for a striking look.

## Features

- **Core Functionality**:
  - Add books manually with title, author, publication year, genre, and read status.
  - Remove books by title.
  - Search your library by title or author.
  - Display all books in your collection.
  - View statistics (total books and percentage read).

- **Google Books Integration**:
  - Search for books online using the Google Books API.
  - Add multiple books at once with cover images from search results.

- **UI Design**:
  - Black background with white text for a minimalist aesthetic.
  - Display of book cover images where available.
  - Interactive sidebar menu and expandable search results.

- **File Handling**:
  - Save and load your library from a `library.txt` file for persistence.

## Prerequisites

- **Python 3.6 or higher**
- Required Python packages:
  - `streamlit`
  - `requests`

## Installation

1. **Clone or Download the Repository**:
   - Download the `library_manager.py` file or clone this project if hosted in a repository.

2. **Set Up a Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows