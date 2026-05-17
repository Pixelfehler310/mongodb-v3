# Zielstruktur fuer das Gesamtprojekt

## Zweck dieses Dokuments

Dieses Dokument definiert die fachliche, technische und organisatorische Zielstruktur fuer das Gesamtprojekt. Es beschreibt den Soll-Zustand, nicht den aktuellen Ist-Zustand.

Der Fokus liegt auf dem bestmoeglichen Endergebnis fuer eine Seminararbeit mit Praesentation im Modulkontext:

- wissenschaftlich belastbar,
- fachlich klar gescoped,
- praesentationsstark,
- methodisch verteidigbar,
- technisch reproduzierbar.

Die Zielstruktur folgt der vorherigen Analyse in `ANALYSE_KONZEPTVERGLEICH.md` und setzt das neue Konzept als Hauptlinie des Projekts.

---

## Leitentscheidung

Das Gesamtprojekt soll kuenftig aus zwei klar getrennten, aber eng verbundenen Teilen bestehen:

1. einem wissenschaftlichen Hauptprojekt fuer Architekturvergleich und Benchmarking,
2. einem didaktischen Demo-Projekt fuer die Praesentation.

Dabei gilt:

- `mongodb-v2` wird das wissenschaftliche Hauptrepo.
- `mongodb_demo` bleibt das Demo- und Showcase-Repo.
- Beide Repos nutzen dieselbe fachliche Domaene als roten Faden.
- Die Domaene wechselt von Sensor-Events auf einen polymorphen Produktkatalog.

Damit wird das Gesamtprojekt inhaltlich konsistent: Dieselben fachlichen Objekte tauchen in Architektur-Showcase, Benchmarking und Demo auf.

---

## Zielbild auf hoechster Ebene

## Repo 1: `mongodb-v2`

Rolle:

- wissenschaftliches Kernrepo,
- Quelle der Forschungsfrage,
- Quelle des Datenmodells,
- Quelle der Benchmark-Methodik,
- Quelle der Messergebnisse,
- Quelle der Dokumentation fuer Architektur- und Testdesign.

Inhaltlich soll dieses Repo zwei sauber getrennte Arbeitsstraenge enthalten:

1. Qualitativer Architektur-Showcase
2. Quantitative Benchmark-Suite

## Repo 2: `mongodb_demo`

Rolle:

- praesentationsnahes Demo-Repo,
- visuelle und interaktive Erklaerung des Dokumentmodells,
- UI-gestuetzter Showcase fuer Queries, Dokumente und Aggregationen,
- keine primaere wissenschaftliche Evidenz.

Dieses Repo darf kleiner, anschaulicher und didaktischer sein. Es darf aber nicht die methodische Hauptlast des Projekts tragen.

---

## Ziel-Forschungsfrage

Die Zielstruktur basiert auf einer klaren Forschungsfrage:

> Unter welchen fachlichen und technischen Bedingungen liefert ein dokumentenorientiertes Modell in MongoDB gegenueber einem relationalen Modell in PostgreSQL Vorteile bei Polymorphie, Datenlokalitaet, Schema-Evolution und operativer Performance, und unter welchen Bedingungen ist das relationale Modell ueberlegen?

Wichtig daran ist die Trennung von vier Ebenen:

1. Datenmodellierung
2. Entwickleraufwand und Aenderbarkeit
3. Lese- und Schreibverhalten
4. technische Ausfuehrung unter Last

Die Zielstruktur muss genau diese vier Ebenen sichtbar machen.

---

## Ziel-Domaene

Die gemeinsame Zieldomaene ist ein vereinfachter E-Commerce-Produktkatalog mit polymorphen Produkttypen.

Beispiele fuer Produkttypen:

- Laptop
- T-Shirt
- Buch
- Smartphone
- Schreibtisch

Gemeinsame Basisattribute:

- `product_id`
- `sku`
- `name`
- `base_price`
- `manufacturer`
- `category_refs`
- `created_at`
- `updated_at`
- `regional_tax_code` ab der Evolutionsstufe 2

Produktspezifische Attribute:

- Laptop: CPU, RAM, Storage, GPU
- T-Shirt: Groesse, Material, Farbe, Fit
- Buch: Autor, ISBN, Seitenzahl, Sprache
- Smartphone: SoC, Display, Akku, Kamera
- Schreibtisch: Material, Breite, Hoehe, Belastbarkeit

