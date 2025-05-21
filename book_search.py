from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
from sqlalchemy import text

server_name = "5CD21553SB\\MSSQLSERVER02"   # kan behöva ändras av användaren!
database_name = "bookstore"

connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes"
url_string = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

try:
    engine = create_engine(url_string)
    with engine.connect() as connection:
        print(f"\nUppkopplad mot databasen {database_name}")
except Exception as e:
    print("Error while connecting to database:\n")
    print(e)



def search_for_book(search_string):
    # sök efter bok med injection-säker query:
    query = text("""
    SELECT
        Titel,
        bocker.ISBN13 as 'ISBN',
        CONCAT(Fornamn, ' ', Efternamn) AS 'Forfattare',
        butiker.Namn AS 'Bokhandel',
        Antal AS 'Lagersaldo'
    FROM
        bocker
        JOIN forfattare ON bocker.ForfattareID = forfattare.ID
        JOIN lagersaldo ON bocker.ISBN13 = lagersaldo.ISBN13
        JOIN butiker ON lagersaldo.ButikID = butiker.ID
    WHERE
        Titel LIKE '%' + :placeholder + '%'
    GROUP BY Titel, bocker.ISBN13, butiker.Namn, CONCAT(Fornamn, ' ', Efternamn), lagersaldo.antal""")

    with engine.connect() as conn:
        result = conn.execute(query, {"placeholder": search_string})
        print(f"{'TITEL'.ljust(27)}{'ISBN'.ljust(20)}{'FÖRFATTARE'.ljust(20)}{'BOKHANDEL'.ljust(15)}{'LAGERSALDO'}")

        for books in result:
            print(f"{str(books.Titel).ljust(27)}{str(books.ISBN).ljust(20)}{str(books.Forfattare).ljust(20)}{str(books.Bokhandel).ljust(15)}{str(books.Lagersaldo)}")



while True:
    search_string=str(input("\nSkriv en del av en boktitel, eller q för att avsluta. "))
    if search_string=="q":
        break
    else:
        print("\nBöckerna du sökte efter finns i dessa bokhandlar:\n")
        search_for_book(search_string)

print("Ha en bra dag!")
