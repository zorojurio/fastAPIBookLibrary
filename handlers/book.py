from datetime import datetime, timedelta
from typing import List

from sqlalchemy import or_

from connection import Session
from models.books import Book
from schemas.books import BookCreate, BooksList
from webapp.forms.book_form import BookForm


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

    def update_book(self, book: dict, book_id):
        existing_book = self.session.query(Book).filter(Book.id == book_id)
        existing_book.update(book)
        self.session.commit()

    @staticmethod
    def prepare_update_data(book_form: BookForm, image_path: str) -> dict:
        book_data = {}
        if image_path:
            book_data['cover_image'] = image_path
        if book_form.title:
            book_data['title'] = book_form.title
        if book_form.author:
            book_data['author'] = book_form.author
        if book_form.publication_date:
            book_data['publication_date'] = book_form.publication_date
        if book_form.isbn:
            book_data['isbn'] = book_form.isbn
        return book_data

    def delete_book(self, book_id):
        existing_book = self.session.query(Book).filter(Book.id == book_id)
        existing_book.delete()
        self.session.commit()

    def find_by_title_or_author(self, search: str) -> List[BooksList]:
        modeled_books = []
        query = self.session.query(Book).filter(
            or_(
                Book.title.like(f"%{search}%"),
                Book.author.like(f"%{search}%"),
            )
        )
        for book in query.all():
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

    def total_books_by_user(self, user_id):
        book = self.session.query(Book).filter_by(
            user_id=user_id)
        return book.count()

    def recent_books_by_user(self, user_id):
        modeled_books = []
        yesterday_date = datetime.now() - timedelta(days=1)
        query = self.session.query(Book).filter_by(
            user_id=user_id).filter(Book.created_at > yesterday_date)
        for book in query.all():
            modeled_books.append(BooksList(
                title=book.title,
                author=book.author,
                publication_date=book.publication_date,
                isbn=book.isbn,
                cover_image=book.cover_image,
                user_id=book.user_id,
                id=book.id
            ))
        return modeled_books, query.count()
