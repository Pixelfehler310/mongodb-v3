# Praesentationsstruktur fuer 15 Minuten

## Ziel dieser Struktur

Diese Struktur ist fuer eine kurze Seminarpraesentation gedacht, in der nur das Demo-Projekt im Mittelpunkt steht. Die Praesentation soll fair bleiben, beide Systeme kritisch betrachten und keine kuenstliche Siegergeschichte bauen.

Die Leitidee lautet:

> MongoDB und PostgreSQL werden am selben Produktkatalog mit demselben Frontend-Contract gezeigt, damit sichtbar wird, wann Dokumentmodellierung staerker wirkt und wann das relationale Modell Vorteile hat.

Die Praesentation soll nicht versuchen, in 15 Minuten alle wissenschaftlichen Beweise zu liefern. Sie soll eine klare, faire und methodisch saubere Architekturgeschichte erzaehlen.

---

## Gesamtaufbau

- Dauer: 15 Minuten
- Artefakt im Mittelpunkt: `mongodb_demo/`
- Stil: kurze Folien, klare Uebergaenge, 1 kontrollierte Live-Demo
- Hauptziel: Unterschiede in Modellierung, Dokumentstruktur, Schema-Evolution und Trade-offs erklaeren
- Nicht Ziel der Praesentation: vollstaendige Benchmark-Beweisfuehrung

Empfohlene Verteilung:

1. Slide 1 bis 3: Problem, Ziel, Fairness des Vergleichs
2. Slide 4 bis 6: Live-Demo und direkte Auswertung
3. Slide 7 bis 8: kritische Einordnung und Fazit

---

## Slide 1 - Titel und Forschungsfrage

### Ziel der Folie

Das Publikum soll in den ersten 30 bis 60 Sekunden verstehen, worum es fachlich geht und dass der Vortrag kein Werbevortrag fuer MongoDB ist.

### Folientitel

`MongoDB vs. PostgreSQL im Produktkatalog: Dokumentmodell, relationale Struktur und praktische Trade-offs`

### Inhalt auf der Folie

- Vergleich eines dokumentenorientierten und eines relationalen Modells
- Gleiche Domaene: polymorpher Produktkatalog
- Gleiche Anwendung, gleicher Frontend-Contract
- Leitfrage: Wann ist welches Modell fuer diese Domaene staerker?

### Gesprochener Text

In diesem Vortrag vergleiche ich MongoDB und PostgreSQL nicht als allgemeine Siegerdatenbanken, sondern anhand eines konkreten fachlichen Beispiels: eines polymorphen Produktkatalogs. Beide Systeme bedienen dieselbe Anwendung und denselben Frontend-Contract. Die eigentliche Frage ist deshalb nicht, welche Datenbank pauschal besser ist, sondern wann ein Dokumentmodell Vorteile bietet und wann ein relationales Modell staerker wirkt.

### Kernaussage

Der Vortrag untersucht einen fairen, fachlich motivierten Architekturvergleich statt einer pauschalen Technologiebehauptung.

### Zeitbudget

1 Minute

---

## Slide 2 - Warum gerade diese Domaene?

### Ziel der Folie

Begruenden, warum der Produktkatalog ein besseres Vergleichsbeispiel ist als eine rein technische Lastsimulation.

### Folientitel

`Warum ein polymorpher Produktkatalog?`

### Inhalt auf der Folie

- mehrere Produkttypen in einem gemeinsamen fachlichen Modell
- gemeinsame Felder plus typspezifische Attribute
- eingebettete Listen und Teilaggregate
- reale Schema-Evolution
- gute Sichtbarkeit von Dokumentlokalitaet und Hydration

### Gesprochener Text

Ich habe bewusst keine rein technische Event-Domaene gewaehlt, sondern einen Produktkatalog. Der Grund ist, dass hier die Unterschiede schon im Datenmodell selbst sichtbar werden. Wir haben gemeinsame Felder, typspezifische Attribute, eingebettete Bereiche wie Varianten oder Reviews und ausserdem echte Schema-Evolution. Genau dadurch werden die typischen Spannungen zwischen Dokumentmodell und relationalem Modell sichtbar, ohne dass ich sofort mit Cluster- oder Infrastrukturthemen argumentieren muss.

### Kernaussage

Die Domaene ist so gewaehlt, dass die Modellierungsunterschiede fachlich natuerlich sichtbar werden.

