# Spezifikation: Wissenschaftliches Testprojekt fuer eine Seminararbeit

## Dokumentstatus

- Ziel: Vollstaendige Spezifikation fuer ein neues wissenschaftliches Vergleichsprojekt
- Projektrolle: Hauptprojekt fuer Architekturvergleich und Benchmarking
- Zielrepo: `mongodb-v2`
- Status: Iteration 3 von 3
- Grundlage: neue Zielstruktur, aktueller Python-Stack, neue fachliche Ausrichtung

## Revisionsnotizen dieser Iteration

- Iteration 1: Zielbild, Domaene, Technologie- und Methodenrahmen gesetzt
- Iteration 2: Vertragsdetails, Fairnessregeln, Export- und Abnahme-Schaerfung eingebaut
- Iteration 3: Run-Artefakte, Preflight-Regeln, Fehlerklassen und Umsetzungsreife finalisiert

---

## 1. Zweck des Projekts

Dieses Projekt ist das wissenschaftliche Kernartefakt einer Seminararbeit im Masterstudium und dient dazu, den Vergleich zwischen einem relationalen System und einem dokumentenorientierten System unter kontrollierten Bedingungen empirisch und architektonisch belastbar durchzufuehren.

Das Projekt ist kein Webservice, kein Produktivsystem und kein allgemeiner Datenbank-Benchmark. Es ist ein fokussiertes Vergleichsprojekt mit einer klar definierten Domaene, klaren Hypothesen, reproduzierbarer Infrastruktur und nachvollziehbaren Messregeln.

---

## 2. Forschungsziel

Das Projekt soll die folgende Hauptfrage beantworten:

> Unter welchen Bedingungen ist ein dokumentenorientiertes Datenmodell in MongoDB gegenueber einem relationalen Datenmodell in PostgreSQL bei polymorphen Produktdaten, komplexen Aggregaten, Schema-Evolution und quantitativen Lastprofilen fachlich oder technisch ueberlegen, und wann ist das relationale Modell im Vorteil?

Aus dieser Frage folgen vier Untersuchungsachsen:

1. Modellierungsaufwand
2. Datenlokalitaet und Leseverhalten
3. Update- und Evolutionskosten
4. analytische oder join-aehnliche Zugriffspfade

---

## 3. Nicht-Ziele

Das Projekt soll explizit nicht in folgende Richtungen ausufern:

- kein allgemeiner Vergleich aller Datenbanktypen,
- kein Benchmark ueber beliebige Domaenen,
- kein HTTP-API-Projekt,
- kein Frontend,
- kein ORM-Showcase,
- kein Cluster-zentriertes Infrastrukturprojekt als Hauptaussage,
- kein Cloud- oder Kubernetes-Projekt,
- keine Produktionsthemen wie Authentifizierung, Mandantenfaehigkeit oder Observability-Plattformen.

---

## 4. Ziel-Nutzen des Projekts

Das Projekt soll drei Arten von Ergebnissen liefern:

### A. Wissenschaftliche Ergebnisse

- empirische Messungen,
- verteidigbare Hypothesenpruefung,
- dokumentierte Threats to Validity,
- methodisch saubere Interpretation.

### B. Architektonische Ergebnisse

- nachvollziehbarer Vergleich zweier Modellierungsparadigmen,
- sichtbare Unterschiede bei Polymorphie und Aggregaten,
- expliziter Vergleich von Schema-Evolution und Denormalisierung.

### C. Praesentationsfaehige Ergebnisse

- exportierbare Rohdaten,
- aggregierte Tabellen und Diagramme,
- kompakte Vergleichsbeispiele fuer die Praesentation.

---

## 5. Technologischer Zielrahmen

Das neue Projekt soll aehnliche Technologien wie das aktuelle Repo verwenden, um Migrationskosten klein zu halten und die bestehende Infrastruktur sinnvoll weiterzuverwenden.

## 5.1 Programmiersprache

- Python 3.11+

Begruendung:

- geeignet fuer wissenschaftliche Skripte,
- direkter Zugriff auf Datenbanktreiber,
- gute Bibliothekslage fuer Statistik, Export und Tests,
- konsistent mit dem aktuellen `mongodb-v2`.

## 5.2 Datenbanktreiber

