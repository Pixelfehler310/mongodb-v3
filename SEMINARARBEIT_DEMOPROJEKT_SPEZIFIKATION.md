# Spezifikation: Demo-Projekt fuer eine Seminararbeit

## Dokumentstatus

- Ziel: Vollstaendige Spezifikation fuer ein neues Demo-Projekt
- Projektrolle: didaktisches, praesentationsfreundliches Showcase-Projekt
- Zielrepo: `mongodb_demo`
- Status: Iteration 3 von 3
- Grundlage: aktueller Flask-/PyMongo-/Vanilla-JS-Stack, neue fachliche Ausrichtung

## Revisionsnotizen dieser Iteration

- Iteration 1: fachliche und technische Neuausrichtung auf den Produktkatalog gesetzt
- Iteration 2: API-Contracts, Seed-Regeln, UI-Zustaende und Abnahme geschaerft
- Iteration 3: Beispieldokumente, Startregeln, Live-Demo-Abnahme und Nutzbarkeit finalisiert

---

## 1. Zweck des Projekts

Dieses Projekt ist das visuelle und interaktive Demo-Artefakt einer Seminararbeit im Masterstudium. Es soll MongoDB anhand eines fachlich sinnvollen Beispiels verstaendlich erklaeren, ohne die wissenschaftliche Benchmark-Logik nachzubauen.

Das Projekt ist kein zweites Benchmark-System, kein vollstaendiger Shop und kein Produktivfrontend. Es ist eine kleine, robuste und praesentationsstarke Anwendung, die Dokumentstruktur, Query-Logik und Aggregationen erklaerbar macht.

---

## 2. Ziel des Demo-Projekts

Das Demo-Projekt soll einem Publikum in wenigen Minuten zeigen:

1. wie ein realistisches MongoDB-Dokument aussieht,
2. wie verschachtelte Daten, Arrays und polymorphe Felder gespeichert werden,
3. wie UI-Filter in MongoDB-Queries uebersetzt werden,
4. wie passende PyMongo-Aufrufe aussehen,
5. wie einfache Aggregationen in MongoDB funktionieren,
6. wie Schema-Flexibilitaet anschaulich erklaert werden kann.

---

## 3. Nicht-Ziele

Das Demo-Projekt soll explizit nicht leisten:

- fairen SQL-vs.-MongoDB-Vergleich,
- quantitative Lastmessung,
- Multi-User-Faehigkeit,
- Authentifizierung,
- Admin-Oberflaechen,
- vollstaendiges CRUD fuer alle Entitaeten,
- Produktionshaertung,
- Microservice- oder Eventing-Architektur.

---

## 4. Technologischer Zielrahmen

Das Demo-Projekt soll dem aktuellen technischen Charakter moeglichst aehnlich bleiben.

## 4.1 Backend

- Python 3.11+
- Flask
- PyMongo
- python-dotenv

## 4.2 Frontend

- HTML
- CSS
- Vanilla JavaScript

## 4.3 Betrieb lokal

- MongoDB lokal via Docker Compose
- Seed-Skript in Python
- Webserver lokal ueber Flask

## 4.4 Nicht verwenden

- React
- Vite
- FastAPI
- TypeScript als Hauptstack des Demos
- SSR-Frameworks
- externe UI-Bibliotheken ohne klaren Mehrwert

---

## 5. Fachliche Domaene des Demo-Projekts

Die Domaene soll mit dem wissenschaftlichen Hauptprojekt konsistent sein und ebenfalls auf einem polymorphen Produktkatalog beruhen.

## 5.1 Grundidee

Das Publikum sieht eine Liste von Produkten aus verschiedenen Produkttypen und kann erkunden, wie sich gemeinsame und typspezifische Felder in MongoDB als Dokumente darstellen.

## 5.2 Beispielhafte Produkttypen

- Laptop
- T-Shirt
- Buch
- Smartphone
- Schreibtisch

## 5.3 Beispielhafte gemeinsame Felder

- `_id`
- `productId`
- `sku`
- `productType`
- `name`
- `basePrice`
- `currency`
- `manufacturer`
- `categories`
- `createdAt`
- `updatedAt`