### Zeitbudget

1 Minute

---

## Slide 3 - Fairness des Vergleichs

### Ziel der Folie

Dem Publikum frueh zeigen, dass die beiden Systeme nicht ueber unterschiedliche Anwendungen verglichen werden.

### Folientitel

`Wie der Vergleich fair gehalten wird`

### Inhalt auf der Folie

- dieselbe UI
- derselbe API-Contract
- dieselbe Produktkatalog-Domaene
- deterministische Seed-Daten
- unterschiedliche interne Modellierung, aber gleiche fachliche Ausgabe

### Zusatzgrafik auf der Folie

```text
Browser UI -> gleicher Frontend-Contract -> MongoDB Backend / PostgreSQL Backend
```

### Gesprochener Text

Der Vergleich ist nur dann sinnvoll, wenn nicht zwei verschiedene Anwendungen gegeneinander antreten. Deshalb verwende ich dieselbe UI und denselben API-Contract fuer beide Backends. Beide Systeme liefern also dieselbe fachliche Sicht auf einen Produktkatalog. Der Unterschied liegt nicht in der Oberflaeche, sondern in der internen Speicherung und Rekonstruktion der Daten.

### Kernaussage

Verglichen werden nicht zwei Apps, sondern zwei Datenmodellierungsansaetze hinter demselben fachlichen Vertrag.

### Zeitbudget

1.5 Minuten

---

## Slide 4 - Live-Demo: MongoDB zeigt seine Staerken

### Ziel der Folie

Die Live-Demo nicht als Herumklicken, sondern als gezielte Illustration von drei MongoDB-Staerken fuehren.

### Folientitel

`Live-Demo Teil 1: Warum das MongoDB-Modell hier natuerlich wirkt`

### Was auf der Folie stehen soll

- ein Produkt ist als Dokument direkt lesbar
- eingebettete Daten liegen schon zusammen vor
- polymorphe Felder passen natuerlich in ein gemeinsames Modell
- Filter werden sichtbar zu Query und PyMongo-Code

### Live-Demo-Aktion

1. Anwendung starten oder offen haben.
2. MongoDB als Backend auswaehlen.
3. Einen Laptop auswaehlen.
4. Dokumentansicht zeigen.
5. Danach Query-Tab und Code-Tab oeffnen.
6. Einen oder zwei Filter setzen, zum Beispiel `productType = laptop` und `schemaEvolution = withTaxCode`.

### Gesprochener Text

Hier sieht man die eigentliche Staerke des Dokumentmodells. Das Produkt liegt als fachlich lesbares Dokument vor. Gemeinsame Felder, typspezifische Attribute, Varianten, Reviews und weitere verschachtelte Bereiche koennen in einer Form gespeichert werden, die der spaeteren API-Antwort schon sehr nahe kommt. Wenn ich Filter setze, kann ich direkt zeigen, wie sich dieselbe UI-Aktion in eine MongoDB-Query und in passenden PyMongo-Code uebersetzt. Fuer ein Publikum ist das sehr anschaulich, weil das Datenmodell und der Zugriffspfad fast dieselbe Form haben.

### Kernaussage

MongoDB wirkt in diesem Szenario stark, wenn ein fachliches Aggregat als zusammenhaengendes Dokument gelesen und erklaert werden soll.

### Zeitbudget

3 Minuten

---

## Slide 5 - Live-Demo: PostgreSQL zeigt seine Staerken

### Ziel der Folie

Direkt danach zeigen, dass PostgreSQL nicht die schlechtere Variante ist, sondern andere Staerken besitzt.

### Folientitel

`Live-Demo Teil 2: Warum das relationale Modell hier ebenfalls stark ist`

### Was auf der Folie stehen soll

- gleiche fachliche Ausgabe trotz anderer interner Struktur
- explizite Tabellenstruktur und klare Trennung von Verantwortlichkeiten
- Kontrolle durch Normalisierung
- SQL und psycopg bleiben fuer strukturierte Abfragen sehr klar

### Live-Demo-Aktion

1. Auf PostgreSQL umschalten.
2. Dasselbe oder ein vergleichbares Produkt oeffnen.
3. `Storage Shape` zeigen.
4. Query-Tab und Code-Tab zeigen.
5. Kurz die gleiche Filterkombination wiederholen.

### Gesprochener Text

