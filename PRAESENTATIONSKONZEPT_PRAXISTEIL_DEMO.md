# Präsentationskonzept Praxisteil Demo

## Zweck dieses Dokuments

Dieses Dokument bildet das praxistaugliche Drehbuch für den Demo-Teil der Präsentation, exakt abgestimmt auf den vorherigen Theorieteil (gemäß PPTX). Es verknüpft die theoretischen Slides mit den Live-Aktionen im `mongodb_demo` Projekt.

---

## Slide-Struktur und Live-Regie

### Slide 1 - Agenda des Praxisteils

- **Ziel:** Direkte Überleitung aus der Theorie und Fahrplan für die Demo.
- **Inhalt auf der PPT:**
  - Die Architektur einer Dokumentendatenbank
  - Anbindung einer MongoDB Datenbank (anhand von pymongo)
  - Konfiguration einer MongoDB Datenbank (Replica Sets)
- **Was sagen:** "Nach der Theorie betrachten wir nun die Praxis. Wir schauen uns die Architektur in unserem Projekt an, untersuchen, wie MongoDB konkret über PyMongo angebunden ist, und betrachten die Konfiguration unseres Replica Sets im Betrieb."

---

### Slide 2 - Demo-Aufbau

- **Ziel:** Den Rahmen für den fairen Systemvergleich setzen.
- **Inhalt auf der PPT:**
  - Shop-Ansicht für CRUD-Demonstration
  - Showcase-Ansicht für Datenmodell, Query-Form und Aggregation
  - MongoDB-Backend und PostgreSQL-Backend liefern dasselbe Produkt-JSON
  - Dadurch ist der Vergleich fachlich fair und direkt sichtbar
- **Live-Aktion:** Kurz die Anwendung (`/shop`) öffnen, um das optische Erscheinungsbild des Shops zu zeigen.
- **Was sagen:** "Um MongoDB und PostgreSQL vergleichen zu können, haben wir eine Shop-Anwendung gebaut. Beide Datenbanken liegen hinter derselben API – wir können jederzeit umschalten und vergleichen, ohne dass sich die Fassade ändert. Ein absolut fairer Vergleich."

---

### Slide 3 - Anbindung von MongoDB mit PyMongo

- **Ziel:** Die technische Brücke ins Backend schlagen.
- **Inhalt auf der PPT:**
  - Verbindung über MongoClient und direkte Arbeit auf Collection-Ebene
  - Konfiguration von Write Concern, Read Concern und Read Preference
  - CRUD-Operationen sind hinter einem gemeinsamen Repository-Interface gekapselt
  - Die API bleibt für das Frontend identisch
- **Live-Aktion / Code-Snippet:** Kurz einen Blick in `mongodb_demo/backend/database.py` werfen (Initialisierung MongoClient) oder als Snippet auf die Folie packen.

---

### Slide 4 - CRUD im Demo-Projekt (Live-Fokus)

- **Ziel:** Beweisen, dass grundlegende Datenbankoperationen reibungslos funktionieren.
- **Inhalt auf der PPT:**
  - Create: neues Produkt in der Shop-Ansicht anlegen
  - Read: Produktliste und Produktdetail laden
  - Update: Produkt im Dialog bearbeiten und vollständig ersetzen
  - Delete: Produkt löschen und direkt im Katalog sehen
- **Live-Aktion:** In `/shop` ein neues Produkt über das Formular anlegen, den Preis aktualisieren (Update) und anschließend löschen.

---

### Slide 5 - Docker- und Replica-Set-Konfiguration

- **Ziel:** Technische Architektur greifbar machen.
- **Inhalt auf der PPT:**
  - MongoDB läuft als Replica Set mit mongo1, mongo2 und Arbiter
  - Kein Sharding, bewusst reduzierter Aufbau für den Praxisteil
  - Seed-Container initialisieren die Demo-Daten
  - Die Statusanzeige im Showcase zeigt aktuelles Primary-Mitglied