## 5.4 Beispielhafte eingebettete Bereiche

- `attributes`
- `variants`
- `highlights`
- `latestReviews`
- `shipping`

## 5.5 Beispielhafte optionale Evolutionsfelder

- `regionalTaxCode`
- `compliance`
- `marketAvailability`

---

## 6. Zentrale Demo-Botschaft

Die Anwendung soll nicht moeglichst viel zeigen, sondern wenige Kernideen sehr klar.

Diese Kernideen sind:

1. Ein Produkt ist in MongoDB ein fachlich gut lesbares Dokument.
2. Polymorphe Produkttypen koennen ohne komplizierte relationale Aufspaltung dargestellt werden.
3. Verschachtelte Felder und Arrays koennen direkt abgefragt werden.
4. Dieselben Filter wirken gleichzeitig auf UI, Query-Anzeige und Resultat.
5. Aggregationen koennen aus derselben Collection erklaerbar aufgebaut werden.

---

## 7. Hauptnutzerfluss der Demo

Ein Presenter soll die Anwendung in dieser Reihenfolge zeigen koennen:

1. Produktliste oeffnen.
2. Unterschiedliche Produkttypen in derselben Collection zeigen.
3. Ein Produkt auswaehlen.
4. Das komplette Dokument mit eingebetteten Bereichen erklaeren.
5. Ueber Filter die Query sichtbar veraendern.
6. Eine Aggregation aktivieren.
7. Optional ein neues Beispieldokument einfuegen.
8. Optional ein Produkt aus einer neueren Schema-Version zeigen.

---

## 8. Funktionale Anforderungen

## FR1. Produktliste

Die Anwendung muss eine Liste von Produkten anzeigen.

Die Liste muss:

- initial begrenzt sein,
- nach `updatedAt` oder `createdAt` sortiert sein,
- gemeinsame Felder kompakt anzeigen,
- den Produkttyp sichtbar machen,
- die Auswahl eines Eintrags ermoeglichen.

## FR2. Detailansicht

Die Anwendung muss das vollstaendige Produktdokument anzeigen.

Die Detailansicht muss:

- nah an der JSON-Struktur bleiben,
- eingebettete Arrays und Objekte sichtbar machen,
- typspezifische Attribute deutlich zeigen,
- Felder aus unterschiedlichen Schema-Stufen darstellbar machen.

## FR3. Filterbereich

Die Anwendung muss einen kleinen, klaren Filterbereich bieten.

Pflichtfilter:

- Produkttyp
- Hersteller
- Kategorie
- Preisbereich
- Verfuegbarkeit oder Status
- verschachteltes Feld aus `attributes` oder `shipping`

Optional:

- Textsuche ueber Namen und Highlights
- Filter auf Arraywerte wie `tags`

## FR4. Kombinierte Filter

Mehrere Filter muessen kombinierbar sein.

Die Resultatliste und die Query-Anzeige muessen gemeinsam aktualisiert werden.

## FR5. Query-Anzeige

Die Anwendung muss die zu den aktiven Filtern passende MongoDB-Query anzeigen.

Die Anzeige muss:

- automatisch aktualisiert werden,
- lesbar formatiert sein,
- echte MongoDB-Syntax zeigen,
- den aktuellen `find`, `sort`, `limit` oder `aggregate`-Pfad widerspiegeln.

## FR6. Code-Anzeige

Die Anwendung muss den passenden PyMongo-Code zum aktuellen UI-Zustand zeigen.

Die Anzeige muss:

- kurz,
- didaktisch,
- konsistent in Python,
- ohne unnötige Produktionskomplexitaet

sein.

## FR7. Aggregationsansicht

Die Anwendung muss mindestens zwei einfache Aggregationen unterstuetzen.

Geeignete Beispiele:

- Durchschnittspreis pro Produkttyp
- Produktanzahl pro Hersteller
- Anzahl Produkte pro Kategorie
- Durchschnittliche Bewertung pro Produkttyp

Die Aggregationsansicht muss:

- die Pipeline anzeigen,
- die Resultate als Tabelle oder einfache Visualisierung zeigen,
- zwischen mehreren Aggregationen umschaltbar sein.

## FR8. Live-Datenwirkung

Die Anwendung soll sichtbar machen, dass sie echte MongoDB-Daten verwendet.

Mindestens eine der folgenden Funktionen ist Pflicht:

- Einfuegen eines Beispielprodukts,
- Aktivieren einer vorbereiteten Evolutionsansicht,
- Umschalten zwischen Seed-Sets.

Die einfachste Soll-Loesung ist ein Button zum Einfuegen eines vorbereiteten Beispielprodukts.

## FR9. Schema-Evolution-Anschaulichkeit

Die Anwendung soll mindestens eine sichtbare Stelle besitzen, an der neuere und aeltere Dokumentversionen nebeneinander erklaert werden koennen.

Das kann erfolgen ueber:

- Dokumente mit und ohne `regionalTaxCode`,
- eine Markierung im Detailpanel,
- eine vorbereitete Filteroption fuer Evolutionsstufen.

## FR10. Reset-Funktion

Alle aktiven Filter muessen mit einer einzigen Aktion ruecksetzbar sein.

## FR11. Stabiles lokales Setup

Ein Presenter muss die Anwendung mit wenigen Schritten lokal starten koennen:

1. MongoDB starten,
2. Daten seeden,
3. Flask-App starten,
4. Browser oeffnen,
5. Demo beginnen.

## FR12. Konsistente Detaildarstellung polymorpher Attribute

Die Anwendung muss typspezifische Attribute so darstellen, dass das Publikum auf einen Blick erkennt:

- welche Felder fuer alle Produkte gelten,
- welche Felder nur fuer einen Produkttyp gelten,
- welche Bereiche eingebettet sind,
- welche Felder nur in neueren Dokumentversionen vorkommen.

## FR13. Sichtbarer Zusammenhang zwischen Liste und Detail

Die Auswahl eines Produkts in der Liste muss das Detailpanel, die Query-Anzeige und die Code-Anzeige konsistent aktualisieren.

---

## 9. Nicht-funktionale Anforderungen

## NFR1. Einfachheit

Einfachheit ist die hoechste Prioritaet.

## NFR2. Verstaendlichkeit

Die UI muss auch fuer ein Publikum mit wenig MongoDB-Erfahrung lesbar bleiben.

## NFR3. Praesentationssicherheit

Die Demo muss lokal stabil laufen und darf keine unnötigen Abhaengigkeiten haben.

## NFR4. Reaktionsgeschwindigkeit

Die Demo muss sich lokal unmittelbar anfuehlen. Normale Interaktionen sollen subjektiv instant wirken.

## NFR5. Kleine Architektur

Der Datenfluss muss in einem Satz erklaerbar bleiben.

Zielbild:

`Browser UI -> Flask API -> PyMongo Repository -> MongoDB`

---

## 10. Ziel-Architektur

## 10.1 Backend-Schichten

### `backend/app.py`

Verantwortung:

- Flask-App erzeugen,
- HTTP-Routen definieren,
- Responses serialisieren,
- Fehler in klare JSON-Antworten umwandeln.

### `backend/database.py`

Verantwortung:

- MongoDB-Client kapseln,
- Datenbank und Collection bereitstellen,
- sauberes Verbindungsmanagement.

### `backend/repository.py`

Verantwortung:

- Lese- und Schreibzugriffe kapseln,
- keine HTTP-Logik,
- keine UI-Formatlogik.

### `backend/query_logic.py`

Verantwortung:

- UI-Filter in MongoDB-Queries uebersetzen,
- Aggregationspipelines erzeugen,
- optionale Default-Limits anwenden.

### `backend/mongo_format.py`

Verantwortung:

- Shell- oder Query-Anzeige formatieren,
- passenden PyMongo-Code generieren.

### `scripts/seed.py`

Verantwortung:

- deterministische Demodaten erzeugen,
- Daten ersetzen oder neu aufbauen,
- notwendige Indizes erstellen.

---

## 11. Ziel-Dateistruktur

