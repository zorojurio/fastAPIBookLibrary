from typing import List

from connection import Session
from models.books import Book
from schemas.books import BookCreate, BooksList


class BookHandler:
    def __init__(self, session: Session):
        self.session: Session = session

    def create_new_book(self, book: BookCreate):
        book = Book(
            title=book.title,
            author=book.author,
            publication_date=book.publication_date,
            isbn=book.isbn,
            cover_image=book.cover_image,
            user_id=book.user_id
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_book_list(self, user_id) -> List[BooksList]:
        modeled_books = []
        book_list = self.session.query(Book).filter_by(
            user_id=user_id
        )
        for book in book_list.all():
            modeled_books.append(BooksList(
                title=book.title,
                author=book.author,
                publication_date=book.publication_date,
                isbn=book.isbn,
                cover_image=book.cover_image,
                user_id=book.user_id,
                id=book.id
            ))
        return modeled_books

    def book_by_userid_book_id(self, user_id, book_id):
        book = self.session.query(Book).filter_by(
            user_id=user_id,
            id=book_id
        ).first()
        return BooksList(
            title=book.title,
            author=book.author,
            publication_date=book.publication_date,
            isbn=book.isbn,
            cover_image=book.cover_image,
            user_id=book.user_id,
            id=book.id
        )
