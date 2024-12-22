import json

BOOKS_FILE = 'books.json'


class Book:
    def __init__(self, title, author, genre, year):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year
        }

    @staticmethod
    def from_dict(data):
        return Book(data['title'], data['author'], data['genre'], data['year'])


class BookManager:
    @staticmethod
    def create_default_books_file():

        try:
            with open(BOOKS_FILE, 'r') as file:
                pass
        except FileNotFoundError:
            default_books = [
                Book("O‘zbekiston Tarixi", "Abdulla Qodiriy", "Tarix", 1926),
                Book("Alisher Navoiy", "Alisher Navoiy", "Adabiyot", 1473),
                Book("Python Dasturlash", "Guido van Rossum", "Dasturlash", 1991)
            ]
            BookManager.save_books(default_books)
            print(f"{BOOKS_FILE} fayli yaratildi va boshlang'ich kitoblar qo'shildi.")

    @staticmethod
    def read_books():
        try:
            with open(BOOKS_FILE, 'r') as file:
                books_data = json.load(file)
            return [Book.from_dict(book) for book in books_data]
        except FileNotFoundError:
            return []

    @staticmethod
    def save_books(books):
        with open(BOOKS_FILE, 'w') as file:
            json.dump([book.to_dict() for book in books], file, indent=4)

    @staticmethod
    def add_book(title, author, genre, year):
        books = BookManager.read_books()
        new_book = Book(title, author, genre, year)
        books.append(new_book)
        BookManager.save_books(books)
        print(f"Kitob '{title}' saqlandi!")

    @staticmethod
    def display_books():
        books = BookManager.read_books()
        if books:
            print("\nKitoblar Ro'yxati:")
            for book in BookManager.books_generator(books):
                print(f"ID: {book.title} | Muallif: {book.author} | Janr: {book.genre} | Yil: {book.year}")
        else:
            print("Kitoblar ro'yxati bo'sh.")

    @staticmethod
    def books_generator(books):
        for book in books:
            yield book

    @staticmethod
    def search_books_by_title(title):
        books = BookManager.read_books()
        found_books = [book for book in books if title.lower() in book.title.lower()]
        if found_books:
            print(f"\n'{title}' nomli kitoblar:")
            for book in BookManager.books_generator(found_books):
                print(f"{book.title} | Muallif: {book.author} | Janr: {book.genre} | Yil: {book.year}")
        else:
            print(f"'{title}' nomli kitoblar topilmadi.")


def main():
    BookManager.create_default_books_file()

    while True:
        print("\nKitoblar Boshqaruv Tizimi:")
        print("1. Kitob qo'shish")
        print("2. Kitoblarni ko'rish")
        print("3. Kitobni qidirish")
        print("4. Chiqish")

        choice = input("Tanlovingizni kiriting (1/2/3/4): ")

        if choice == '1':
            title = input("Kitob nomini kiriting: ")
            author = input("Muallif nomini kiriting: ")
            genre = input("Kitob janrini kiriting: ")
            year = input("Kitob chiqarilgan yilni kiriting: ")
            BookManager.add_book(title, author, genre, int(year))

        elif choice == '2':
            BookManager.display_books()

        elif choice == '3':
            title = input("Qidirilayotgan kitob nomini kiriting: ")
            BookManager.search_books_by_title(title)

        elif choice == '4':
            print("Dasturdan chiqyapman...")
            break

        else:
            print("Noto'g'ri tanlov. Iltimos, qayta urinib ko'ring.")


if __name__ == '__main__':
    main()
