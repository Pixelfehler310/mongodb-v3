# Praesentationsfolien: Inhalt und Darstellung

## Zweck dieses Dokuments

Diese zweite Struktur ist nicht fuer den gesprochenen Vortrag gedacht, sondern nur fuer die Folien selbst.

Der Fokus liegt auf zwei Fragen:

1. Welche Stichpunkte sollen auf die jeweilige Folie?
2. Wie sollte die Folie visuell aufgebaut sein, damit sie klar, ruhig und professionell wirkt?

Die Grundregel lautet:

> Pro Folie nur eine Kernidee, wenige Stichpunkte und eine visuelle Form, die die Aussage sofort lesbar macht.

---

## Uebergeordnete Gestaltungsregeln

### Was auf allen Folien gelten sollte

- pro Folie nur eine Hauptaussage
- maximal 3 bis 5 Stichpunkte
- keine ganzen Saetze in den Stichpunkten
- wichtige Begriffe visuell hervorheben
- lieber Kontrast und Struktur statt viel Text
- gleiche visuelle Logik auf allen Folien beibehalten

### Sinnvolle Layout-Regeln

- Titel oben links
- darunter kurze Unterzeile oder Leitfrage, wenn noetig
- Hauptinhalt in 2-Spalten-Layout oder als einfache Vergleichstabelle
- viel Weissraum lassen
- MongoDB und PostgreSQL farblich konsistent markieren

Empfehlung:

- MongoDB immer in Gruen
- PostgreSQL immer in Blau
- neutrale Aussagen in Dunkelgrau oder Schwarz

### Was du vermeiden solltest

- volle Textfolien
- zu viele Tabellen auf einmal
- kleine Schrift
- mehr als eine Grafik pro Folie
- zu viele Animationen
- unterschiedliche Folienstile im selben Vortrag

---

## Slide 1 - Titel und Vergleichsrahmen

### Folientitel

`MongoDB vs. PostgreSQL im Produktkatalog`

### Untertitel

`Modellierung, Evolution und Architektur-Trade-offs im selben Anwendungsszenario`

### Stichpunkte auf der Folie

- gleicher Produktkatalog
- gleiche UI
- gleicher API-Contract
- unterschiedliche Persistenzmodelle

### Beste Darstellung

Diese Folie sollte sehr ruhig sein.

Empfohlenes Layout:

- grosser Titel
- kleinere Unterzeile darunter
- darunter eine einzige horizontale Vergleichszeile mit 4 Begriffen

Beispiel:

```text
gleicher Produktkatalog | gleiche UI | gleicher API-Contract | andere Persistenzmodelle
```

Optional rechts klein:

- MongoDB-Icon oder gruenes Label
- PostgreSQL-Icon oder blaues Label

Ziel der Darstellung:

Die Folie soll nicht erklaeren, sondern den Rahmen sofort setzen.

---

## Slide 2 - Warum diese Domaene?

### Folientitel

`Warum ein kuratierter Produktkatalog?`

### Stichpunkte auf der Folie

- drei Produkttypen
- gemeinsame Basis plus typspezifische Attribute
- Kategorien, Varianten, Reviews als Teilaggregate
- alte und neue Datensaetze fuer Evolution
- gut fuer Update- und Analytics-Faelle

### Beste Darstellung

Am besten als kompakte Kartenansicht.

Empfohlenes Layout:

- drei kleine Karten nebeneinander: Laptop, T-Shirt, Buch
- unter den Karten eine kurze zweite Ebene mit den Querschnittsaspekten

Beispielstruktur:

```text
Laptop | T-Shirt | Buch

gemeinsame Basis
typspezifische Attribute
Teilaggregate
Schema-Evolution
```

Wichtig:

- nicht zu viele Beispieldetails auflisten
- nur die Domaenenmerkmale zeigen, die spaeter in der Demo wieder auftauchen

Ziel der Darstellung:

Das Publikum soll sehen, warum die Domaene klein, aber ergiebig ist.

---

## Slide 3 - Wie der Vergleich fair bleibt

