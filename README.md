# Analiza jakości powietrza w polskich miastach

Projekt SkillBridge (L1): trendy PM2.5 i PM10 w Warszawie, Krakowie i Wrocławiu
na danych pomiarowych GIOŚ (portal dane.gov.pl).

## Źródło danych

Publiczne API GIOŚ v1 (`https://api.gios.gov.pl/pjp-api/v1/`) — bieżące pomiary
godzinowe ze stacji państwowego monitoringu środowiska. Zbiór na dane.gov.pl:
„Dane pomiarowe GIOŚ".

## Jak uruchomić

```bash
pip install pandas matplotlib requests
python pobierz_dane.py   # zaciąga pomiary → data/pomiary_surowe.csv
python analiza.py        # czyszczenie + statystyki + wykresy/
```

## Struktura

| Plik | Rola |
|---|---|
| `pobierz_dane.py` | pobranie stacji/stanowisk PM2.5+PM10 i pomiarów z API (paginacja, retry, obsługa 400 dla stanowisk bez danych) |
| `analiza.py` | czyszczenie (typy, braki, duplikaty), agregacja per miasto, statystyki, wykresy |
| `data/pomiary_surowe.csv` | surowy zrzut pomiarów (560 wierszy w badanym oknie) |
| `data/statystyki.csv` | statystyki opisowe per miasto × wskaźnik |
| `wykresy/` | trend PM2.5 + porównanie średnich między miastami |
| `wnioski.md` | interpretacja wyników i ograniczenia |

## Najważniejsze ustalenia

Szczegóły i ograniczenia w [wnioski.md](wnioski.md). W skrócie: w badanym oknie
(lipiec) stężenia są niskie względem norm, ale ranking miast jest wyraźny —
Kraków ma średnie PM2.5 ponad **2× wyższe** niż Warszawa (7,9 vs 3,6 µg/m³);
najwyższą średnią zanotował Wrocław (11,3 µg/m³), ale w przesuniętym oknie
pomiarowym — porównanie z nim traktuję orientacyjnie (szczegóły w wnioski.md).