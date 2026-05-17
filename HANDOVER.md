# Handover fuer das Wissenschafts-Repo

Dieses Dokument beschreibt den Soll-Kontext fuer die weitere Arbeit an `mongodb-v2`.

Es geht nicht darum, den historischen Zustand des Repos zu konservieren. Es geht darum, einen klaren Handover fuer den neuen Zielzustand zu liefern.

## 1. Akademischer Kontext

Das Repository ist Teil einer Seminararbeit im Masterstudium fuer das Modul NoSQL-Datenbanken.

Die Arbeit soll nicht den Umfang einer Abschlussarbeit simulieren. Sie soll stattdessen eine eng gescopte, methodisch nachvollziehbare und praesentationsstarke Vergleichsarbeit liefern.

## 2. Rolle dieses Repos

`mongodb-v2` ist das wissenschaftliche Hauptrepo der Seminararbeit.

Es soll die belastbaren Aussagen tragen zu:

- Forschungsfrage,
- Hypothesen,
- Modellierungsentscheidungen,
- Fairness des Vergleichs,
- Benchmarking,
- Ergebnisinterpretation.

Das Repo ist nicht der visuelle Demo-Showcase. Diese Rolle liegt im separaten Repo `mongodb_demo`.

## 3. Neue Leitfrage

Die neue Leitfrage lautet sinngemaess:

> Unter welchen fachlichen und technischen Bedingungen liefert ein dokumentenorientiertes Modell in MongoDB gegenuber einem relationalen Modell in PostgreSQL Vorteile bei Polymorphie, Datenlokalitaet, Schema-Evolution und operativer Performance, und wann ist das relationale Modell im Vorteil?

Wichtig ist die Verschiebung des Scopes:

- weg von Sensor-Events,
- weg von einer sharding-zentrierten Haupterzaehlung,
- hin zu einem Modellierungs- und Architekturvergleich mit empirischer Absicherung.

## 4. Neue Zieldomaene

Die Domaene ist ein polymorpher Produktkatalog.

Kernbestandteile:

- Produkte mit gemeinsamen Basisattributen,
- produktspezifische Attribute je Produkttyp,
- Varianten,
- Kategorien,
- Hersteller,
- Bewertungen,
- eine dokumentierte Evolutionsstufe mit `regional_tax_code`.

Die Domaene soll sowohl fuer den qualitativen Showcase als auch fuer den quantitativen Benchmark gelten.

## 5. Zielarchitektur des Repos

Das Repo soll kuenftig zwei klar getrennte Bereiche haben:

### A. Qualitativer Architektur-Showcase

Zweck:

- Vergleich der Modellierung in MongoDB und PostgreSQL,
- Sichtbarmachung von Mapping-Aufwand,
- Vergleich von Aggregate-Reads,
- Vergleich von Schema-Evolution.

### B. Quantitative Benchmark-Suite

Zweck:

- reproduzierbare Messung definierter Kernworkloads,
- Auswertung ueber standardisierte Metriken,
- Export von Roh- und Summary-Daten,
- methodisch saubere Interpretation.

## 6. Ziel-Workloads

Das Repo soll sich auf drei Kernworkloads konzentrieren:

1. kompletter Produkt-Aggregat-Read,
2. Kategorie-Umbenennung unter Denormalisierung,
3. analytische Query ueber Produkte, Hersteller und Bewertungen.

Optional koennen spaeter Topologie- oder Skalierungsszenarien hinzukommen. Diese sollen aber nicht mehr die Hauptaussage dominieren.

## 7. Was aus dem Altbestand bleibt

Wiederverwendbar bleiben voraussichtlich:

- Python-CLI-Grundidee,
- Adapter-Schicht,
- Exportgedanke,
- Teile der Metrikberechnung,
- Docker-basierte lokale Reproduzierbarkeit.

Nicht mehr zielkonform als Hauptlinie sind:

- Sensor-Event-Domaene,
- regionszentrierte Lastlogik,
- clusterzentrierte Haupterzaehlung,
- die bisherigen T1-T4 als finaler Kernbeleg.

## 8. Verbindliche Referenzdokumente

Beim weiteren Umbau gelten diese Dateien als fachliche Leitdokumente:

- `ANALYSE_KONZEPTVERGLEICH.md`
- `ZIELSTRUKTUR_SEMINARARBEIT.md`
- `SEMINARARBEIT_TESTPROJEKT_SPEZIFIKATION.md`

## 9. Erwartung an die weitere Arbeit

Die weitere Arbeit im Repo soll:

- den Scope enger und besser verteidigbar machen,
- die Fairness des Vergleichs explizit absichern,
- qualitative und quantitative Aussagen sauber trennen,
- und am Ende direkt in eine Seminarpraesentation ueberfuehrbar sein.