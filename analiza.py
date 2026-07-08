"""Analiza trendów PM2.5 i PM10 w Warszawie, Krakowie i Wrocławiu.

Wejście: data/pomiary_surowe.csv (z pobierz_dane.py).
Czyszczenie: konwersja typów (data → datetime, wartość → float), usunięcie
braków (API zwraca null dla niezweryfikowanych godzin) i duplikatów
(miasto+stacja+wskaźnik+data). Agregacja: średnia godzinowa per miasto
(uśredniamy stacje w mieście, żeby porównywać miasta, nie stacje).
Wyjście: wykresy/trend_pm25.png, wykresy/porownanie_srednich.png + statystyki.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def wczytaj_i_wyczysc(sciezka: str = "data/pomiary_surowe.csv") -> pd.DataFrame:
    df = pd.read_csv(sciezka)
    przed = len(df)

    # Typy: API oddaje wszystko tekstem; wartości bywają puste (null → NaN).
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["wartosc"] = pd.to_numeric(df["wartosc"], errors="coerce")

    # Braki: pomiar bez wartości albo bez czasu jest bezużyteczny do trendu.
    df = df.dropna(subset=["data", "wartosc"])

    # Duplikaty: ta sama godzina z tej samej stacji nie może liczyć się podwójnie.
    df = df.drop_duplicates(subset=["miasto", "stacja", "wskaznik", "data"])

    po = len(df)
    print(f"Czyszczenie: {przed} → {po} wierszy (usunięto {przed - po}: braki/duplikaty)")
    return df


def srednia_miejska(df: pd.DataFrame) -> pd.DataFrame:
    """Średnia godzinowa per miasto i wskaźnik (uśrednienie stacji w mieście)."""
    return df.groupby(["miasto", "wskaznik", "data"], as_index=False)["wartosc"].mean()


def wykres_trendu_pm25(df: pd.DataFrame) -> None:
    pm25 = df[df["wskaznik"] == "pył zawieszony PM2.5"]
    fig, ax = plt.subplots(figsize=(11, 5))
    for miasto, grupa in pm25.groupby("miasto"):
        ax.plot(grupa["data"], grupa["wartosc"], label=miasto, linewidth=1.4)
    ax.axhline(15, color="red", linestyle="--", linewidth=1, label="norma dobowa WHO (15 µg/m³)")
    ax.set_title("PM2.5 — średnia godzinowa ze stacji w mieście")
    ax.set_ylabel("µg/m³")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig("wykresy/trend_pm25.png", dpi=120)
    print("Zapisano wykresy/trend_pm25.png")


def wykres_porownania(df: pd.DataFrame) -> None:
    srednie = df.groupby(["miasto", "wskaznik"])["wartosc"].mean().unstack()
    fig, ax = plt.subplots(figsize=(8, 5))
    srednie.plot.bar(ax=ax, rot=0)
    ax.set_title("Średnie stężenie w badanym oknie — porównanie miast")
    ax.set_ylabel("µg/m³")
    fig.tight_layout()
    fig.savefig("wykresy/porownanie_srednich.png", dpi=120)
    print("Zapisano wykresy/porownanie_srednich.png")


def statystyki(df: pd.DataFrame) -> None:
    opis = df.groupby(["miasto", "wskaznik"])["wartosc"].agg(["count", "mean", "median", "max"])
    opis = opis.round(1)
    print("\nStatystyki opisowe (µg/m³):")
    print(opis.to_string())
    opis.to_csv("data/statystyki.csv")


def main() -> None:
    df = wczytaj_i_wyczysc()
    df_miasta = srednia_miejska(df)
    statystyki(df_miasta)
    wykres_trendu_pm25(df_miasta)
    wykres_porownania(df_miasta)


if __name__ == "__main__":
    main()