- MongoDB: `pymongo==4.7.*`
- PostgreSQL: `psycopg2-binary==2.9.*`

Optional zulaessig fuer spaetere Erweiterung:

- `motor` nur dann, wenn ein expliziter Async-Vergleich sauber motiviert ist.

## 5.3 Hilfsbibliotheken

- `python-dotenv==1.0.*`
- `rich==13.*`
- `faker==24.*`
- `numpy==1.26.*`
- `pytest==8.*`

Optional zulaessig:

- `pandas` fuer die Nachbearbeitung von Exporten,
- `matplotlib` oder `seaborn` fuer Diagrammerzeugung.

## 5.4 Explizit ausgeschlossene Technologien

- SQLAlchemy
- Django
- Flask
- FastAPI
- React
- Node.js als Laufzeitkern des Benchmark-Projekts
- Redis, Kafka, Celery oder sonstige Middleware
- proprietaere Benchmark-Frameworks als Kernabhaengigkeit

---

## 6. Domaene des neuen Projekts

## 6.1 Fachlicher Kontext

Die Domaene ist ein vereinfachter E-Commerce-Produktkatalog mit polymorphen Produkttypen, Varianten, Kategorien, Herstellern und Kundenbewertungen.

## 6.2 Ziel des Domaenenmodells

Die Domaene wurde so gewaehlt, dass folgende Spannungen natuerlich sichtbar werden:

- polymorphe Attribute,
- hierarchische Aggregate,
- Einbettung versus Referenzen,
- Joins versus Dokumentlokalitaet,
- Schema-Evolution unter laufendem Betrieb,
- Schreibkosten bei duplizierten Daten.

## 6.3 Kernentitaeten

- Produkt
- Produkttyp
- Variante
- Kategorie
- Hersteller
- Bewertung
- optional: Bestellposition oder Kaufhistorie fuer erweiterte Benchmark-Szenarien

---

## 7. Fachliches Zielmodell

## 7.1 Gemeinsame Pflichtattribute eines Produkts

Jedes Produkt muss mindestens die folgenden Felder besitzen:

- `product_id`
- `sku`
- `product_type`
- `name`
- `base_price`
- `currency`
- `manufacturer_id`
- `category_ids`
- `status`
- `created_at`
- `updated_at`

Ab Evolutionsstufe 2 zusaetzlich:

- `regional_tax_code`

## 7.2 Produktspezifische Attribute

Jeder Produkttyp besitzt eine eigene Attributmenge.

### Laptop

- `cpu_model`
- `ram_gb`
- `storage_gb`
- `gpu_model`
- `screen_size_inches`

### T-Shirt

- `size`
- `material`
- `fit`
- `color`
- `target_group`

### Buch

- `author`
- `isbn`
- `page_count`
- `language`
- `publisher`

### Smartphone

- `soc`
- `display_inches`
- `battery_mah`
- `camera_mp`
- `os_family`

### Schreibtisch

- `material`
- `width_cm`
- `height_cm`
- `depth_cm`
- `max_load_kg`

## 7.3 Varianten

Varianten sind fachlich Teil des Produkts, aber technisch je nach Datenbank unterschiedlich modelliert.

Beispielattribute einer Variante:

- `variant_id`
- `label`
- `price_delta`
- `inventory_count`
- `variant_attributes`

## 7.4 Kategorien

Kategorien muessen umbenennbar sein und werden bewusst als wichtiger Vergleichspunkt fuer Denormalisierung genutzt.

Pflichtfelder:

- `category_id`
- `name`
- `slug`
- `parent_category_id`

## 7.5 Bewertungen

Bewertungen dienen als Bestandteil komplexer Aggregate und analytischer Workloads.

Pflichtfelder:

- `review_id`
- `product_id`
- `user_id`
- `rating`
- `title`
- `text`
- `created_at`
- `verified_purchase`

---

## 8. Modellierungsregeln fuer beide Datenbanken

## 8.1 MongoDB

MongoDB soll das Produkt als fachliches Aggregat modellieren.

Pflichtentscheidungen:

