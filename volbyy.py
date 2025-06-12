import sys
import csv
import requests
from bs4 import BeautifulSoup

SLEDOVANE_STRANY = {
    "Občanská demokratická strana": "ODS",
    "Česká str.sociálně demokrat.": "ČSSD",
    "Komunistická str.Čech a Moravy": "KSČM",
    "ANO 2011": "ANO 2011",
    "Svob.a př.dem.-T.Okamura (SPD)": "SPD",
    "Česká pirátská strana": "Piráti",
    "CESTA ODPOVĚDNÉ SPOLEČNOSTI": "COS",
    "Radostné Česko": "Rado. Č.",
    "STAROSTOVÉ A NEZÁVISLÍ": "STAN",
    "Strana zelených": "Zelený",
    "ROZUMNÍ-stop migraci,diktát.EU": "ROZUMNÍ",
    "Strana svobodných občanů": "SSO",
    "Blok proti islam.-Obran.domova": "BPI",
    "Občanská demokratická aliance": "ODA",
    "Referendum o Evropské unii": "EU referendum",
    "TOP 09": "TOP 09",
    "Dobrá volba 2016": "DB 2016",
    "SPR-Republ.str.Čsl. M.Sládka": "SPR",
    "Křesť.demokr.unie-Čs.str.lid.": "Křesťaní",
    "Česká strana národně sociální": "ČSNS",
    "REALISTÉ": "REALIST",
    "SPORTOVCI": "SPORT",
    "Dělnic.str.sociální spravedl.": "DSSS",
    "Strana Práv Občanů": "SPO"
}


def nacti_obce(hlavni_odkaz):
    zaklad_url = "https://volby.cz/pls/ps2017nss/"
    odpoved = requests.get(hlavni_odkaz)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    obce = []
    for radek in soup.select("tr"):
        cislo_td = radek.select_one("td.cislo a")
        nazev_td = radek.select_one("td.overflow_name")

        if cislo_td and nazev_td:
            kod = cislo_td.text.strip()
            nazev = nazev_td.text.strip()
            obec_url = zaklad_url + cislo_td["href"]
            obce.append((kod, nazev, obec_url))
    return obce


def ziskej_data_z_obce(url_obce):
    odpoved = requests.get(url_obce)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    def vycisti(td): return td.text.strip().replace("\xa0", "")

    volici = vycisti(soup.find("td", headers="sa2"))
    obalky = vycisti(soup.find("td", headers="sa3"))
    platne = vycisti(soup.find("td", headers="sa6"))

    vysledky = {zkr: "0" for zkr in SLEDOVANE_STRANY.values()}

    strany_td = soup.find_all("td", class_="overflow_name")
    hlasy_td = soup.find_all("td", headers=lambda h: h and "t1sa2" in h)

    for strana_td, hlas_td in zip(strany_td, hlasy_td):
        jmeno = strana_td.text.strip()
        if jmeno in SLEDOVANE_STRANY:
            zkr = SLEDOVANE_STRANY[jmeno]
            vysledky[zkr] = vycisti(hlas_td)

    return volici, obalky, platne, vysledky


def uloz_do_csv(data, nazev_souboru, hlavicka):
    with open(nazev_souboru, mode="w", newline="", encoding="utf-8") as vystup:
        zapisovac = csv.writer(vystup)
        zapisovac.writerow(hlavicka)
        zapisovac.writerows(data)


def main():
    if len(sys.argv) != 3:
        print("Použití: python volby2017.py <URL> <vystup.csv>")
        sys.exit(1)

    vstupni_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    print("➡Načítá se seznam obcí...")
    seznam_obci = nacti_obce(vstupni_url)
    print(f"Nalezeno {len(seznam_obci)} obcí")

    zkratky = list(SLEDOVANE_STRANY.values())
    vystupni_data = []

    for kod, nazev, url in seznam_obci:
        volici, obalky, platne, strany_data = ziskej_data_z_obce(url)
        radek = [kod, nazev, volici, obalky, platne] + [strany_data[z] for z in zkratky]
        vystupni_data.append(radek)

    hlavicka = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + zkratky

    print("Ukládám výsledky...")
    uloz_do_csv(vystupni_data, vystupni_soubor, hlavicka)

    print(f"Výstupní soubor vytvořen: {vystupni_soubor}")


if __name__ == "__main__":
    main()
