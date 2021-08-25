
# Sjakkbot

## Hvordan komme i gang?

### Starte sjakkboten

Først installer avhengigheter med `pip install -r requirements.txt`.
 
Du kan velge om du vil kjøre boten fra terminalen, eller kjøre den opp på Lichess sånn at du kan spille mot den der. For å starte sjakkboten i terminalen, kjør `python engine.py`. For å spille mot boten i terminalen, må du skrive fra-koordinaten fulgt av til-koordinaten, f.eks. `e2e4` for å spille bonde fra e2 til e4. Det har ikke noe å si hvilken brikke det er, så om du vil flytte springer fra g1 til f3, skriver du `g1f3`. Boten svarer på samme måte.

For å starte boten på Lichess slik at du kan spille mot den der, legg inn brukernavnet og tokenet til boten i filen `keys.py`. Så er det bare å kjøre `python lichess.py`.

Nå er det bare å logge seg på en annen Lichess-konto (du kan [opprette en her](https://lichess.org/signup)) og utfordre boten! Gå til profilen til boten på https://lichess.org/@/BRUKERNAVN, f.eks.  https://lichess.org/@/Bottios. Så klikker du på sverdikonet, velger en tidskontroll og utfordrer boten:

![](https://user-images.githubusercontent.com/1413265/130758914-6a973908-f54c-4bef-841d-0cc4facdccf4.png)

### Hvordan forbedre den 

I `evaluation.py` finner dere evalueringsfunksjonen `evaluate`. Den tar inn stillingen (noden), og returnerer en score. Siden den nå bare returnerer et tilfeldig tall, vil boten spille helt tilfeldig. Målet er å forbedre denne evalueringsfunsjonen.

Den enkleste måten å evaluerere stillingen på, er å telle opp brikkene på brettet. Legg sammen verdien på de hvite brikkene og trekk fra verdien på de svarte brikkene, så har du en verdi på stillingen.

For å hjelpe deg i gang, skal vi vise hvordan du kan gjøre en slik brikkeopptelling. Men først en forklaring av variabelen `node`, som representerer stillingen. Dere kan se på `node` som selve sjakkbrettet med alle brikkene på. Vi bruker biblioteket `python-chess` for å representere brettet og generere lovlige trekk, og `node` kommer fra denne pakken, der den er av typen Board.

Se `Board` i dokumentasjonen til `python-chess`: https://python-chess.readthedocs.io/en/latest/

Radene på et sjakkbrett går fra 1 til 8, og kolonnene går fra A til H:

![Screenshot](http://3.bp.blogspot.com/-OeoLo7bgI3s/UCSMlx1trbI/AAAAAAAAAFY/O8gCOQkZypE/s1600/annotated-chess_algebraic_naming-squares.gif)

Det er disse koordinatene vi bruker for å referere til felter på brettet. Feltet helt nede til venstre heter A1, og feltet der svarts konge starter heter E8.

For å finne ut hvilken brikke som står på A1, kan vi skrive `piece = node.piece_at(chess.A1)` (og `chess.A1` kan skrives `get_attr(chess, "A1")`). Da vil `piece` inneholde brikken dersom det står en brikke der, ellers `None`. Hvite brikker har store bokstaver, mens svarte brikker har små. En hvit bonde vil være `P`, mens en svart konge vil være `k`.

Bonde: P, Løper: B, Springer: N, Tårn: R, Dronning: Q, Konge: K.

`fields`-variabelen i `evaluation.py` er en liste med alle feltene på brettet: `['A1', 'A2', ..., 'H8']`. Så ved å loope gjennom denne listen kan man legge til eller trekke fra en score basert på hvilken brikke som står på feltet.

Vanligvis brukes disse verdiene på brikkene: Bonde: 1, løper og springer: 3, tårn: 5, dronning 9. Så kan man sette en verdi på kongen som er mye høyere enn alle de andre til sammen, f.eks. 100. For å kunne justere verdiene mer nøyaktig, pleier man å oppgi verdier i "centipawns", altså hundredeler av bondeverdien. Da blir verdiene 100 for bonde, 300 for løper, osv... Finn mer informasjon om brikkeverdier på https://www.chessprogramming.org/Point_Value

For eksempel:

```
def evaluate(node):
    score = 0

    for field in fields:
        piece = node.piece_at(getattr(chess, field))

        if piece:
            p = str(piece)

            if p == "P":
                score += 100
            elif p == "p":
                score -= 100
            elif p == "B":
                score += 300
        # osv...

    return score
```

Så kan dere jo prøve å justere på verdiene for å se om den blir bedre. Det er for eksempel kjent at det er en fordel å ha løperparet (begge løperne), så man kan prøve å gi en ekstra score for dette. [En halv bonde](https://www.chessprogramming.org/Bishop_Pair) er ofte foreslått.

### Piece-Square Tables

For å tildele brikkene verdier basert på hvor på brettet de står, brukes [piece-square tables](https://www.chessprogramming.org/Piece-Square_Tables). I `evaluation`-mappa ligger det tabeller med verdier for alle brikkene, så om dere får tid kan dere prøve å bruke disse for å gjøre den enda bedre.
