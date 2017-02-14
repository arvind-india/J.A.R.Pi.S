class Konto(object):
    def __init__(self, inhaber, kontonummer,
                 kontostand,
                 kontokorrent=0):
        self.Inhaber = inhaber
        self.Kontonummer = kontonummer
        self.Kontostand = kontostand
        self.Kontokorrent = kontokorrent

    def ueberweisen(self, ziel, betrag):
        if (self.Kontostand - betrag < -self.Kontokorrent):
            # Deckung nicht genuegend
            return False
        else:
            self.Kontostand -= betrag
            ziel.Kontostand += betrag
            return True

    def einzahlen(self, betrag):
        self.Kontostand += betrag

    def auszahlen(self, betrag):
        self.Kontostand -= betrag

    def kontostand(self):
        return self.Kontostand