```text
mongodb_demo/
  README.md
  DEMO_SCOPE.md
  DEMO_FLOW.md
  SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md

  backend/
    app.py
    database.py
    repository.py
    query_logic.py
    mongo_format.py
    serialization.py
    settings.py
    sample_data.py
    facets.py

  public/
    index.html
    app.js
    styles.css
    assets/

  scripts/
    seed.py
    reset_demo.py

  exports/
    screenshots/
    sample-queries/

  docker-compose.yml
  requirements.txt
  package.json
```

## 11.1 Verbindliche Dateikontrakte fuer das neue Projekt

### `backend/sample_data.py`

Muss vorbereitete Beispieldokumente und Demo-Sonderfaelle enthalten, etwa:

- ein typisches Laptop-Dokument,
- ein typisches T-Shirt-Dokument,
- ein Evolutionsdokument mit `regionalTaxCode`.

### `backend/facets.py`

Muss Facet- oder Auswahlwerte fuer Filter liefern, ohne UI-Code zu enthalten.

### `backend/query_logic.py`

Muss die einzige Stelle sein, an der Query-Dokumente und Aggregationspipelines aus UI-Parametern gebaut werden.

### `backend/mongo_format.py`

Muss dieselbe fachliche Operation in zwei Lesarten ausgeben koennen:

- MongoDB-Shell-nahe Darstellung,
- didaktisch passender PyMongo-Code.

---

## 12. API-Zielbild

Die Demo soll nur eine kleine Zahl klarer Endpunkte besitzen.

## 12.1 Pflichtendpunkte

- `GET /api/health`
- `GET /api/facets`
- `GET /api/products`
- `GET /api/products/<product_id>`
- `GET /api/aggregation`
- `POST /api/products/sample`

## 12.2 Optionale Endpunkte

- `GET /api/schema-versions`
- `POST /api/products/evolution-sample`

## 12.3 Antwortprinzipien

Jede relevante API-Antwort soll nach Moeglichkeit enthalten:

- die fachlichen Daten,
- die Query-Anzeige,
- den passenden Code-Ausschnitt.

## 12.4 Beispiel-Antwort fuer `GET /api/products`

```json
{
  "items": [],
  "total": 0,
  "limit": 25,
  "queryText": "db.products.find({...}).sort({...}).limit(25)",
  "codeText": "list(collection.find(query).sort(...).limit(25))"
}
```

## 12.5 Beispiel-Antwort fuer `GET /api/products/<product_id>`

```json
{
  "item": {},
  "queryText": "db.products.findOne({_id: 'prod_1001'})",
  "codeText": "collection.find_one({'_id': 'prod_1001'})"
}
```

## 12.6 Beispiel-Antwort fuer `GET /api/aggregation`

```json
{
  "kind": "avgPriceByType",
  "label": "Average price by product type",
  "results": [],
  "queryText": "db.products.aggregate([...])",
  "codeText": "list(collection.aggregate(pipeline))"
}
```

---

## 13. Seed-Daten

## 13.1 Zielgroesse

Die Demo-Daten muessen gross genug fuer Filter und Aggregationen, aber klein genug fuer sofortige lokale Bedienbarkeit sein.

Zielgroesse:

- 200 bis 600 Produkte
- 5 Produkttypen
- 20 bis 40 Hersteller
- 15 bis 30 Kategorien
- 2 bis 5 Varianten pro geeignetem Produkt
- 0 bis 10 eingebettete letzte Bewertungen pro Produkt

## 13.2 Seed-Eigenschaften

Die Daten muessen:

- deterministisch sein,
- verschiedene Produkttypen sichtbar machen,
- polymorphe Attribute enthalten,
- eingebettete Arrays enthalten,
- verschachtelte Felder enthalten,
- mindestens zwei Schema-Stufen enthalten.

## 13.3 Pflicht-Indizes fuer die Demo

Mindestens die folgenden Indizes muessen im Seed- oder Setup-Schritt angelegt werden:

- `productType`
- `manufacturer.name`
- `categories.slug`
- `updatedAt`
- ein passender Index fuer ein ausgewaehltes verschachteltes Feld

