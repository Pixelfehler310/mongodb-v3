# Leitfaden: Demo-Projekt fuer Praesentation und Live-Nutzung

## 1. Rolle dieses Projekts

Das Demo-Projekt ist das didaktische Showcase-Artefakt der Seminararbeit. Es soll MongoDB sichtbar, erklaerbar und praesentierbar machen. Es soll nicht die wissenschaftliche Hauptbeweisfuehrung tragen.

Die Leitdokumente dafuer sind:

- `DEMO_PROJECT_REQUIREMENTS.md`
- `SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md`
- `README_mongodb_demo.md`

Die umgesetzte Anwendung liegt in `mongodb_demo/`.

## 2. Was du mit dem Demo zeigen sollst

Das Demo ist dann erfolgreich, wenn ein Publikum in wenigen Minuten versteht:

1. warum ein Produkt in MongoDB als gut lesbares Dokument modelliert werden kann,
2. wie mehrere Produkttypen in einer Collection zusammenleben,
3. wie Filter auf gemeinsame, verschachtelte und Array-Felder wirken,
4. wie dieselbe UI-Aktion zu einer MongoDB-Query und zu passendem PyMongo-Code fuehrt,
5. wie einfache Aggregationen erklaert werden koennen,
6. wie Schema-Evolution am Feld `regionalTaxCode` sichtbar wird.

## 3. Was du mit dem Demo ausdruecklich nicht zeigen sollst

Das Demo ist nicht dafuer da, Aussagen zu beweisen ueber:

- SQL vs. MongoDB als fairen Vergleich,
- Performance oder Benchmarking,
- statistische Signifikanz,
- allgemeine wissenschaftliche Ueberlegenheit von MongoDB.

Kurzregel: Das Demo erklaert, das Testprojekt belegt.

## 4. Empfohlene Lesereihenfolge

Wenn du das Projekt inhaltlich schnell verstehen willst, lies in dieser Reihenfolge:

1. `DEMO_PROJECT_REQUIREMENTS.md`
2. `SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md`
3. `README_mongodb_demo.md`
4. `mongodb_demo/README.md`
5. `mongodb_demo/DEMO_SCOPE.md`
6. `mongodb_demo/DEMO_FLOW.md`

Danach erst lohnt sich der Blick in den Code.

## 5. Wie das Projekt gelesen werden soll

Die wichtigste Struktur in `mongodb_demo/` ist:

- `backend/`: Flask-API, Query-Aufbereitung, Repository-Zugriffe, Serialisierung.
- `frontend/`: praesentationsorientierte React/Vite-Oberflaeche.
- `scripts/`: Seed- und Reset-Helfer fuer reproduzierbare Demo-Zustaende.
- `tests/`: Absicherung der Query-Logik und Seed-Daten.

Fachlich ist die zentrale Kette weiterhin einfach:

`Browser UI -> Flask API -> PyMongo Repository -> MongoDB`

Die aktuelle React/Vite-Implementierung ist fuer die Seminarlogik zweitrangig. Entscheidend ist nicht das UI-Framework, sondern dass Query, Dokumentansicht, Filter und Aggregation klar und stabil erklaert werden koennen.

## 6. Praktische Nutzung vor der Praesentation

Der zuverlaessigste Startpfad ist der Container-Start:

```powershell
cd mongodb_demo
docker compose up --build
```

Danach gelten diese Zieladressen:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`
- MongoDB: `mongodb://localhost:27117/`

Sinnvolle Kurzchecks vor dem Vortrag:

1. `http://localhost:5000/api/health` liefert `ok: true`.
2. Die Produktliste zeigt mehrere Produkttypen.
3. Das Auswaehlen eines Produkts laedt das JSON-Dokument.
4. Die Aggregationsansicht zeigt Zeilen statt eines leeren Zustands.
5. Der Sample-Insert funktioniert oder ist vorab bewusst deaktiviert.

Wenn du den Datenzustand vor einer Probe oder vor dem eigentlichen Vortrag neu aufsetzen willst, nutze in `mongodb_demo/`:

```powershell
python scripts/reset_demo.py
```

oder den Alias:

```powershell
npm run reset
```

## 7. Empfohlener Live-Demo-Ablauf

Der robuste Standardpfad ist:

