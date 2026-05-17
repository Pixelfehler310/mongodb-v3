# MongoDB Produktkatalog Demo

Dieses Repository ist das Demo- und Showcase-Repo der Seminararbeit im Modul NoSQL-Datenbanken.

Es dient nicht als wissenschaftlicher Hauptbeleg. Es dient dazu, MongoDB anhand eines kleinen, praesentationsfreundlichen Produktkatalogs anschaulich zu erklaeren.

## Rolle dieses Repos

`mongodb_demo` ist das visuelle Gegenstueck zum Wissenschafts-Repo `mongodb-v2`.

Es soll in der Praesentation zeigen:

- wie ein realistisches Produktdokument in MongoDB aussieht,
- wie polymorphe Produkttypen in einer Collection sichtbar werden,
- wie Filter auf verschachtelte Felder und Arrays wirken,
- wie Query und PyMongo-Code aus derselben UI-Aktion ableitbar sind,
- wie einfache Aggregationen praesentierbar erklaert werden koennen.

## Was dieses Repo nicht leisten soll

Dieses Repo ist nicht gedacht fuer:

- fairen SQL-vs.-MongoDB-Vergleich,
- Lasttests,
- wissenschaftliche Evidenzgewinnung,
- Produktionshaertung,
- grosse Fullstack-Architektur.

## Ziel-Domaene

Die Domaene ist ein vereinfachter Produktkatalog mit:

- Laptops,
- T-Shirts,
- Buechern,
- Smartphones,
- Schreibtischen.

Produkte besitzen gemeinsame Felder und typspezifische Attribute. Zusaetzlich sollen eingebettete Bereiche wie Varianten, Highlights oder letzte Bewertungen sichtbar sein.

## Ziel-Flow der Demo

Ein Presenter soll in wenigen Minuten zeigen koennen:

1. eine Produktliste,
2. mehrere Produkttypen in derselben Collection,
3. ein vollstaendiges Dokument,
4. die dazugehoerige MongoDB-Query,
5. den passenden PyMongo-Code,
6. mindestens eine einfache Aggregation,
7. optional einen kleinen Live- oder Evolutions-Effekt.

## Technologie-Rahmen

Die Demo bleibt absichtlich nah am aktuellen Stack:

- Python 3.11+
- Flask
- PyMongo
- HTML
- CSS
- Vanilla JavaScript
- Docker Compose fuer lokales MongoDB

## Verbindliche Zielreferenz

Die neue Detail-Spezifikation liegt in:

- `SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md`

Die Anforderungen fuer das Demo-Repo sind in:

- `DEMO_PROJECT_REQUIREMENTS.md`

beschrieben.

## Umgang mit dem aktuellen Bestand

Der aktuelle Codebestand kann noch historische Sensor-Event-Artefakte enthalten. Diese sind nicht mehr die fachliche Zielrichtung. Das Repo soll kuenftig konsistent auf die Produktkatalog-Domaene ausgerichtet werden.