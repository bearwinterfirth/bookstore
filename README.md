## Om databasen _bookstore_
Databasen _bookstore_ finns lagrad i backup-filen _BjornWinterfjord.bak_. Databasen är upplagd som en bokhandel i miniatyr, med ett fåtal böcker, skrivna av ett fåtal författare som säljs i ett fåtal bokhandlar inom samma koncern.
- I undermappen _Database Diagrams_ finns ett ER-diagram som visar hur databasens olika tabeller är länkade till varandra.
- Filen _bookstore.sql_ visar hur databasens tabeller och innehåll har skapats. I slutet av filen visas även hur den speciella vyn _TitlarPerForfattare_ har valts ut. Här framgår det totala lagervärdet för böckerna i bokhandlar, räknat per författare. 
### Sökning i databasen
För att som användare kunna göra en enkel sökning på boktitel i databasen, körs filen _book_search.py_. (__Man kan behöva ändra servernamnet på rad 6 för att kunna köra filen!__)

Därefter skriver man in en kort söksträng, exempelvis '_ens_', och får som resultat en lista med boktitlar som innehåller '_ens_', och vilka bokhandlar som har böckerna i lager.

Programmet ansluter till databasen med hjälp av en _engine_, varefter en _query_ skickas. Programmet är skyddat mot SQL-injection genom att använda text()-parameter med kolon-formatet (:placeholder) istället för att ange söksträngen direkt i queryn.

### Kort om de olika tabellerna i databasen:
- Den viktigaste tabellen är _bocker_. Som primärnyckel har använts ISBN13-numret, eftersom detta är världsunikt för varje bok. I tabellen kan man dessutom (förutom bokens titel) få information om dess författare, språk, pris och utgivningsdatum.
- Eftersom vi har en _many-to-many_-relation mellan _bocker_ och _genrer_ (varje bok kan tillhöra flera genrer, och varje genre kan omfatta flera böcker), gjordes en separat tabell med _genre-ID_, och en _bok_genre_-tabell som länkade vaje bok till en eller flera genrer (och varje genre till en eller flera böcker).
- Information om varje författare (Förnamn, Efternamn och födelsedatum) lagrades också i en separat tabell (_forfattare_) som länkades till _bocker_ via _ForfattareID_.
- Varje kund som lagt en order hamnar förstås i butikens databas, närmare bestämt i tabellen _kunder_, med information om adress och telefonnummer. Varje kund kan ha lagt en eller flera _ordrar_ som kopplas till kunden via KundId.
- Ordrarna är också länkade till _bocker_-tabellen via tabellen _orderdetaljer_. Varje kund kan ha gjort flera ordrar, varje order kan ha innehållit flera böcker, från flera olika butiker, och varje bok kan ha beställts i flera olika ordrar. Detta sammanfattas i den omfattande _many-to-many_-tabellen _orderdetaljer_.
- Slutligen finns tabellen _butiker_, med namn och adress, och en tabell med _lagersaldo_ för varje bok och varje butik. Detta är kopplat till _bocker_ via ISBN13-numret, och till _butiker_ via _ButikID_.

Därutöver finns den separata vyn _TitlarPerForfattare_ som skapats med ett enkelt SELECT-kommando. Här ser man lagervärdet för varje författare, det vill säga det totala värdet av samtliga författarens böcker som finns i lager i någon av de fyra butikerna.

### Testdata i databasen
Databasen ska endast efterlikna en bokhandel(-koncern) i miniatyr, och innehåller därför endast ett fåtal testdata:
- 7 författare (som skrivit 1-3 böcker vardera)
- 12 boktitlar
- 5 litteraturgenrer
- 4 butiker
- 3 kunder

För den som vill använda _book_search_ och vill vara säker på att få någon träff, kan det vara bra att veta att följande titlar ingår i databasen: _And then there were none_, _Hodejegerne_, _Raskens_, _En man som heter Ove_, _Stenhuggaren_, _Madicken_, _De ensamma_, _Mästerdetektiven Blomkvist_, _The murder of Roger Ackroyd_, _Carambole_ och _Fallet G_.