Zusaetzliche fachliche Komponenten:

- Varianten
- Kategorien
- Kundenbewertungen
- Herstellerdaten
- optionale Bestellhistorien fuer quantitative Szenarien

Diese Domaene ist gesetzt und soll in beiden Repos konsistent verwendet werden.

---

## Zielprinzipien fuer die Gesamtstruktur

## 1. Eine Domaene, zwei Repo-Rollen

Es darf keine fachliche Fragmentierung mehr geben. Wenn die Arbeit den Produktkatalog untersucht, dann sollen Demo, Architekturvergleich und Benchmarking alle dieselbe Domaene benutzen.

## 2. Qualitativ und quantitativ strikt trennen

Der qualitative Teil soll nicht mit Durchsatzmetriken ueberladen werden. Der quantitative Teil soll nicht mit UI- oder Demo-Aspekten vermischt werden.

## 3. Wissenschaftliche Fairness vor Demo-Effekt

Die Zielstruktur muss so gebaut sein, dass keine Datenbank durch Treiberverhalten, Locking, Pooling oder unfaire Modellierung kuenstlich bevorzugt wird.

## 4. Dokumentation ist Teil des Systems

Die Arbeit ist nicht nur der Code. Die Zielstruktur muss die Forschungsfrage, Hypothesen, Modellierungsannahmen, Metriken und Auswertungsregeln explizit als versionierte Dokumente enthalten.

## 5. Demo ist Begleiter, nicht Beweis

Das Demo-Repo soll Dinge erklaeren. Die Benchmark-Suite soll Dinge belegen.

---

## Zielstruktur fuer `mongodb-v2`

Das Repo `mongodb-v2` soll zum zentralen Wissenschafts-Repo werden.

## Ziel-Ordnerbaum

```text
mongodb-v2/
  README.md
  HANDOVER.md
  RESEARCH_QUESTION.md
  HYPOTHESES.md
  MODELLING_DECISIONS.md
  METRICS_AND_METHODS.md
  PRESENTATION_STORYLINE.md
  ZIELSTRUKTUR_SEMINARARBEIT.md

  docs/
    architecture/
      qualitative-showcase.md
      quantitative-benchmarking.md
      repository-boundaries.md
      comparison-fairness.md
    data-model/
      domain-overview.md
      mongodb-model.md
      postgres-model.md
      schema-evolution.md
      indexing-strategy.md
    experiments/
      experiment-matrix.md
      warmup-and-cache-policy.md
      runbook.md
      threat-to-validity.md
    results/
      result-interpretation-template.md
      graph-guidelines.md
      findings-summary.md

  showcase/
    README.md
    common/
      models.py
      fixtures.py
      scenarios.py
    mongodb/
      repository.py
      models.py
      examples.py
    postgres/
      repository.py
      models.py
      migrations/
      ddl/
    comparisons/
      aggregate-read.md
      schema-evolution.md
      dx-change-task.md

  benchmark/
    README.md
    config.py
    runner.py
    metrics.py
    statistics.py
    export.py
    models.py
    workload_catalog.py
    fairness_checks.py
    adapters/
      base.py
      mongo_adapter.py
      postgres_adapter.py
      connection_profiles.py
    seed/
      generator.py
      fixtures.py
      distributions.py
    workloads/
      read_locality.py
      denormalized_update.py
      join_lookup_comparison.py
      optional_scaling.py
    scenarios/
      baseline_single_node.py
      benchmark_read_advantage.py
      benchmark_update_anomaly.py
      benchmark_join_bottleneck.py
    validation/
      explain_plans.py
      index_checks.py
      dataset_checks.py
    tests/
      test_metrics.py
      test_seed_consistency.py
      test_workload_definitions.py
      test_query_semantics.py

  infra/
    README.md
    compose/
      docker-compose.postgres.yml
      docker-compose.mongo-single.yml
      docker-compose.mongo-sharded.yml
    scripts/
      init-postgres.sql
      init-mongo.js
      bootstrap-cluster.js
      reset-state.ps1
      collect-stats.ps1

  exports/
    raw/
    processed/
    charts/

  state/
    manifests/
    run-history/

  requirements.txt
  package.json
  projects.json
```

