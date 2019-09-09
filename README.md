# python3tasks
Coding solutions for 3 tasks writen in Python

1. Task

Koristeći standardne python biblioteke napraviti više procesni sustav koji se sastoji od tri procesa (hint: naslijediti multiprocessing.Process).
1. proces - spava 5 sekundi, ispiše &quot;Proces 1&quot;, ponavlja u nedogled
2. proces - spava 100 ms, ispisuje &quot;Proces 2&quot;, ponavlja se u nedogled
3. proces - spava 2 sekunde, ispisuje &quot;Proces 3&quot;, ponavlja se u nedogled
Sav ispis se mora izvršavati kroz logger modul te se ispis mora izvršavati u centralni log i pojedinačni log za svaki proces.
VAŽNO: Redoslijed ispisa nije važan, ali se ispis jednog procesa ne smije ponavljati dok ostali ne ispišu (hint: multiprocessing.Lock). Primjer:

Točno:....................Krivo:

Proces 2....................Proces 2

Proces 3....................Proces 2

Proces 1....................Proces 2

Proces 2....................Proces 2

Proces 3....................Proces 3

Proces 1....................Proces 2


2. Task

Koristeći python psycopg2 modul i postgresql bazu postići interprocesnu komunikaciju.
Sustav se sastoji od dva procesa i postgresql tablice. Tablica naziva "poruke" se sastoji od dva polja, proces_id i poruka.
1. proces
- provjera tablice &quot;poruke&quot; za poruke čiji je proces_id jednak 2
- ukoliko poruka sadrži slovo &#39;a&#39; ispisati pročitanu poruku
- ukoliko poruka ne sadrži slovo &#39;a&#39; ispisati &quot;pročitana poruka ne sadrži slovo a&quot;
- ukoliko poruka nije pronađena ispisati &quot;poruka nije pronađena&quot;
- svake 3 sekunde upisati nasumičnu poruku od 5 slova i svaki 3 upis osigurati da poruka sadržava slovo &#39;b&#39;, proces_id je 1
- proces spava pola sekunde prije slijedećeg ponavljanja, ponavlja se u nedogled
2. proces
- provjera tablice &quot;poruke&quot; za poruke čiji je proces_id jednak 1
- ukoliko poruka sadrži slovo &#39;b&#39; ispisati pročitanu poruku
- ukoliko poruka ne sadrži slovo &#39;b&#39; ispisati &quot;pročitana poruka ne sadrži slovo b&quot;
- ukoliko poruka nije pronađena ispisati &quot;poruka nije pronađena&quot;
- svake 3 sekunde upisati nasumičnu poruku od 5 slova i svaki 3 upis osigurati da poruka sadržava slovo &#39;a&#39;, proces_id je 2

- proces spava pola sekunde prije slijedećeg ponavljanja, ponavlja se u nedogled
Sav ispis se mora izvršavati kroz logger modul i ispis se mora izvršavati u centralni log i pojedinačni log za svaki proces.


3. Task

Isti kao zadatak 2, ali umjesto interprocesne komunikacije kroz postgresql odabrati neki
drugi način interprocesne komunikacije koji nije baza podataka.


4. Task

Koristeći python Flask napraviti HTTP endpoint koji vraća sadržaj gore navedene tablice poruke.
