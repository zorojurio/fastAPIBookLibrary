from connection import Session
from models.books import Book
from schemas.books import BookCreate


class BookHandler:
    def __init__(self, session: Session):
        self.session = session

    def create_new_book(self, book: BookCreate):
        book = Book(
            title=book.title,
            author=book.author,
            publication_date=book.publication_date,
            isbn=book.isbn,
            cover_image=book.cover_image
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book