---

## Bedeutung der Hauptbereiche in `mongodb-v2`

## Root-Dokumente

Die Root-Ebene soll nicht aus allgemeinen Texten bestehen, sondern aus den Dokumenten, die ein Gutachter oder ein Mitstudent sofort braucht.

### `README.md`

Zweck:

- Einstieg ins Repo,
- Schnellstart,
- kurze Projektdefinition,
- Verweis auf die wissenschaftlichen Kerndokumente.

Nicht in die README gehoeren:

- tiefe Methodikdiskussionen,
- lange theoretische Begruendungen,
- experimentelle Detailmatrizen.

### `HANDOVER.md`

Zweck:

- Gesamtkontext,
- akademische Einordnung,
- Erwartung an Neuaufsetzer oder spaetere Bearbeiter.

### `RESEARCH_QUESTION.md`

Zweck:

- exakte Forschungsfrage,
- Abgrenzung gegen falsche Vergleichsfragen,
- Definition des Geltungsbereichs.

### `HYPOTHESES.md`

Zweck:

- explizite Hypothesen pro Teilprojekt,
- jeweils mit Begruendung,
- erwarteten Metriken,
- moeglichen Gegenbeobachtungen.

### `MODELLING_DECISIONS.md`

Zweck:

- exakte Festlegung, was in MongoDB eingebettet und was referenziert wird,
- exakte Festlegung, wie PostgreSQL modelliert wird,
- Begruendung jeder relevanten Modellierungsentscheidung,
- explizite Dokumentation, was absichtlich nicht verglichen wird.

Dieses Dokument ist zentral fuer die wissenschaftliche Fairness.

### `METRICS_AND_METHODS.md`

Zweck:

- Definition aller Metriken,
- Wiederholungslogik,
- Warmup-Regeln,
- Cache-Policy,
- Auswertungsvorgehen,
- Grenzen der Aussagekraft.

### `PRESENTATION_STORYLINE.md`

Zweck:

- verdichtete Story fuer die Praesentation,
- Reihenfolge der Argumente,
- Verweis auf Demo, Showcase und Benchmark.

---

## Bereich `docs/`

Der Bereich `docs/` ist die eigentliche Wissensbasis des Repos.

### `docs/architecture/`

Enthaelt die Systemstruktur.

- `qualitative-showcase.md`: Aufbau und Ziel des Architektur-Showcase.
- `quantitative-benchmarking.md`: Aufbau und Ziel der Benchmark-Suite.
- `repository-boundaries.md`: klare Verantwortungen zwischen Repos und Modulen.
- `comparison-fairness.md`: Regeln fuer einen fairen Vergleich.

### `docs/data-model/`

Enthaelt die Domaenen- und Modellspezifikation.

- `domain-overview.md`: Produktkatalog, Entitaeten, Beziehungen.
- `mongodb-model.md`: Dokumentstruktur, Einbettung, Referenzen, Indizes.
- `postgres-model.md`: Tabellen, Normalisierung, Migrationsregeln, Indizes.
- `schema-evolution.md`: Evolutionsstufen, Pflichtfeld-Strategie, Rueckwaertskompatibilitaet.
- `indexing-strategy.md`: welche Indizes erlaubt sind und warum.

### `docs/experiments/`

Enthaelt die exakte Versuchsmethodik.

- `experiment-matrix.md`: alle Testfaelle und Parameter.
- `warmup-and-cache-policy.md`: wie Cache-Effekte kontrolliert werden.
- `runbook.md`: wie ein kompletter Messlauf reproduzierbar durchgefuehrt wird.
- `threat-to-validity.md`: bekannte Risiken, Bias und Einschraenkungen.

### `docs/results/`

Enthaelt Regeln fuer Ergebnisinterpretation.

- `result-interpretation-template.md`: standardisierte Ergebnisdiskussion.
- `graph-guidelines.md`: welche Diagramme wie genutzt werden.
- `findings-summary.md`: laufend aktualisierte verdichtete Befunde.

---

## Bereich `showcase/`

Dieser Bereich bildet den qualitativen Architekturvergleich ab. Er ist kein UI-Projekt und kein Lasttestprojekt.

Sein Zweck ist, dieselben fachlichen Use Cases in zwei Modellwelten direkt gegeneinanderzustellen.