Beim Wechsel auf PostgreSQL bleibt die fachliche Ausgabe fuer die Anwendung stabil, aber intern passiert etwas anderes. Das Produkt wird nicht als einzelnes Dokument gelesen, sondern aus mehreren relationalen Teilen zusammengesetzt. Genau darin liegt aber auch eine Staerke: Die Struktur ist explizit, die Beziehungen sind kontrolliert und die Daten sind klar getrennt. Das ist oft weniger bequem fuer ein aggregiertes API-Objekt, kann aber bei Datenkontrolle, zentralen Updates und klarer Struktur sehr vorteilhaft sein.

### Kernaussage

PostgreSQL ist hier nicht schwach, sondern staerker in expliziter Struktur, Kontrolle und zentraler Datenhaltung.

### Zeitbudget

2.5 Minuten

---

## Slide 6 - Direkter Vergleich der wichtigsten Trade-offs

### Ziel der Folie

Das Publikum soll die Unterschiede nach der Live-Demo strukturiert einordnen koennen.

### Folientitel

`Was man nach der Demo direkt vergleichen kann`

### Inhalt auf der Folie

| Aspekt                        | MongoDB                      | PostgreSQL                              |
| ----------------------------- | ---------------------------- | --------------------------------------- |
| Produktdetail lesen           | sehr natuerlich als Dokument | muss aus Relationen hydratisiert werden |
| Polymorphe Produkttypen       | flexibel in einer Collection | expliziter modelliert                   |
| Strukturkontrolle             | flexibler                    | strenger und expliziter                 |
| Globale Datenaenderungen      | bei Denormalisierung teurer  | zentral oft einfacher                   |
| Erklaerbarkeit fuer Aggregate | sehr anschaulich             | technisch praezise, aber indirekter     |

### Gesprochener Text

Nach der Demo lassen sich die Unterschiede relativ klar verdichten. MongoDB wirkt stark, wenn ein Produkt als zusammenhaengendes fachliches Aggregat gedacht wird. PostgreSQL wirkt stark, wenn Struktur, zentrale Pflege und explizite Beziehungen im Vordergrund stehen. Entscheidend ist, dass sich die Systeme hier nicht nur in Syntax unterscheiden, sondern in der Art, wie sie die gleiche fachliche Welt modellieren.

### Kernaussage

Die Unterschiede liegen im Modellierungsparadigma und nicht nur in der Abfragesprache.

### Zeitbudget

2 Minuten

---

## Slide 7 - Schema-Evolution und Developer Experience

### Ziel der Folie

Den fuer MongoDB oft zentralen Punkt der Flexibilitaet zeigen, ohne daraus eine unkritische Werbebotschaft zu machen.

### Folientitel

`Schema-Evolution: Flexibilitaet gegen Explizitheit`

### Inhalt auf der Folie

- Beispiel: `regionalTaxCode` als spaeter eingefuehrtes Feld
- MongoDB: alte und neue Dokumente koennen nebeneinander existieren
- PostgreSQL: neue Struktur ist explizit und kontrolliert
- Interpretationspunkt: Flexibilitaet ist ein Vorteil, aber auch ein Steuerungsproblem

### Optionaler Unterpunkt auf der Folie

- MongoDB ermoeglicht Lazy Migration
- PostgreSQL erzwingt haeufig frueher explizite Anpassungen

### Gesprochener Text

Ein besonders wichtiger Unterschied ist die Schema-Evolution. Im Demo ist das am Feld `regionalTaxCode` sichtbar. In MongoDB koennen alte und neue Dokumentversionen vergleichsweise natuerlich nebeneinander existieren. Das ist praktisch, wenn sich Anforderungen schrittweise entwickeln. PostgreSQL ist hier meist expliziter: Aenderungen muessen klarer eingezogen und kontrolliert werden. Das ist weniger flexibel, aber dafuer oft besser steuerbar. Genau deshalb sollte man Flexibilitaet nicht automatisch mit Ueberlegenheit verwechseln.

### Kernaussage

MongoDB erleichtert evolutionaere Aenderungen, PostgreSQL bietet dafuer haeufig staerkere strukturelle Kontrolle.

### Zeitbudget

1.5 Minuten

---

## Slide 8 - Kritisches Fazit

### Ziel der Folie

Die Praesentation sauber abschliessen, ohne zu uebertreiben, und Raum fuer die spaetere Seminararbeit offenlassen.

