# Wnioski z analizy

Okno badania: bieżące pomiary godzinowe z API GIOŚ (ok. 2 doby wstecz od
uruchomienia zaciągu, lipiec 2026). Po czyszczeniu: 502 z 560 pomiarów
(58 usunięte — puste wartości niezweryfikowanych godzin i duplikaty stacji).

## 1. Ranking miast jest wyraźny nawet latem

Średnie PM2.5 (µg/m³, uśrednione stacje w mieście): **Wrocław 11,3 · Kraków
7,9 · Warszawa 3,6**. Uwaga: okno pomiarowe Wrocławia jest przesunięte
względem pozostałych miast (patrz ograniczenia), więc bezpośrednio porównywać
można Kraków z Warszawą — i tu różnica jest ponad dwukrotna przy tej samej
pogodzie wyżowej. To spójne z literaturą o krakowskiej niecce i emisji
komunikacyjnej.

## 2. Poziomy są niskie względem norm — sezon ma znaczenie

Maksimum godzinowe PM2.5 w całym oknie to 17,6 µg/m³ (Wrocław) — poniżej
polskiej normy dobowej i w okolicy dobowej wytycznej WHO (15 µg/m³). Lipcowe
dane NIE mówią nic o sezonie grzewczym, w którym te same miasta potrafią
przekraczać normy wielokrotnie; to analiza „najlepszego przypadku".

## 3. PM10 podąża za PM2.5

Tam, gdzie mamy oba wskaźniki (Kraków, Warszawa), ranking PM10 powtarza
ranking PM2.5 (15,4 vs 6,7 µg/m³) — sugeruje wspólne źródła w tym oknie
(transport, wtórna emisja), nie epizod pyłu grubego.

## Ograniczenia (świadome)

1. **Krótkie okno** — API v1 `getData` oddaje tylko bieżące ~2 doby; trend
   sezonowy wymagałby archiwum (osobny zbiór na dane.gov.pl).
2. **Luka PM10 we Wrocławiu** — stanowiska PM10 zwracały w oknie zaciągu 400
   (brak bieżących danych); analiza PM10 opiera się na Krakowie i Warszawie.
   Z tego samego powodu okno czasowe Wrocławia dla PM2.5 różni się od
   pozostałych miast — porównanie z Wrocławiem traktuję orientacyjnie.
3. **Uśrednienie stacji** — średnia miejska maskuje różnice tła vs komunikacja;
   przy dłuższym oknie warto rozdzielić typy stacji.
4. **Korelacja ≠ przyczyna** — ranking miast opisuje stan, nie mechanizm;
   bez danych meteo nie rozdzielę emisji od warunków rozpraszania.
