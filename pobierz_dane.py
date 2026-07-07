"""Pobranie danych o jakości powietrza z API GIOŚ (v1).

Źródło: https://api.gios.gov.pl/pjp-api/v1/ (portal dane.gov.pl, zbiór GIOŚ).
Skrypt: znajduje stacje w wybranych miastach, wybiera stanowiska PM2.5 i PM10,
pobiera pomiary godzinowe i zapisuje surowe dane do data/pomiary_surowe.csv.
"""

import csv
import time

import requests

BASE = "https://api.gios.gov.pl/pjp-api/v1/rest"
MIASTA = ["Warszawa", "Kraków", "Wrocław"]
WSKAZNIKI = {"pył zawieszony PM2.5", "pył zawieszony PM10"}


def pobierz_json(url: str) -> dict:
    """GET z prostym ponowieniem — API publiczne bywa chwilowo przeciążone."""
    for proba in range(3):
        try:
            odp = requests.get(url, timeout=20)
            odp.raise_for_status()
            return odp.json()
        except requests.RequestException:
            if proba == 2:
                raise
            time.sleep(2 * (proba + 1))
    raise RuntimeError("nieosiągalne")


def znajdz_stacje() -> list[dict]:
    """Wszystkie stacje pomiarowe (paginacja API), przefiltrowane po miastach."""
    stacje = []
    strona = 0
    while True:
        dane = pobierz_json(f"{BASE}/station/findAll?page={strona}&size=500")
        lista = dane.get("Lista stacji pomiarowych", [])
        if not lista:
            break
        stacje.extend(lista)
        if strona >= int(dane.get("totalPages", 1)) - 1:
            break
        strona += 1
    return [s for s in stacje if s.get("Nazwa miasta") in MIASTA]


def stanowiska_pm(stacja_id: int) -> list[dict]:
    dane = pobierz_json(f"{BASE}/station/sensors/{stacja_id}")
    lista = dane.get("Lista stanowisk pomiarowych dla podanej stacji", [])
    return [s for s in lista if s.get("Wskaźnik") in WSKAZNIKI]


def pomiary(stanowisko_id: int) -> list[dict]:
    # API odpowiada 400 dla stanowisk bez bieżących danych (np. serwisowanych)
    # — traktujemy jak pustą listę zamiast wywracać cały zaciąg.
    try:
        dane = pobierz_json(f"{BASE}/data/getData/{stanowisko_id}")
    except requests.HTTPError as blad:
        if blad.response is not None and blad.response.status_code == 400:
            return []
        raise
    return dane.get("Lista danych pomiarowych", [])


def main() -> None:
    wiersze = []
    for stacja in znajdz_stacje():
        miasto = stacja["Nazwa miasta"]
        stacja_id = stacja["Identyfikator stacji"]
        for stanowisko in stanowiska_pm(stacja_id):
            wskaznik = stanowisko["Wskaźnik"]
            for pomiar in pomiary(stanowisko["Identyfikator stanowiska"]):
                wiersze.append(
                    {
                        "miasto": miasto,
                        "stacja": stacja.get("Nazwa stacji", ""),
                        "wskaznik": wskaznik,
                        "data": pomiar.get("Data"),
                        "wartosc": pomiar.get("Wartość"),
                    }
                )
            time.sleep(0.3)  # nie zalewamy publicznego API

    with open("data/pomiary_surowe.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["miasto", "stacja", "wskaznik", "data", "wartosc"])
        writer.writeheader()
        writer.writerows(wiersze)
    print(f"Zapisano {len(wiersze)} pomiarów do data/pomiary_surowe.csv")


if __name__ == "__main__":
    main()