### Folientitel

`Fazit: Keine Siegerdatenbank, sondern ein Problem-Fit`

### Inhalt auf der Folie

- MongoDB ist stark bei:
  - dokumentnahen Aggregaten
  - Polymorphie
  - anschaulicher Dokumentstruktur
  - flexibler Schema-Evolution
- PostgreSQL ist stark bei:
  - expliziter Struktur
  - zentralen Updates
  - kontrollierter Datenhaltung
  - klaren relationalen Zugriffspfaden
- Ausblick: Die quantitative Validierung folgt im schriftlichen Teil

### Gesprochener Text

Mein Fazit ist deshalb bewusst nicht, dass eines der beiden Systeme generell besser ist. MongoDB wirkt in diesem Produktkatalog stark, wenn fachliche Aggregate, Dokumentnaehe und flexible Evolution wichtig sind. PostgreSQL wirkt stark, wenn Strukturkontrolle, zentrale Pflege und explizite Relationen im Vordergrund stehen. Fuer die Praesentation reicht diese qualitative Gegenueberstellung. Die quantitativ belastbare Validierung von Performance- oder Ausfallhypothesen gehoert anschliessend in das wissenschaftliche Testprojekt und in die schriftliche Seminararbeit.

### Kernaussage

Die Datenbankwahl ist eine Architekturentscheidung in Abhaengigkeit von Domaene und Zielbild, nicht eine pauschale Glaubensfrage.

### Zeitbudget

1.5 Minuten

---

## Optionales Backup-Slide - Wenn noch Zeit oder Fragen kommen

### Folientitel

`Was in der schriftlichen Arbeit noch vertieft wird`

### Inhalt auf der Folie

- quantitative Workloads und Messungen
- Denormalized Update Cost
- Join-/Lookup-Spannung bei nicht lokalem Datenzugriff
- spaeter eventuell Topologie- und Failover-Aspekte

### Gesprochener Text

Wenn ich diesen Vergleich spaeter in der Seminararbeit weiter ausbaue, dann wuerde ich genau die Punkte vertiefen, die in 15 Minuten nicht serioes live gezeigt werden koennen: reproduzierbare quantitative Messungen, die Kosten denormalisierter Updates, die Unterschiede zwischen Dokumentlokalitaet und relationaler Rekonstruktion sowie gegebenenfalls auch Topologie- und Ausfallverhalten.

### Kernaussage

Die Praesentation ist der qualitative Architekturteil, die Seminararbeit liefert spaeter die tieferen Mess- und Methodenebenen.

---

## Empfohlene Live-Demo-Reihenfolge in Kurzform

1. MongoDB auswaehlen.
2. Produktdetail zeigen.
3. Query und Code zeigen.
4. Zwei Filter setzen.
5. PostgreSQL auswaehlen.
6. Gleiches fachliches Ergebnis, aber andere Storage Shape zeigen.
7. Vergleich verbal verdichten.

Diese Reihenfolge ist robust, weil sie wenige Klicks benoetigt und fachlich klar bleibt.

---

## Was du bewusst nicht behaupten solltest

- Nicht sagen: MongoDB ist generell performanter.
- Nicht sagen: PostgreSQL ist fuer moderne Anwendungen schlechter geeignet.
- Nicht sagen: Das Demo beweist bereits alle wissenschaftlichen Aussagen.
- Nicht sagen: Schema-Flexibilitaet ist automatisch ein Vorteil ohne Kosten.

Stattdessen besser:

- In diesem Produktkatalog wirkt MongoDB bei Dokumentnaehe sehr natuerlich.
- In diesem Produktkatalog wirkt PostgreSQL bei zentraler Strukturkontrolle sehr stark.
- Die Praesentation zeigt die Architekturunterschiede qualitativ und fair.

---

## Letzte Praesentationstipps

1. Starte nicht mit der Anwendung, sondern mit der Leitfrage.
2. Nutze die Live-Demo nur fuer klar vorbereitete Klickpfade.
3. Wechsle nach MongoDB relativ schnell zu PostgreSQL, damit der Vergleich sichtbar fair bleibt.
4. Verbringe mehr Zeit mit Interpretation als mit Navigation in der UI.
5. Schliesse mit einem kritischen Problem-Fit-Fazit statt mit einer Siegerfolie.