- produktspezifische Attribute liegen im Produktdokument,
- Varianten werden eingebettet,
- die letzten 5 Bewertungen duerfen eingebettet oder materialisiert vorgehalten werden,
- Kategorien duerfen fuer bestimmte Szenarien dupliziert werden, wenn dies explizit dokumentiert ist,
- Hersteller duerfen referenziert bleiben.

## 8.2 PostgreSQL

PostgreSQL soll das Modell relational und explizit abbilden.

Pflichtentscheidungen:

- gemeinsame Produktstammdaten in einer Basistabelle,
- typabhängige Detailtabellen pro Produkttyp oder ein wohldefiniertes alternatives relationales Muster,
- Varianten in eigener Tabelle,
- Kategorien in eigener Tabelle und Verbindungstabelle,
- Bewertungen in eigener Tabelle,
- Hersteller in eigener Tabelle.

## 8.3 Fairness-Regel

Die Modellierung darf Unterschiede sichtbar machen, aber sie darf keine Seite absichtlich sabotieren. Jede relevante Modellierungsentscheidung muss in einem separaten Dokument begruendet werden.

## 8.4 Verbotene Vergleichsverzerrungen

Die folgende Vergleichsverzerrungen sind in der neuen Projektumsetzung explizit unzulaessig:

- eine globale Lock-Serialisierung nur auf einer Datenbankseite,
- unterschiedliche Default-Limits oder abweichende Ergebnismengen,
- fachlich verschiedene Datenausschnitte hinter gleich benannten Workloads,
- massiv unterschiedliche Indexpflege ohne Dokumentation,
- Explain- oder Analyseausgaben nur fuer eine Datenbank,
- unterschiedliche Seed-Semantik zwischen relationalem und dokumentenorientiertem Modell.

---

## 9. Projektarchitektur

Das Projekt besteht aus zwei logisch getrennten Bereichen im selben Repo:

1. `showcase/` fuer den qualitativen Architekturvergleich
2. `benchmark/` fuer die quantitative Evaluation

## 9.1 Bereich `showcase/`

Dieser Bereich demonstriert denselben fachlichen Use Case in zwei Modellierungswelten.

Er soll keine Lasttests ausfuehren. Er soll sichtbar machen:

- wie das Modell aussieht,
- welche Persistenzlogik benoetigt wird,
- wie komplex ein Aggregate-Read ist,
- wie eine Schema-Aenderung durch das System laeuft.

## 9.2 Bereich `benchmark/`

Dieser Bereich misst gezielt definierte Workloads.

Er soll:

- Daten generieren,
- Datenbanken aufsetzen und validieren,
- Workloads ausfuehren,
- Metriken exportieren,
- Ergebnisse standardisiert ausgeben.

---

## 10. Benchmark-Ziele und Hypothesen

## 10.1 Szenario A: Read Locality Advantage

Fragestellung:

Wie verhalten sich beide Systeme beim Abruf eines vollstaendigen Produktaggregats mit Varianten, Kategorien, Hersteller und letzten Bewertungen?

Hypothese:

MongoDB erzielt niedrigere Latenzen bei stark aggregatnahen Leseoperationen, wenn die fachlich zusammengehoerigen Daten im selben Dokument vorliegen.

Metriken:

- p50
- p90
- p95
- p99
- mean latency
- throughput
- Fehlerrate

## 10.2 Szenario B: Denormalized Update Cost

Fragestellung:

Wie teuer ist die Umbenennung einer Kategorie, wenn diese in MongoDB dupliziert und in PostgreSQL zentral referenziert ist?

Hypothese:

PostgreSQL ist bei zentralen Massenupdates ueber referenzierte Stammdaten deutlich effizienter und einfacher zu kontrollieren.

Metriken:

- Gesamtdauer der Operation
- Anzahl betroffener Datensaetze oder Dokumente
- Fehlerrate
- Zeit bis Konsistenz erreicht ist

## 10.3 Szenario C: Join versus Lookup Pressure

Fragestellung:

Wie verhalten sich beide Systeme bei einer analytischen Query ueber Hersteller, Produkte und Bewertungen?

Hypothese:

PostgreSQL ist bei stark vernetzten, filternden Aggregationen mit relationalem Query Planner im Vorteil, sofern keine denormalisierte Voraggregation genutzt wird.

Metriken:

- p50
- p95
- p99
- throughput
- Explain-Plan-Qualitaet
- Fehlerrate

## 10.4 Optionales Szenario D: Topologieerweiterung

Nur wenn die Kernszenarien stabil sind, darf spaeter ein optionales Topologie-Szenario hinzukommen.

Es ist explizit nicht Teil des Kernbelegs.

## 10.5 Szenario-Matrix

| Szenario   | Fachliche Operation                                       | Primaere Aussage        | Zulaessige Topologien                                 |
| ---------- | --------------------------------------------------------- | ----------------------- | ----------------------------------------------------- |
| A          | kompletter Produkt-Aggregat-Read                          | Datenlokalitaet         | Postgres Single, Mongo Single                         |
| B          | Kategorie-Umbenennung                                     | Denormalisierungskosten | Postgres Single, Mongo Single                         |
| C          | analytische Query ueber Produkte, Hersteller, Bewertungen | Join- oder Lookup-Druck | Postgres Single, Mongo Single                         |
| D optional | Skalierungs- oder Topologiefrage                          | Infrastrukturwirkung    | Postgres Single, Mongo Single, optional Mongo Sharded |

---

## 11. Messmethodik

## 11.1 Allgemeine Regeln

- jeder Lauf muss eine eindeutige Run-ID erhalten,
- jeder Workload muss isoliert protokolliert werden,
- Seed und Parameter muessen exportiert werden,
- jede Messung muss mehrfach wiederholt werden,
- Warmup und produktive Messung muessen getrennt werden.

## 11.2 Wiederholungen

Jeder Benchmark-Lauf soll mindestens 5 Wiederholungen pro Datenbank und Szenario umfassen.

Wenn die Streuung hoch ist, soll auf 10 Wiederholungen erhoeht werden.

## 11.3 Warmup-Regel

Vor jeder Messserie wird ein Warmup ausgefuehrt, dessen Resultate nicht in die Endauswertung eingehen.

## 11.4 Cache-Regel

Die Spezifikation muss explizit festlegen, ob ein Lauf als Cold-Cache- oder Warm-Cache-Lauf behandelt wird.

## 11.5 Concurrency-Regel

Parallelitaet darf nur dann verwendet werden, wenn beide Datenbanken ueber faire Connection- oder Pooling-Strategien angesprochen werden.

Eine clientseitige Serialisierung einer Seite ist unzulaessig.

## 11.6 Pflichtprotokoll pro Messlauf

Jeder Messlauf muss mindestens die folgenden Schritte in derselben Reihenfolge ausfuehren:

1. Konfiguration laden und run manifest erzeugen.
2. Ziel-Datenbankverbindungen pruefen.
3. Schema und Indizes validieren.
4. Datensatzprofil herstellen oder verifizieren.
5. Warmup-Lauf ausfuehren.
6. Produktive Messung starten.
7. Rohresultate und Metadaten exportieren.
8. Optional Explain- oder Plan-Daten exportieren.
9. Lauf als erfolgreich oder fehlerhaft markieren.

## 11.7 Fehlerklassifikation

Jeder fehlgeschlagene Messvorgang muss mindestens einer Fehlerklasse zugeordnet werden:

- Verbindungsfehler
- Timeout
- Query-Fehler
- Validierungsfehler
- Datenintegritaetsfehler
- Infrastrukturfehler
- unbekannter Fehler

Die Fehlerklasse muss in jedem fehlgeschlagenen Exportdatensatz enthalten sein.

---

## 12. Datenvolumen und Seed-Strategie

## 12.1 Seed-Ziele

Die Seed-Daten muessen deterministisch und fachlich plausibel sein.

## 12.2 Datenmengen fuer lokale Entwicklungslaeufe

- 5.000 Produkte
- 20.000 Varianten
- 50.000 Bewertungen
- 200 Kategorien
- 500 Hersteller

## 12.3 Datenmengen fuer Vollbenchmarks

- 100.000 Produkte
- 400.000 Varianten
- 1.000.000 Bewertungen
- 1.000 Kategorien
- 5.000 Hersteller

## 12.4 Verteilungsvorgaben

