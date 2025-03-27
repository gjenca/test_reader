# Testovanie reader servera

## Klonovať, nie sťahovať zip

```
git clone https://github.com/gjenca/test_reader.git
```

## Čo urobiť pred testovaním

1. Je treba nainštalovať pythonovskú knižnicu `pygments`.
2. Musíte mať nainštalovanú aj knižnicu `ncurses`, ale tú takmer iste nainštalovanú máte.
3. Potrebujete nainštalovať aj príkaz `rkill`, ktorý je pravdepodobne v balíčku `pslist`

## Ako testovať hromadne všetky testy

1. Skopírujte do tohto adresára váš program a nazvite ho `reader.py`, alebo si spravte symbolický link -- to je možno šikovnejšie.
2. Spustite skript `runtests.sh`.
3. Spustia sa testy. Počkajte, kým dobehnú, pár sekúnd to trvá.
4. Vznikne súbor `results.html`, ktorý si môžete otvoriť v browseri.
5. Pre každý test máte pod linkom uvedené, čo sa posielalo a v akom stave skončil.
6. Ak bol nejaký chybový výstup (niečo padlo), chybový výstup vidíte pod linkom err.

## Spúšťanie testov z nejakého intervalu

Čakať na všetky testy zaberá čas,
ak vám to vadí, pomocou `-t` takto:
```
./runtests.sh -t 2 3
```
spustíte iba `test02` až `test10`.

## Čo robiť ak niečo nejde

Ak Vám to testovanie nejde (to znamená, padá testovanie), ozvite sa mi buď
emailom alebo napíšte issue do tohto projektu na githube a zistíme, kde je
problém.
