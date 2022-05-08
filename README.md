# Testovanie reader servera

## Čo urobiť pred testovaním

1. Pred použitím musíte nainštalovať knižnicu `pyyaml`, ktorá sa možno volá vo Vašej distribúcii
   inak, možno `python3-yaml` alebo tak nejako.
2. Takisto je treba nainštalovať pythonovskú knižnicu `pygments`.
3. Musíte mať nainštalovanú aj knižnicu `ncurses`, ale tú takmer iste nainštalovanú máte.

## Ako testovať hromadne všetky testy

1. Skopírujte do tohto adresára váš program a nazvite ho `reader.py`.
2. Spustite skript `runtests.sh`.
3. Spustia sa testy. Počkajte, kým dobehnú, pár sekúnd to trvá.
4. Vznikne súbor `results.html`, ktorý si môžete otvoriť v browseri.
5. Pre každý test máte pod linkom uvedené, čo sa posielalo a v akom stave skončil.
6. Ak bol nejaký chybový výstup (niečo padlo), chybový výstup vidíte pod linkom err.

## Čo robiť ak niečo nejde

Ak Vám to testovanie nejde, ozvite sa mi buď emailom alebo napíšte issue do tohto projektu na githube zistíme, kde je problém.