## 13.4 Beispiel fuer ein Demo-Dokument

```json
{
  "_id": "prod_1001",
  "productId": "prod_1001",
  "sku": "LAP-1001",
  "productType": "laptop",
  "name": "Aster Pro 14",
  "basePrice": 1499.0,
  "currency": "EUR",
  "manufacturer": {
    "id": "man_010",
    "name": "Northstar Computing"
  },
  "categories": [{ "id": "cat_001", "name": "Laptops", "slug": "laptops" }],
  "attributes": {
    "cpuModel": "Ryzen 7 8840U",
    "ramGb": 32,
    "storageGb": 1000,
    "screenSizeInches": 14
  },
  "variants": [{ "variantId": "var_1", "label": "32 GB / 1 TB", "inventoryCount": 18 }],
  "latestReviews": [{ "reviewId": "rev_01", "rating": 5, "title": "Fast and quiet" }],
  "regionalTaxCode": "DE-STD",
  "updatedAt": "2026-05-17T10:15:00Z"
}
```

---

## 14. UI-Anforderungen im Detail

## 14.1 Produktliste

Die Liste soll pro Eintrag mindestens zeigen:

- Name
- Produkttyp
- Preis
- Hersteller
- mindestens eine Kategorie
- Aktualisierungszeit

## 14.2 Detailpanel

Das Detailpanel soll drei Sichten unterstuetzen:

1. Dokumentansicht
2. Query-Ansicht
3. Code-Ansicht

Optional:

4. Schema-Hinweis oder Evolutionshinweis

## 14.3 Aggregationspanel

Das Panel soll:

- Aggregation auswaehlbar machen,
- Ergebnis als Tabelle zeigen,
- Pipeline erklaerbar machen.

## 14.4 Statusmeldungen

Die Anwendung soll kurze, klare Statusmeldungen haben fuer:

- Laden,
- leere Trefferliste,
- fehlgeschlagene Anfrage,
- erfolgreiches Einfuegen eines Beispieldokuments.

## 14.5 Pflicht-UI-Zustaende

Die UI muss folgende Zustaende sauber behandeln:

- Initialzustand ohne Auswahl,
- Ladezustand,
- Zustand ohne Treffer,
- Detailzustand mit Auswahl,
- Fehlerzustand,
- Aggregationszustand.

---

## 15. Konfiguration

Pflichtvariablen:

- `PORT`
- `MONGO_URI`
- `MONGO_DB`
- `MONGO_COLLECTION`

Optionale Variablen:

- `DEFAULT_LIMIT`
- `DEMO_SEED_PROFILE`
- `ENABLE_EVOLUTION_VIEW`

## 15.1 Beispiel fuer `.env.example`

```env
PORT=3000
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=product_demo
MONGO_COLLECTION=products

DEFAULT_LIMIT=25
DEMO_SEED_PROFILE=standard
ENABLE_EVOLUTION_VIEW=true
```

---

## 16. Test- und Qualitaetsstrategie

Das Demo-Projekt braucht keine schwere Testarchitektur, aber es braucht stabile Minimaltests.

## 16.1 Pflicht-Checks

- Seed-Skript laeuft deterministisch durch.
- App startet mit lokalem MongoDB.
- Produktliste ist abrufbar.
- Detailansicht liefert ein echtes Produkt.
- Aggregation liefert Resultate.
- Query- und Codeanzeige enthalten plausible Inhalte.

## 16.2 Empfohlene Tests

- kleine Backend-Tests mit `pytest`
- Query-Building-Tests
- Serialisierungs-Tests
- einfache Smoke-Tests fuer zentrale Endpunkte

## 16.3 Mindest-Smoketest fuer Live-Demo

Vor einer Praesentation soll ein schneller lokaler Smoke-Test moeglich sein:

1. Health-Endpunkt pruefen.
2. Produktliste abrufen.
3. Erstes Produkt oeffnen.
4. Eine Aggregation abrufen.
5. Beispielprodukt einfuegen.

## 16.4 Manuelle Abnahme vor einer Praesentation

Vor einer echten Praesentation soll manuell geprueft werden:

1. Startet die Liste mit sinnvollen Daten?
2. Sind mehrere Produkttypen sofort sichtbar?
3. Aendert sich die Query-Anzeige bei Filterwechsel?
4. Ist das Detaildokument gut lesbar?
5. Liefert die Aggregation ein erklaerbares Resultat?
6. Funktioniert der Beispielinsert?

---

## 17. Akzeptanzkriterien

Das Demo-Projekt gilt nur dann als fachlich fertig, wenn:

1. die Domaene auf dem Produktkatalog basiert,
2. mindestens 5 Produkttypen sichtbar vorhanden sind,
3. Query und Code parallel zur UI nachvollziehbar angezeigt werden,
4. mindestens zwei Aggregationen funktionieren,
5. eingebettete Strukturen und Arrays im Detail klar sichtbar sind,
6. mindestens eine Schema-Evolutionsidee erklaerbar praesentiert werden kann,
7. das lokale Setup in wenigen Minuten stabil funktioniert.
8. Query-Text und Code-Text fuer Listen- und Detailansicht immer vorhanden sind.
9. Die Demo besitzt mindestens ein vorbereitetes Beispieldokument fuer jede Produktfamilie.

---

## 18. Minimaler Umsetzungsplan fuer ein neues Projekt

1. MongoDB-Dokumentmodell fuer Produkte definieren.
2. Seed-Datengenerator fuer die Demo schreiben.
3. Repository und Query-Logik implementieren.
4. Flask-Routen fuer Liste, Detail und Aggregation bauen.
5. UI fuer Liste, Detail, Query und Code erstellen.
6. Beispielinsert oder Evolutionsdemo ergaenzen.
7. Setup und README finalisieren.

---

## 19. Erwartete Projekt-Deliverables

Ein neues Demo-Projekt nach dieser Spezifikation muss am Ende mindestens die folgenden Artefakte liefern:

### Produkt-Deliverables

- eine lokal startbare Demo-Anwendung,
- ein deterministisches Seed-Skript,
- eine Produktliste mit mehreren Produkttypen,
- eine funktionierende Detailansicht,
- Query- und Code-Anzeige,
- mindestens zwei Aggregationen,
- einen sichtbaren Live- oder Evolutions-Effekt.

### Dokumentations-Deliverables

- ein README mit Schnellstart,
- ein klares Demo-Flow-Dokument,
- eine kurze Scope-Abgrenzung,
- eine Liste empfohlener Klickpfade fuer die Praesentation.

### Praesentations-Deliverables

- mindestens ein stabiler Standard-Demo-Ablauf,
- vorbereitete Beispielprodukte fuer mehrere Typen,
- mindestens ein gutes Evolutionsbeispiel,
- exportierbare Screenshots oder Query-Beispiele.

---

## 20. Definition of Done fuer das neue Demo-Projekt

Das neue Demo-Projekt ist erst dann wirklich abgeschlossen, wenn alle folgenden Aussagen gleichzeitig wahr sind:

1. Die Anwendung laesst sich lokal in wenigen Schritten starten.
2. Das Publikum kann den Zusammenhang zwischen UI, Query und Dokument verstehen.
3. Polymorphe Produkttypen sind auf den ersten Blick sichtbar.
4. Mindestens ein Evolutionsaspekt ist erklaerbar demonstrierbar.
5. Die Demo bleibt klein genug, um in wenigen Minuten erklaert zu werden.
6. Das Projekt versucht nicht, die Rolle des Benchmark-Repos zu uebernehmen.

---

## 21. Abschlussbewertung der Soll-Ausrichtung

Dieses Demo-Projekt bleibt technisch absichtlich leichtgewichtig und nah am aktuellen Flask-/PyMongo-/Vanilla-JS-Ansatz. Inhaltlich wird es jedoch auf dieselbe Produktkatalog-Domaene wie das Hauptprojekt ausgerichtet.

So entsteht ein Demo-Repo, das:

- modern genug fuer eine gute Praesentation,
- klein genug fuer schnelle Erklaerbarkeit,
- und fachlich konsistent genug fuer einen roten Faden mit dem Testprojekt

ist.