### Folientitel

`Wie der Vergleich fair gehalten wird`

### Stichpunkte auf der Folie

- dieselbe React-UI
- dieselben Szenarien
- derselbe HTTP-Contract
- deterministische Seed-Daten
- gleiche fachliche Ausgabe

### Beste Darstellung

Hier ist ein einfaches Architekturdiagramm besser als viele Stichpunkte.

Empfohlenes Layout:

- oben Browser UI
- darunter ein Kasten: gleicher API-Contract
- darunter zwei Kaesten nebeneinander: MongoDB Backend und PostgreSQL Backend

Darunter klein als Stichwortzeile:

- gleiche Eingabe
- gleiche Ausgabe
- andere interne Modellierung

Wichtig:

- kein technisches Detaildiagramm mit Ports, Docker oder Containern
- nur die Fairnesslogik visualisieren

Ziel der Darstellung:

Das Publikum soll sofort verstehen, dass nicht zwei verschiedene Apps verglichen werden.

---

## Slide 4 - Gleiche Sicht, andere Storage Shape

### Folientitel

`Gleiches Produkt, andere interne Form`

### Stichpunkte auf der Folie

- gleiche fachliche Produktsicht
- MongoDB: eingebettetes Aggregat
- PostgreSQL: normalisierte Tabellen
- gleiche Ausgabe, andere innere Struktur

### Beste Darstellung

Diese Folie sollte klar als Gegenueberstellung gebaut sein.

Empfohlenes Layout:

- linke Spalte: MongoDB
- rechte Spalte: PostgreSQL
- oben ueber beiden Spalten ein kleines Label: `gleiches Produkt in der UI`

Inhalt links:

- ein vereinfachter Dokumentblock
- kleine Tags wie `categories`, `variants`, `reviews`

Inhalt rechts:

- mehrere verbundene kleine Tabellenkaesten
- `products`, `categories`, `variants`, `reviews`

Unten eine gemeinsame Schlusszeile:

```text
gleiche fachliche Antwort, andere strukturelle Logik
```

Ziel der Darstellung:

Nicht die Query zeigen, sondern die Form sichtbar machen.

---

## Slide 5 - Schema-Evolution und Aenderungskosten

### Folientitel

`Evolution und Aenderungskosten`

### Stichpunkte auf der Folie

- `regionalTaxCode` als spaeteres Feld
- MongoDB: alte und neue Dokumente parallel moeglich
- PostgreSQL: explizite und kontrollierte Anpassung
- Kategorie-Umbenennung als Gegenbeispiel

### Beste Darstellung

Diese Folie sollte aus zwei horizontalen Vergleichsreihen bestehen.

Empfohlenes Layout:

- oberer Block: Schema-Evolution
- unterer Block: Kategorie-Update

Im oberen Block:

- links MongoDB mit Alt- und Neu-Dokument nebeneinander
- rechts PostgreSQL mit zentraler Tabellensicht oder Update-Pfeil

Im unteren Block:

- links viele betroffene Produktdokumente
- rechts eine zentrale Kategorienzeile

Wichtig:

- nicht zu viele technische Begriffe auf die Folie schreiben
- die visuelle Richtung muss sofort lesbar sein: verteilt versus zentral

Ziel der Darstellung:

Die Folie soll zeigen, dass dieselbe Aenderung in beiden Modellen andere Kosten erzeugt.

---

## Slide 6 - Analytics und Verdichtung

### Folientitel

`Analytics und Verdichtung der Unterschiede`

### Stichpunkte auf der Folie

- beide Systeme beantworten dieselbe Frage
- MongoDB aggregiert ueber Dokumente
- PostgreSQL aggregiert ueber relationale Pfade
- Unterschied liegt im Modell, nicht nur in der Syntax

### Beste Darstellung

Hier eignet sich eine kleine Vergleichstabelle am besten.

Empfohlenes Layout:

| Aspekt | MongoDB | PostgreSQL |
| --- | --- | --- |
| Produkt lesen | nahe am Dokument | aus Relationen hydratisiert |
| Evolution | flexibel und schrittweise | explizit und kontrolliert |
| Update | breiter verteilt | zentral einfacher |
| Analytics | Dokumentaggregation | SQL ueber Relationen |

Wichtig:

- Tabelle sehr kurz halten
- pro Zelle nur 2 bis 4 Worte
- keine erklaerenden Nebensaetze in der Tabelle

Optional rechts unten klein:

- `avgPriceByType`
- `avgRatingByManufacturer`

Ziel der Darstellung:

Die Folie verdichtet den Vergleich, statt neue Informationen einzufuehren.

---

## Slide 7 - Grenzen der Demo

### Folientitel

`Was diese Demo bewusst nicht behauptet`

### Stichpunkte auf der Folie

- kein allgemeiner Performance-Beweis
- kein CAP-Nachweis
- keine Replica-Set- oder Failover-Demo
- keine Sharding-Aussage
- qualitative Architekturbeobachtung

### Beste Darstellung

Diese Folie sollte bewusst schlicht und fast streng wirken.

Empfohlenes Layout:

- links 4 kurze Negativpunkte
- rechts 1 positiver Einordnungssatz in einem hervorgehobenen Kasten

Beispiel rechts:

```text
Die Demo zeigt qualitative Modellierungsfolgen im selben Anwendungsszenario.
```

Wichtig:

- keine Rechtfertigungsfolie bauen
- lieber methodische Klarheit als defensive Formulierungen

Ziel der Darstellung:

Serioesitaet und methodische Ehrlichkeit.

---

## Slide 8 - Fazit

### Folientitel

`Keine Siegerdatenbank, sondern ein Problem-Fit`

### Stichpunkte auf der Folie

- MongoDB stark bei:
  - dokumentnahen Aggregaten
  - polymorpher Modellierung
  - schrittweiser Evolution
- PostgreSQL stark bei:
  - expliziter Struktur
  - zentralen Updates
  - kontrollierter relationaler Logik
- Datenbankwahl haengt vom Problem-Fit ab

### Beste Darstellung

Diese Folie sollte als symmetrische 2-Spalten-Folie gebaut werden.

Empfohlenes Layout:

- linke Spalte gruen: MongoDB stark bei
- rechte Spalte blau: PostgreSQL stark bei
- unten ueber beide Spalten eine gemeinsame Abschlusszeile

Beispiel fuer die Abschlusszeile:

```text
Keine Glaubensfrage, sondern eine Architekturentscheidung.
```

Wichtig:

- keine Uebertreibung
- kein Siegerdesign
- beide Seiten visuell gleich stark gewichten

Ziel der Darstellung:

Das Publikum soll mit einer differenzierten, sauberen Schlussbotschaft rausgehen.

---

## Empfohlene Darstellungsprinzipien fuer die gesamte Praesentation

### Typografie

- grosse, klare Titel
- Stichpunkte deutlich groesser als normaler Fliesstext
- keine langen Unterzeilen

### Farbe

- MongoDB immer gruen
- PostgreSQL immer blau
- neutrale Aussagen in dunklem Grau
- Warn- oder Grenzfolien eher in gedeckten Farben

### Visuals

- lieber einfache Diagramme als Screenshots voller Details
- lieber abstrahierte Storage-Shape-Grafiken als echte Datenbankdiagramme
- Tabellen nur dann, wenn sie wirklich verdichten

### Textmenge

- 3 bis 5 Stichpunkte pro Folie
- pro Stichpunkt nur 3 bis 8 Woerter
- ganze Argumente muendlich sagen, nicht auf die Folie schreiben

### Gesamtwirkung

Die Folien sollten nicht wie ein Skript aussehen, sondern wie eine visuelle Fuehrung durch einen klaren Vergleich.

Wenn eine Folie auch ohne deinen Sprechertext halbwegs verstaendlich bleibt, aber trotzdem noch Luft fuer muendliche Erklaerung laesst, ist sie gut gebaut.