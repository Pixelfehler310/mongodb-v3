# Developer Experience Change Tasks

## Zweck

Dieses Dokument beschreibt, wie der praktische DX-Vergleich aus dem Dual-Backend-Demo-Projekt abgeleitet werden sollte. Der Vergleich soll nicht nur behaupten, dass ein Modell einfacher zu aendern ist, sondern anhand gleicher Aenderungsaufgaben sichtbar machen, wo der Aufwand entsteht.

## Grundregel

Vergleiche nicht "MongoDB-App gegen PostgreSQL-App" pauschal. Vergleiche dieselbe Change-Task in beiden Backend-Implementierungen bei gleichem Frontend-Contract.

## Empfohlene Change-Tasks

1. Neues Evolutionsfeld einfuehren: `regionalTaxCode` wird von optionaler Demo-Eigenschaft zu fachlich relevanter Filter- und Anzeigeeigenschaft.
2. Neuen Produkttyp einfuehren: zum Beispiel `monitor` mit eigenen Attributen.
3. Neue Filtermoeglichkeit einfuehren: zum Beispiel Mindestbewertung aus `latestReviews`.
4. Neue Aggregation einfuehren: zum Beispiel Durchschnittsinventar pro Produkttyp.

## Was pro Task dokumentiert werden sollte

Halte fuer MongoDB und PostgreSQL jeweils fest:

1. betroffene Dateien,
2. betroffene Datenbankartefakte,
3. benoetigte Migrations- oder Seed-Schritte,
4. geaenderte Query-Logik,
5. geaenderte Mapping- oder Hydration-Logik,
6. Testanpassungen,
7. Fehler, die beim Umsetzen aufgetreten sind.

## Commit-Strategie

Die beste praktische Darstellung ist ein Vorher-/Nachher-Commit pro Change-Task.

Empfohlenes Vorgehen:

1. Commit A: stabiler Ausgangszustand der Dual-Backend-Demo.
2. Branch oder Arbeitsabschnitt fuer genau eine Change-Task.
3. Umsetzung der Task in MongoDB und PostgreSQL.
4. Commit B: fertige Change-Task.
5. Auswertung ueber Diff, Dateiliste und kurze qualitative Notizen.

Nutze den Diff aber nicht allein. Eine reine Zahl wie "5 Dateien vs. 9 Dateien" ist zu flach. Erklaere zusaetzlich, warum die Dateien betroffen waren und welche Art von Aufwand darin steckt.

## Geeignete Mess- und Beobachtungspunkte

- Anzahl geaenderter Dateien.
- Anzahl geaenderter Datenbankartefakte.
- Anzahl neuer oder geaenderter Queries.
- Anzahl Mapping-/Hydration-Stellen.
- Notwendigkeit einer Migration.
- Notwendigkeit von Rueckwaertskompatibilitaet.
- Komplexitaet des Tests.
- Subjektiver Stolperpunkt, aber nur als begruendete Beobachtung.

## Darstellung in der Seminararbeit

Eine gute Darstellung kombiniert Tabelle und Erklaertext.

Beispielstruktur:

| Change-Task | MongoDB-Aufwand         | PostgreSQL-Aufwand                         | Interpretation                                                                           |
| ----------- | ----------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Neues Feld  | Seed + Filter + Anzeige | Tabelle/Spalte + Seed + Hydration + Filter | MongoDB ist flexibler bei optionaler Evolution, PostgreSQL expliziter und kontrollierter |

Danach sollte ein kurzer Absatz folgen, der die wichtigste Ursache erklaert: Dokumentlokalitaet, Normalisierung, Polymorphie, Migration oder Mapping-Aufwand.

## Wichtigste Einschraenkung

Der DX-Vergleich ist kein universeller Beweis, sondern ein kontrollierter Praxisvergleich fuer diese Domaene, diesen Contract und diese Change-Tasks.
