# volby2.0
# O co jde v projektu ?
Tento skript umožňuje získat výsledky parlamentních voleb z roku 2017 pro konkretní okres<a href="https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ">z této webové stranky</a> (vyberte si okres ve sloupci Výběr obce) a uložit je do CSV souboru.
# Jak na to?
Před spušťením projektu si nainstalujte potřebné knihovny uvedené v souboru &gt; <code>requirements.txt</code>. 
Skript spustíte z příkazového řádku pomocí následujícího příkazu
</pre>
<p>
 python volbyy.py < odkaz_uzemniho_celku > < vystupni_soubor > 
</p>
Výstupem bude soubor .csv s výsledky pro daný okres.
   
# Jak to vypadá v praxi?
Například pro okres Rakovník:
1. Odkaz -> https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5205
2. Název výstupního souboru -> &gt; <code>Trutnov.csv</code>