- Produkttypen muessen ungleich, aber kontrolliert verteilt sein,
- einige Hersteller sollen sehr viele Produkte haben,
- einige Kategorien sollen stark besetzt sein,
- Bewertungen sollen eine realistische Schiefe besitzen,
- ein Teil der Produkte soll viele Bewertungen, ein grosser Teil wenige Bewertungen haben.

---

## 13. CLI-Zielbild

Das Testprojekt soll als Python-CLI bedient werden.

## 13.1 Pflichtbefehle

- `python -m benchmark.runner --scenario read-locality`
- `python -m benchmark.runner --scenario denormalized-update`
- `python -m benchmark.runner --scenario join-lookup`
- `python -m benchmark.runner --scenario all`

## 13.2 Pflichtoptionen

- `--db postgres`
- `--db mongo`
- `--db all`
- `--dataset small`
- `--dataset large`
- `--repetitions <n>`
- `--warmup`
- `--export`
- `--output-dir <path>`

## 13.3 Optionale, aber sinnvolle Optionen

- `--explain`
- `--skip-seed`
- `--seed-only`
- `--validate-only`

---

## 14. Konfiguration

Die Konfiguration erfolgt ueber `.env` und optionale CLI-Flags.

## 14.1 Pflichtvariablen

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `MONGO_URI`
- `MONGO_DB`
- `EXPORT_DIR`

## 14.2 Optionale Variablen

- `LOG_LEVEL`
- `POSTGRES_POOL_MIN`
- `POSTGRES_POOL_MAX`
- `MONGO_MAX_POOL_SIZE`
- `BENCHMARK_DEFAULT_DATASET`

## 14.3 Beispiel fuer `.env.example`

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=product_benchmark
POSTGRES_USER=benchmark
POSTGRES_PASSWORD=benchmark

MONGO_URI=mongodb://localhost:27017/
MONGO_DB=product_benchmark

EXPORT_DIR=./exports/raw
LOG_LEVEL=INFO