## Zielinhalte von `showcase/`

### `showcase/common/`

Gemeinsame fachliche Artefakte:

- kanonische Beispieldaten,
- gemeinsame Use-Case-Beschreibungen,
- definierte Aenderungsszenarien.

### `showcase/mongodb/`

Zeigt die MongoDB-Seite des Architekturvergleichs:

- Dokumentmodell,
- Repository-Operationen,
- Beispielqueries,
- einfache Aggregationen,
- Behandlung von Schema-Evolution.

### `showcase/postgres/`

Zeigt die PostgreSQL-Seite des Architekturvergleichs:

- relationale Tabellenstruktur,
- DDL,
- Migrationen,
- Repositories oder Query-Implementierungen,
- notwendige Join- und Mapping-Logik.

### `showcase/comparisons/`

Verdichtete Gegenueberstellungen, jeweils als didaktische Artefakte:

- `aggregate-read.md`: kompletter Produkt-Aggregat-Read in beiden Welten.
- `schema-evolution.md`: Einfuehrung von `regional_tax_code`.
- `dx-change-task.md`: Vergleich einer vordefinierten Aenderungsaufgabe.

## Mindest-Use-Cases des qualitativen Showcase

Der qualitative Teil muss mindestens diese drei Use Cases enthalten:

1. Speichern polymorpher Produkte.
2. Laden eines kompletten Produkt-Aggregats mit Varianten, Kategorien und letzten Bewertungen.
3. Einfuehrung eines neuen Pflichtfelds im laufenden Projekt.

Optional kann ein vierter Use Case hinzukommen:

4. Erweiterung um einen neuen Produkttyp ohne Rueckbau bestehender Strukturen.

---

## Bereich `benchmark/`

Dieser Bereich enthaelt ausschliesslich die quantitative Evidenz.

## Zielanforderungen fuer `benchmark/`

### 1. Keine asymmetrische Concurrency

PostgreSQL und MongoDB muessen mit fairer, definierter Connection- und Pooling-Strategie betrieben werden. Keine Seite darf clientseitig kuenstlich serialisiert werden.

### 2. Gleiche fachliche Semantik

Ein Workload muss auf beiden Seiten fachlich dasselbe tun. Nicht nur "aehnlich", sondern kontrolliert dasselbe.

### 3. Getrennte Workload-Definition und Workload-Ausfuehrung

Workload-Bedeutung gehoert in `workload_catalog.py` oder `workloads/`, Ausfuehrung in Runner und Szenarien.

### 4. Validierung ist Teil des Benchmarking

Zu jedem wichtigen Lauf soll geprueft werden:

- existieren die erwarteten Indizes,
- ist das Dataset vollstaendig,
- treffen Queries fachlich denselben Datenausschnitt,
- sind Explain- oder Ausfuehrungsplaene plausibel.

## Ziel-Workloads

### `workloads/read_locality.py`

Vergleicht den Abruf komplexer Produktaggregate.

Messziel:

- Latenzvorteil oder -nachteil durch Datenlokalitaet.

### `workloads/denormalized_update.py`

Vergleicht Aenderungen an vielfach referenzierten oder duplizierten Kategorien.

Messziel:

- Kosten von Denormalisierung gegenueber zentraler Normalisierung.

### `workloads/join_lookup_comparison.py`

Vergleicht analytisch angehauchte Queries mit mehreren fachlichen Beziehungen.

Messziel:

- Unterschiede zwischen SQL-Joins und MongoDB-`$lookup` bzw. alternativen Modellierungsstrategien.

### `workloads/optional_scaling.py`

Optionaler Zusatzbereich.

Dieser Bereich darf erst spaeter kommen und nur dann, wenn die drei Kernworkloads sauber stehen. Er kann Topologie- oder Skalierungsfragen enthalten, aber nicht mehr die Hauptfrage dominieren.

## Ziel-Szenarien

### `scenarios/baseline_single_node.py`

Fairer Baseline-Vergleich ohne Cluster-Vorteil.

### `scenarios/benchmark_read_advantage.py`

Entspricht TS-01 aus dem neuen Konzept.

### `scenarios/benchmark_update_anomaly.py`

Entspricht TS-02 aus dem neuen Konzept.

### `scenarios/benchmark_join_bottleneck.py`