1. Starte mit der Produktliste und betone: eine Collection, mehrere Produkttypen.
2. Waehle ein konkretes Produkt, idealerweise einen Laptop, und zeige gemeinsame Felder plus `attributes`.
3. Zeige die eingebetteten Bereiche wie `categories`, `variants` und `latestReviews`.
4. Wechsle zur Query-Anzeige und erklaere den aktuellen `find`-Pfad.
5. Wechsle zur PyMongo-Anzeige und verbinde UI, Query und Anwendungscode.
6. Setze danach 2 bis 3 Filter, zum Beispiel `productType`, RAM und `regionalTaxCode`-Vorhandensein.
7. Zeige, dass Ergebnisliste, Query-Text und Code gleichzeitig kippen.
8. Oeffne die Aggregationen und zeige zuerst Durchschnittspreis pro Produkttyp, danach Produktanzahl pro Kategorie.
9. Wenn die Live-Situation stabil ist, fuehre den Sample-Insert aus und zeige das neue Dokument als Schema-Evolutionsbeispiel.

Die Reihenfolge ist wichtig: erst Dokument, dann Query, dann Filter, dann Aggregation, dann Evolution.

## 8. Wie die Praesentation darum gebaut werden sollte

Eine gute Seminarpraesentation behandelt das Demo nicht als Hauptteil, sondern als Sichtbarmachung der spaeteren Argumente.

Ein belastbarer Aufbau fuer einen kurzen Vortrag ist:

1. Problemrahmen: Warum ist die Wahl zwischen relationalem und dokumentenorientiertem Modell fachlich relevant?
2. Trennung der Artefakte: `mongodb_demo/` erklaert, `metrics-quantification/` misst.
3. Gemeinsame Domaene: polymorpher Produktkatalog als roter Faden.
4. Kurze Architekturfolie: Browser, Flask, PyMongo, MongoDB.
5. Live-Demo entlang des Standardpfads aus Abschnitt 7.
6. Rueckbindung: Was die Demo sichtbar gemacht hat und welche Fragen dadurch fuer den wissenschaftlichen Vergleich entstehen.
7. Uebergang zum Testprojekt: Datenlokalitaet, Denormalisierung, Join-/Lookup-Spannung, Schema-Evolution.

Wenn die Praesentation zeitlich knapp ist, sollte das Demo eher kurz und kontrolliert bleiben. Drei bis fuenf Minuten fokussierte Live-Demo sind methodisch staerker als ein laengeres Herumklicken ohne klare Aussage.

## 9. Sprechlogik waehrend der Demo

Die staerkste Erzaehlung ist nicht "hier ist eine App", sondern:

1. "Hier ist ein fachlich gut lesbares Dokument."
2. "Hier sieht man, wie Polymorphie ohne Tabellenaufspaltung sichtbar wird."
3. "Hier sieht man, wie ein Filter direkt zur Query wird."
4. "Hier sieht man, wie dieselbe Collection auch Aggregationen tragen kann."
5. "Hier sieht man, warum Schema-Flexibilitaet spaeter wissenschaftlich interessant wird."

Damit bleibt die Demo eng an der Forschungsfrage statt an Oberflaechendetails.

## 10. Fallback-Strategie fuer die Praesentation

Wenn die Live-Demo instabil wird, sollte die fachliche Aussage nicht zusammenbrechen. Deshalb gilt:

1. Halte die Startseite vor dem Vortrag bereits offen.
2. Halte einen Beispielpfad bereit: Liste, Detailansicht, Query, Aggregation.
3. Nutze den Insert nur, wenn der Rest schon stabil laeuft.
4. Verlasse dich nie darauf, spontan neue Datenkonstellationen zu suchen.

Die Seminarleistung entsteht nicht durch Live-Risiko, sondern durch Klarheit der Erklaerung.

## 11. Wie das Demo in die Seminararbeit eingeordnet werden sollte

In der schriftlichen Arbeit hat das Demo eine unterstuetzende Rolle:

- als motivierendes Beispiel fuer die Produktkatalog-Domaene,
- als Visualisierung von Dokumentstruktur und Filterlogik,
- als Bruecke zur spaeteren Diskussion ueber Datenlokalitaet, Denormalisierung und Evolution.

Es sollte aber nicht als primaere Ergebnisquelle in den Ergebnis- oder Interpretationskapiteln verwendet werden. Diese Rolle gehoert dem wissenschaftlichen Testprojekt.