POSTGRES_POOL_MIN=1
POSTGRES_POOL_MAX=20
MONGO_MAX_POOL_SIZE=50
BENCHMARK_DEFAULT_DATASET=small
```

---

## 15. Code-Struktur

## 15.1 `benchmark/config.py`

Laedt und validiert die Konfiguration.

## 15.2 `benchmark/models.py`

Enthaelt Dataclasses oder Modelle fuer:

- Workload-Definitionen,
- Operationsergebnisse,
- Metrikzusammenfassungen,
- Exportmetadaten.

## 15.3 `benchmark/adapters/base.py`

Definiert das gemeinsame Adapter-Interface.

## 15.4 `benchmark/adapters/postgres_adapter.py`

Implementiert:

- Verbindungsmanagement,
- Schemaaufbau,
- Seed-Operationen,
- Workload-spezifische Query-Pfade,
- Explain-Plan-Abfragen.

## 15.5 `benchmark/adapters/mongo_adapter.py`

Implementiert dieselben fachlichen Operationen fuer MongoDB.

## 15.6 `benchmark/seed/generator.py`

Erzeugt reproduzierbare Produktkatalog-Daten.

## 15.7 `benchmark/workloads/`

Enthaelt fachliche Definition und Ausfuehrung einzelner Workloads.

## 15.8 `benchmark/validation/`

Prueft vor Messlaeufen:

- Schema-Vollstaendigkeit,
- Index-Zustand,
- Datenmengenkonsistenz,
- fachliche Semantik der Queries.

## 15.9 Verbindliche Dateikontrakte fuer das neue Projekt

### `benchmark/workload_catalog.py`

Muss jede fachliche Messoperation als deklaratives Profil definieren:

- `scenario_id`
- `display_name`
- `query_family`
- `dataset_profile`
- `default_repetitions`
- `supports_explain`

### `benchmark/statistics.py`

Muss die statistische Verdichtung kapseln und mindestens liefern:

- Percentile-Berechnung,
- Mittelwert,
- Standardabweichung,
- Min und Max,
- Konfidenzintervall oder dokumentierte Alternative.

### `benchmark/export.py`

Muss strukturierte Roh- und Summary-Exporte schreiben, ohne Darstellungscode zu enthalten.

### `benchmark/fairness_checks.py`

Muss zentrale Guardrails pruefen, zum Beispiel:

- stimmt die erwartete Datenmenge,
- existieren die benoetigten Indizes,
- liefern Referenzqueries vergleichbare Ergebnismengen,
- ist Concurrency fuer beide Seiten konsistent konfiguriert.

---

## 16. Exportformat

Jeder Lauf soll ein maschinenlesbares JSON-Ergebnis erzeugen.

Pflichtfelder:

- `run_id`
- `timestamp_utc`
- `scenario_id`
- `scenario_name`
- `database_type`
- `dataset_profile`
- `repetition_index`
- `seed`
- `warmup_used`
- `total_operations`
- `successful_operations`
- `failed_operations`
- `throughput_ops_per_sec`
- `mean_latency_ms`
- `p50_latency_ms`
- `p90_latency_ms`
- `p95_latency_ms`
- `p99_latency_ms`
- `max_latency_ms`
- `notes`

Optional:

- `explain_summary`
- `host_stats`
- `index_snapshot`

## 16.1 Run-Manifest pro Messserie

Neben den Einzelresultaten muss pro Messserie ein Manifest geschrieben werden.

Pflichtfelder:

- `run_id`
- `created_at_utc`
- `dataset_profile`
- `seed`
- `active_scenarios`
- `active_databases`
- `warmup_enabled`
- `repetition_count`
- `notes`

## 16.2 Verzeichnisregeln fuer Exporte

- Rohresultate: `exports/raw/<run_id>/`
- Summary-Dateien: `exports/processed/<run_id>/`
- Diagramme: `exports/charts/<run_id>/`

## 16.3 Pflichtdateien pro erfolgreicher Messserie

- `manifest.json`
- `raw_results.json`
- `summary.json`
- `environment.json`
- optional `explain.json`

---

## 17. Teststrategie

`pytest` wird nur fuer Korrektheitstests genutzt, nicht fuer die eigentlichen Benchmarks.

## 17.1 Pflicht-Unit-Tests

- Seed-Determinismus
- Metrikberechnung
- Query-Building-Semantik
- Exportserialisierung
- Konfigurationsvalidierung

## 17.2 Pflicht-Integrationschecks

- Aufbau von PostgreSQL-Schema
- Aufbau von MongoDB-Indizes
- Seed-Konsistenz in beiden Datenbanken
- identische Ergebnismengen fuer definierte Referenzqueries

## 17.3 Pflicht-Preflight-Checks vor produktiven Messungen

Vor jeder produktiven Messung muessen automatisiert geprueft werden:

1. Datenbanken erreichbar
2. benoetigte Tabellen oder Collections vorhanden
3. benoetigte Indizes vorhanden
4. erwartete Datenmenge erreicht
5. Referenzqueries liefern Resultate
6. Exportziel ist schreibbar

---

## 18. Akzeptanzkriterien

Das Projekt gilt nur dann als fachlich fertig, wenn alle folgenden Punkte erfuellt sind:

1. Die Domaene ist durchgaengig der polymorphe Produktkatalog.
2. Es existieren mindestens drei belastbare Kernszenarien.
3. Fuer jedes Szenario sind Hypothese, Messmethode und Ergebnisinterpretation dokumentiert.
4. PostgreSQL und MongoDB werden ueber faire Treiber- und Concurrency-Strategien angesprochen.
5. Die Datenmodelle beider Systeme sind explizit und nachvollziehbar dokumentiert.
6. Jeder Messlauf ist reproduzierbar.
7. Es existieren Exportdateien, die direkt fuer Diagramme weiterverarbeitet werden koennen.
8. Die Kernresultate sind praesentationsfaehig verdichtet.
9. Jeder Kernworkload besitzt einen dokumentierten Fairness-Check.
10. Fuer jeden Kernworkload existiert mindestens eine Referenzquery zur Ergebnisvalidierung.

## 18.1 Abnahme-Gates pro Implementierungsphase

### Gate 1: Modell und Seed

- beide Datenbanken lassen sich mit derselben Domaene befuellen,
- Referenzqueries liefern fachlich passende Resultate,
- Seed ist deterministisch.

### Gate 2: Showcase

- Aggregate-Read ist fuer beide Datenbanken implementiert,
- Schema-Evolution ist demonstrierbar,
- Modellierungsentscheidungen sind dokumentiert.

### Gate 3: Benchmark

- drei Kernszenarien laufen stabil,
- Exporte sind maschinenlesbar,
- Explain- oder Planpruefung ist vorhanden,
- Wiederholungen und Warmup sind aktiv.

### Gate 4: Ergebnisnutzung

- Resultate sind interpretierbar,
- Graphen lassen sich direkt erzeugen,
- Findings lassen sich in die Praesentation uebernehmen.

---

## 19. Minimaler Umsetzungsplan fuer ein neues Projekt

1. Repo-Grundstruktur anlegen.
2. Konfigurations- und Adapter-Schnittstellen definieren.
3. Produktkatalog-Seed implementieren.
4. PostgreSQL- und MongoDB-Schema aufbauen.
5. Qualitativen Showcase fuer Aggregate und Schema-Evolution erstellen.
6. Kernworkloads implementieren.
7. Validierungs- und Explain-Schicht implementieren.
8. Export- und Auswertungsformat stabilisieren.
9. Dokumentation vervollstaendigen.

## 19.1 Empfohlene Implementierungsreihenfolge innerhalb des Codes

1. Konfigurationsmodell
2. gemeinsame fachliche Seed-Struktur
3. PostgreSQL-Schema und Loader
4. MongoDB-Schema und Loader
5. Referenzqueries fuer Gleichheitspruefung
6. einzelne Workload-Funktionen
7. Runner und Export
8. Validierungs- und Explain-Schicht
9. Statistikverdichtung

---

## 20. Erwartete Projekt-Deliverables

Ein neues Projekt nach dieser Spezifikation muss am Ende mindestens die folgenden Artefakte liefern:

### Dokumentations-Deliverables

- eine klare Forschungsfrage,
- dokumentierte Hypothesen,
- Modellierungsentscheidungen fuer beide Datenbanken,
- eine dokumentierte Experimentmatrix,
- ein Threats-to-Validity-Dokument,
- ein Runbook fuer reproduzierbare Durchlaeufe.

### Code-Deliverables

- lauffaehige Seed-Pipeline,
- zwei funktionierende Datenbankadapter,
- drei implementierte Kernworkloads,
- Validierungs- und Fairness-Checks,
- Export- und Statistikschicht,
- reproduzierbare CLI-Kommandos.

### Ergebnis-Deliverables

- Rohdaten pro Run,
- verdichtete Summary-Dateien,
- mindestens ein Diagramm pro Kernhypothese,
- eine zusammenfassende Findings-Datei.

---

## 21. Definition of Done fuer das neue Testprojekt

Das neue Testprojekt ist erst dann wirklich abgeschlossen, wenn alle folgenden Aussagen gleichzeitig wahr sind:

1. Die drei Kernhypothesen koennen mit echten Messdaten diskutiert werden.
2. Die Ergebnismengen der Referenzqueries sind fachlich geprueft.
3. Die Vergleichsbedingungen sind in Code und Dokumentation konsistent.
4. Die Exporte koennen ohne manuelle Nacharbeit weiterverwendet werden.
5. Die Resultate sind nicht nur gemessen, sondern methodisch eingeordnet.
6. Die Praesentation kann jede grosse Designentscheidung begruenden.

---

## 22. Abschlussbewertung der Soll-Ausrichtung

Dieses Projekt soll ein wissenschaftlich fokussiertes Python-Vergleichsprojekt bleiben, aber inhaltlich vom alten Sensor-/Sharding-Scope weg zu einem fachlich deutlich staerkeren Produktkatalog-Vergleich verschoben werden.

Die wichtigsten konstanten Elemente gegenueber dem alten Projekt sind:

- Python als Hauptsprache,
- direkte DB-Treiber,
- CLI-basierter Ablauf,
- Docker-basierte Reproduzierbarkeit,
- JSON-Exporte,
- klare Trennung zwischen Infrastruktur, Ausfuehrung und Auswertung.

Die wichtigsten Aenderungen gegenueber dem alten Projekt sind:

- neue Domaene,
- neue Forschungsfrage,
- keine clusterzentrierte Hauptnarration,
- staerkerer Fokus auf Modellierungs- und Architekturfragen,
- explizite Fairness- und Validierungsregeln.