Entspricht TS-03 aus dem neuen Konzept.

---

## Bereich `infra/`

Die Infrastruktur dient der Reproduzierbarkeit, nicht der Argumentation.

Ziel:

- alle benoetigten Topologien startbar,
- initiale Struktur automatisiert,
- klare Reset-Skripte,
- definierte Statistik-Erfassung.

## Zielrolle der Compose-Dateien

- `docker-compose.postgres.yml`: PostgreSQL fuer Showcase und Benchmark.
- `docker-compose.mongo-single.yml`: MongoDB Single Node fuer fairen Basisvergleich.
- `docker-compose.mongo-sharded.yml`: nur fuer optionale Topologie- und Skalierungsfragen.

Wichtig:

Der Sharded Cluster ist nicht mehr das Zentrum des Projekts. Er ist nur noch ein optionaler Spaetbaustein.

---

## Bereich `exports/`

Die Exporte muessen sauber getrennt werden.

### `exports/raw/`

Unveraenderte Messergebnisse je Lauf.

### `exports/processed/`

Verdichtete, aggregierte und fuer Diagramme vorbereitete Daten.

### `exports/charts/`

Diagramme fuer Praesentation und Arbeit.

Die Exportstruktur soll verhindern, dass ad hoc erzeugte JSON-Dateien ungeordnet im Repo liegen.

---

## Bereich `state/`

Dieser Bereich dient dem Laufzustand und der Reproduzierbarkeit.

### `state/manifests/`

Laufkonfigurationen und Manifestdateien pro Messserie.

### `state/run-history/`

Metadaten ueber durchgefuehrte Runs.

Der Bereich soll klein bleiben. Er ist Hilfsmittel, nicht Wissensspeicher.

---

## Zielstruktur fuer `mongodb_demo`

Das Repo `mongodb_demo` bleibt eigenstaendig, wird aber fachlich auf dieselbe Produktkatalog-Domaene umgestellt.

## Ziel-Ordnerbaum