- **Live-Aktion:** Den Footer in der App / Showcase-View zeigen, wo der aktuelle Primary (`mongo1`) angezeigt wird.

---

### Slide 6 - Write Concern, Read Concern & Read Preference

- **Ziel:** Zeigen, dass MongoDB für Konsistenz/Verfügbarkeits-Tradeoffs konfigurierbar ist.
- **Inhalt auf der PPT:**
  - **Write Concern:** w=1 (schnell) vs. majority (sicher, aber Latenz/Write-Block bei Partitionierung)
  - **Read Concern:** local vs majority
  - **Read Preference:** primary vs secondary (Verteilung vs. marginal veraltete Daten)
- **Was sagen:** "Was bedeutet das im Code? Wir können pro Operation entscheiden, wie wichtig uns sofortige Bestätigung gegenüber absoluter Datensicherheit ist." (Bezug auf CAP-Theorem).

---

### Slide 7 - Dokumentaufbau vs Main Entity

- **Ziel:** Den Kernvorteil des Dokumentenmodells visualisieren.
- **Inhalt auf der PPT:**
  - MongoDB speichert ein Produkt als Aggregat in einem Dokument
  - Kategorien, Attribute, Varianten und Reviews liegen direkt am Produkt
  - PostgreSQL rekonstruiert dieselbe Fachsicht aus mehreren Tabellen durch Joins
- **Live-Aktion:** Die Ansicht auf `/showcase` wechseln! Im Tab "Shape" die verschachtelte JSON-Struktur von MongoDB mit dem normalisierten Schema von PostgreSQL vergleichen.

---

### Slide 8 - Bounded und Unbounded Embedding

- **Ziel:** Best Practices der MongoDB-Modellierung erklären.
- **Inhalt auf der PPT:**
  - `latestReviews` im Demo-Projekt ist ein Beispiel für _bounded embedding_ (begrenzt, kontrollierte Größe)
  - Vollständige Historie aller Reviews wäre _unbounded embedding_ (kann 16MB Grenze sprengen)
  - Leitspruch: Eingebettet wird, was gemeinsam gelesen wird und begrenzt bleibt.
- **Live-Aktion:** Im `/showcase` (Document Tab) anschaulich auf das "reviews" Array im Produkt-JSON deuten.

---

### Slide 9 - Aggregation Framework vs. SQL Joins

- **Ziel:** Performance-Auswirkungen lokaler Daten erklären.
- **Inhalt auf der PPT:**
  - Aggregation Framework vs SQL Joins
  - Lokal abrufbare Aggregate (MongoDB) sind bei verteilten Systemen oft performanter, da keine teuren netzwerkübergreifenden Joins berechnet werden müssen.
- **Live-Aktion:** Im `/showcase` auf "Query (Agg.)" umschalten und die Aggregation Pipeline in Mongo mit den SQL-Joins in Postgres vergleichen.

---

### Slide 10 - Ausfallsicherheit (High Availability in Action)

- **Ziel:** Echtes Verhalten im Fehlerfall demonstrieren.
- **Inhalt auf der PPT:**
  - Manuelles Ausschalten / Killen einer Node
  - Zeigen von "Availability" im AP-System
- **Live-Aktion:**
  1. Statusleiste im Showcase zeigt: `Primary: mongo1`.
  2. Im Terminal (im Hintergrund): `docker stop mongo1` ausführen.
  3. Live in der UI zeigen: Nach wenigen Sekunden springt die Statusleiste um auf `Primary: mongo2` (oder es wird ein Write-Test im Shop gemacht, der weiterhin durchläuft).
  4. _Hinweis: Der Deep-Dive zur bewussten Erzeugung von C-Tradeoffs (Datenverlust bei Failover) wird zugunsten eines reibungsloseren Präsentationsflusses weggelassen._

---

### Slide 11 - Synthese & Fragerunde

- **Ziel:** Runder Abschluss passend zum Ende der Präsentation.
- **Live-Aktion:** Zurück auf die PPT wechseln.
  - Danke für Ihre Aufmerksamkeit!
  - Zeit für Fragen.
