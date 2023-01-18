# Zufällige Schatzsuche
from random import randint
from schatz_gui import SchatzGUI


def search_schatz(n):
    ich = [0,0]
    schatz = [randint(0,n-1),randint(0,n-1)]
    schritte = ["nord", "ost", "süd", "west"]
    pfad = [ich.copy()]
    while ich != schatz:
        schritt = randint(0,3)
        if schritt == 0:
            ich[1] = ich[1] + 1
            if ich[1] >= n:
                ich[1] = 0
        elif schritt == 1:
            ich[0] = ich[0] + 1
            if ich[0] >= n:
                ich[0] = 0
        elif schritt == 2:
            ich[1] = ich[1] - 1
            if ich[1] < 0:
                ich[1] = n-1
        elif schritt == 3:
            ich[0] = ich[0] - 1
            if ich[0] < 0:
                ich[0] = n-1
        pfad.append(ich.copy())
    return pfad, schatz


SchatzGUI(search_schatz).start()