```text
mongodb_demo/
  README.md
  DEMO_SCOPE.md
  DEMO_FLOW.md

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

## Zielrolle des Demo-Repos

Das Demo-Repo soll genau diese Dinge sichtbar machen:

1. Produktdokumente mit polymorphen Attributen.
2. Filter auf Basisfeldern, verschachtelten Feldern und Arrays.
3. Ansicht des kompletten Dokuments.
4. Anzeige der MongoDB-Query.
5. Anzeige des passenden PyMongo-Codes.
6. mindestens eine einfache Aggregation.

Es soll nicht leisten:

- fairen SQL-vs.-MongoDB-Vergleich,
- Lasttests,
- wissenschaftliche Beweisfuehrung,
- Topologievergleiche.

## Empfohlene Demo-Ansichten

### Hauptansicht

Zeigt:

- Produktliste,
- Filterpanel,
- Dokumentdetails,
- Query-Panel,
- Code-Panel,
- Aggregationspanel.

### Optionaler Evolutions-View

Kann zeigen:

- wie neue Produkte mit `regional_tax_code` aussehen,
- wie alte Dokumente noch lesbar bleiben,
- wie Schema-Evolution in MongoDB auf UI-Ebene erklaert werden kann.

Wenn diese Ansicht die Demo ueberlaedt, ist sie verzichtbar.

---

## Ziel-Schnittstelle zwischen beiden Repos

Auch wenn beide Repos getrennt bleiben, muessen sie konsistent gekoppelt sein.

## Gemeinsame fachliche Artefakte

Beide Repos muessen dieselben fachlichen Begriffe benutzen:

- Produkttypen,
- Kategorien,
- Varianten,
- Hersteller,
- Bewertungen,
- `regional_tax_code`.

## Gemeinsame Erzaehlstruktur

Die Praesentation soll logisch durch beide Repos fuehren:

1. Problem und Domaene erklaeren.
2. Dokumentmodell in der Demo zeigen.
3. Architekturvergleich im Showcase zeigen.
4. Quantitative Belege aus `mongodb-v2` zeigen.
5. Grenzen und Einordnung benennen.

## Unterschiedliche Rollen klar markieren

Die Demo beantwortet die Frage:

- "Wie sieht dieses Modell in MongoDB praktisch aus?"

Das Wissenschafts-Repo beantwortet die Frage:

- "Wann und warum ist dieses Modell gegenueber einer relationalen Alternative fachlich oder technisch besser oder schlechter?"

---

## Ziel-Artefakte fuer die Endpraesentation

Am Ende soll die Struktur nicht nur guten Code enthalten, sondern klar auswertbare Artefakte liefern.

## Fachliche Artefakte

- Domaenenmodell
- Vergleichsschemata fuer MongoDB und PostgreSQL
- dokumentierte Evolutionsstufen
- klare Use-Case-Beschreibungen

## Wissenschaftliche Artefakte

- Forschungsfrage
- Hypothesen
- Experimentmatrix
- Threats to Validity
- Metrikdefinitionen
- reproduzierbare Runbooks
- auswertbare Messergebnisse

## Praesentationsartefakte

- visuelle Demo
- kompakte Gegenueberstellungsseiten fuer Architekturvergleiche
- exportierte Diagramme
- zusammenfassende Findings fuer jede Hypothese

---

## Ziel-Umgang mit dem aktuellen Bestand

Nicht alles im aktuellen Repo ist falsch. Der vorhandene Bestand soll selektiv uebernommen werden.

## In `mongodb-v2` voraussichtlich uebernehmbar

- generelle CLI- und Export-Idee,
- Teile der Runner-Struktur,
- Teile der Metrics-Berechnung,
- Docker-basierte Reproduzierbarkeit,
- Grundidee einer Adapter-Schicht.

## In `mongodb-v2` nicht zielkonform als Hauptlinie

- Sensor-Event-Domaene,
- Regionszentrierte Testlogik,
- sharding-zentrierte Hauptnarration,
- aktuelle T1 bis T4 als Kernbenchmark,
- methodisch asymmetrische Parallelitaet.

## In `mongodb_demo` voraussichtlich uebernehmbar

- einfacher Python-Backend-Ansatz,
- Query- und Codeanzeige,
- klare Repository-Struktur,
- deterministisches Seeding,
- einfache und praesentationsfreundliche UI.

## In `mongodb_demo` fachlich umzubauen

- Domaene von Sensor-Events auf Produktkatalog,
- Filterlogik auf Produktattribute,
- Detailansicht auf polymorphe Produkte,
- Aggregationen auf fachlich passende Produktdaten.

---

## Nicht-Ziele der Zielstruktur

Die Zielstruktur soll explizit nicht in diese Richtungen abdriften:

- kein Fullstack-Produkt mit Produktivanspruch,
- kein allgemeines E-Commerce-System,
- kein Kubernetes- oder Cloud-Projekt,
- kein generischer DB-Benchmark ueber beliebige Domaenen,
- kein unfairer Strohmann-Vergleich,
- kein erneutes Vermischen von Demo, Architekturvergleich und Lasttest.

---

## Qualitaetskriterien fuer den Soll-Zustand

Die Zielstruktur ist erst dann erreicht, wenn alle folgenden Aussagen wahr sind:

1. Beide Repos verwenden dieselbe fachliche Domaene.
2. Der qualitative und der quantitative Teil sind sauber getrennt.
3. Die Benchmark-Suite vergleicht fachlich denselben Workload in beiden Datenbanken.
4. Treiber-, Pooling- und Concurrency-Verhalten sind fair kontrolliert.
5. Schema-Evolution und DX sind operationalisiert und nicht nur erzaehlt.
6. Die Demo unterstuetzt die Geschichte, ersetzt aber nicht die Evidenz.
7. Die Praesentation kann das Ergebnis ohne methodische Ausweichmanoever verteidigen.

---

## Schlussbild

Die Zielstruktur soll das Gesamtprojekt von einer technisch interessanten, aber methodisch noch diffusen MongoDB-vs.-PostgreSQL-Uebung in ein fachlich konsistentes, wissenschaftlich deutlich staerkeres Vergleichsprojekt ueberfuehren.

Der Soll-Zustand ist erreicht, wenn:

- `mongodb-v2` das belastbare Wissenschafts-Repo ist,
- `mongodb_demo` das didaktische Showcase-Repo ist,
- beide denselben Produktkatalog untersuchen,
- und Benchmark, Architekturvergleich und Demo endlich dieselbe Geschichte erzaehlen.
