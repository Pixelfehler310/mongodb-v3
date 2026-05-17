# MongoDB vs. PostgreSQL - Seminararbeit NoSQL-Datenbanken

Dieses Repository ist das wissenschaftliche Kernrepo einer Seminararbeit im Modul NoSQL-Datenbanken. Es wird auf ein fokussiertes Vergleichsprojekt mit polymorphem Produktkatalog ausgerichtet.

Das Ziel ist nicht mehr, primar einen MongoDB-Sharded-Cluster gegen einen PostgreSQL-Single-Node auf Basis von Sensor-Events zu benchmarken. Das Ziel ist ein fachlich sauberer Vergleich zwischen dokumentenorientierter und relationaler Modellierung entlang von vier Kernfragen:

- Polymorphie im Datenmodell
- Datenlokalitaet bei komplexen Aggregaten
- Kosten von Denormalisierung und Schema-Evolution
- Grenzen von Joins, Lookups und stark vernetzten Lesezugriffen

## Rolle dieses Repos

`mongodb-v2` ist das Wissenschafts-Repo. Es soll die belastbaren Aussagen der Seminararbeit tragen:

- Forschungsfrage
- Hypothesen
- Modellierungsentscheidungen
- Benchmark-Methodik
- Messdaten und Auswertung

Das Repo ist nicht als Webanwendung gedacht. Es ist ein Python-basiertes Vergleichs- und Benchmark-Projekt mit reproduzierbarer Infrastruktur.

## Wichtige Zieldokumente

Die folgenden Dateien definieren den neuen Zielzustand:

- `ANALYSE_KONZEPTVERGLEICH.md`
- `ZIELSTRUKTUR_SEMINARARBEIT.md`
- `SEMINARARBEIT_TESTPROJEKT_SPEZIFIKATION.md`

Diese Dokumente sind fuer den Neuaufbau und die fachliche Ausrichtung wichtiger als der historische Altbestand im Repo.

## Neue Zielrichtung

Die Ziel-Domaene ist ein vereinfachter E-Commerce-Produktkatalog mit:

- polymorphen Produkttypen,
- Varianten,
- Kategorien,
- Herstellern,
- Bewertungen,
- einer dokumentierten Schema-Evolution ueber `regional_tax_code`.

Das Projekt soll zwei sauber getrennte Bereiche enthalten:

1. einen qualitativen Architektur-Showcase,
2. eine quantitative Benchmark-Suite.

## Ziel-Repo-Struktur

Im Zielzustand konzentriert sich das Repo auf diese Hauptbereiche:

- `showcase/` fuer den qualitativen Architekturvergleich,
- `benchmark/` fuer reproduzierbare Last- und Vergleichsmessungen,
- `infra/` fuer lokales Setup und Resetbarkeit,
- `exports/` fuer Rohdaten, Summarys und Diagramme,
- Root-Dokumente fuer Forschungsfrage, Hypothesen und Methodik.

Die komplette Zielstruktur ist in `ZIELSTRUKTUR_SEMINARARBEIT.md` beschrieben.

## Technologie-Rahmen

Die neue Ausrichtung bleibt absichtlich nah am aktuellen Technologie-Stack:

- Python 3.11+
- `pymongo`
- `psycopg2-binary`
- `rich`
- `python-dotenv`
- `faker`
- `numpy`
- `pytest`

Nicht Teil des Zielprojekts sind:

- ORMs,
- Web-Frameworks als Benchmark-Kern,
- Frontend-Logik,
- generische Middleware oder Eventing-Plattformen.

## Umgang mit dem aktuellen Bestand

Der aktuelle Codebestand enthaelt noch historische Artefakte aus dem alten Sensor- und Sharding-Scope. Diese sind als Vorstufe oder technische Ausgangsbasis zu verstehen, nicht als finaler wissenschaftlicher Zielzustand.

Wenn du dieses Repo fuer die Seminararbeit weiterentwickelst, orientiere dich an den neuen Zieldokumenten und nicht an der alten inhaltlichen Rahmung.

## Naechste Prioritaeten

1. Root-Dokumente und Methodik konsolidieren.
2. Produktkatalog-Domaene als gemeinsames Zielmodell fixieren.
3. Qualitativen Showcase definieren.
4. Benchmark-Kernszenarien neu aufsetzen.
5. Mess- und Exportpfade standardisieren.