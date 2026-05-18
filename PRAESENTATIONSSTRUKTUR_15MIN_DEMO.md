# Praesentationsstruktur fuer 15 Minuten

## Ziel dieser Struktur

Diese Struktur ist auf den aktuellen Stand des Demo-Projekts abgestimmt. Im Mittelpunkt steht jetzt eine gefuehrte Dual-Backend-Demo mit demselben Produktkatalog, derselben UI und demselben API-Contract fuer MongoDB und PostgreSQL.

Die Leitidee lautet:

> MongoDB und PostgreSQL werden am selben Produktkatalog mit derselben Anwendung gezeigt, damit sichtbar wird, wie sich Dokumentmodellierung und relationale Modellierung bei Lesezugriff, Schema-Evolution, zentralen Updates und Analytics unterscheiden.

Die Praesentation soll bewusst keine CAP-, Replica-Set- oder Benchmark-Beweisfuehrung liefern. Sie soll eine faire, klare und fachlich nachvollziehbare Architekturgeschichte erzaehlen.

---

## Gesamtaufbau

- Dauer: 15 Minuten
- Artefakt im Mittelpunkt: `mongodb_demo/`
- Stil: wenige Folien, klare Uebergaenge, eine gefuehrte Live-Demo
- Hauptziel: Modellierungs-Trade-offs an einem kleinen, kuratierten Produktkatalog erklaeren
- Nicht Ziel der Praesentation: quantitative Endgueltigkeit, CAP-Nachweis, Failover-Beweis oder Sharding-Demo

Empfohlene Verteilung:

1. Slide 1 bis 3: Problem, Domaene, Fairness des Vergleichs
2. Slide 4 bis 6: gefuehrte Live-Demo entlang der Story-Schritte
3. Slide 7 bis 8: Einordnung, Grenzen, Fazit

---

## Slide 1 - Titel und Leitfrage

### Ziel der Folie

Das Publikum soll sofort verstehen, dass es nicht um eine Siegerdatenbank geht, sondern um einen kontrollierten Architekturvergleich.

### Folientitel

`MongoDB vs. PostgreSQL im Produktkatalog: Modellierung, Evolution und Trade-offs`

### Inhalt auf der Folie

- gleicher Produktkatalog
- gleiche UI und gleicher API-Contract
- zwei unterschiedliche Persistenzmodelle
- Leitfrage: Welche Modellierungsfolgen werden im selben Anwendungsszenario sichtbar?

### Gesprochener Text

Ich vergleiche MongoDB und PostgreSQL hier nicht als allgemeine Siegerdatenbanken. Stattdessen zeige ich denselben Produktkatalog, dieselbe Anwendung und denselben API-Contract mit zwei unterschiedlichen Persistenzmodellen. Die Leitfrage ist also nicht, welche Datenbank pauschal besser ist, sondern welche Modellierungsfolgen in genau diesem Szenario sichtbar werden.

### Kernaussage

Der Vortrag ist ein fairer Architekturvergleich und kein Werbevortrag fuer eine Datenbank.

### Zeitbudget

1 Minute

---

## Slide 2 - Warum diese Domaene?

### Ziel der Folie

Begruenden, warum der aktuelle kleine Produktkatalog ein gutes Vergleichsbeispiel ist.

### Folientitel

`Warum ein kuratierter Produktkatalog?`

### Inhalt auf der Folie

- drei Produkttypen: Laptop, T-Shirt, Buch
- gemeinsame Felder plus typspezifische Attribute
- eingebettete Teilaggregate wie Kategorien, Varianten und Reviews
- alte und neue Datensaetze fuer Schema-Evolution
- gut erklaerbare Update- und Analytics-Faelle

### Gesprochener Text

Die Domaene ist absichtlich klein, aber fachlich ergiebig. Mit Laptops, T-Shirts und Buechern habe ich unterschiedliche Produkttypen in einem gemeinsamen Modell. Gleichzeitig enthaelt jedes Produkt Teilaggregate wie Kategorien, Varianten und Reviews. Dazu kommen alte und neue Datensaetze, damit Schema-Evolution sichtbar wird. So kann ich Modellierungsunterschiede zeigen, ohne mich in zu vielen Nebenthemen zu verlieren.

### Kernaussage

Die Domaene ist klein genug fuer 15 Minuten, aber reich genug fuer einen fairen Modellvergleich.

### Zeitbudget

1 Minute

---

## Slide 3 - Wie der Vergleich fair bleibt

### Ziel der Folie

Klar machen, dass nicht zwei verschiedene Apps, sondern zwei Datenmodellierungsansaetze verglichen werden.

### Folientitel

`Wie der Vergleich fair gehalten wird`

### Inhalt auf der Folie

- dieselbe React-UI
- dieselben Produktansichten und Szenarien
- derselbe HTTP-Contract
- deterministische Seed-Daten
- unterschiedliche interne Speicherung, gleiche fachliche Ausgabe

### Zusatzgrafik auf der Folie

```text
Browser UI -> gleicher API-Contract -> MongoDB Backend / PostgreSQL Backend
```

### Gesprochener Text

Der Vergleich ist nur sinnvoll, wenn nicht zwei verschiedene Anwendungen gegeneinander antreten. Deshalb laufen beide Backends hinter derselben UI und demselben API-Contract. Beide liefern also dieselbe fachliche Produktsicht. Der Unterschied liegt nicht in der Oberflaeche, sondern in der internen Modellierung und in den daraus entstehenden Konsequenzen.

### Kernaussage

Verglichen werden Modellierungsansaetze hinter demselben fachlichen Vertrag.

### Zeitbudget

1.5 Minuten

---

## Slide 4 - Live-Demo Teil 1: Gleiches Ergebnis, andere Storage Shape

### Ziel der Folie

Die Demo mit einem klaren Symmetriepunkt starten: gleiche sichtbare Anwendung, aber andere interne Form.

### Folientitel

`Live-Demo Teil 1: Gleiches Produkt, andere interne Form`

### Was auf der Folie stehen soll

- zuerst gleiche fachliche Produktsicht zeigen
- danach `Storage Shape` vergleichen
- MongoDB: eingebettetes Aggregat
- PostgreSQL: normalisierte Tabellen und Hydration

### Live-Demo-Aktion

1. Anwendung offen haben.
2. MongoDB auswaehlen.
3. Ein Produkt oeffnen, idealerweise einen Laptop.
4. Zwischen `document`, `query` und `code` wechseln.
5. Auf PostgreSQL umschalten.
6. Dasselbe Produkt erneut betrachten und `Storage Shape` zeigen.

### Gesprochener Text

Ich starte bewusst mit einem symmetrischen Blick: Die sichtbare Anwendung bleibt gleich, aber intern aendert sich die Form des Produkts. In MongoDB liegt das Produkt als eingebettetes Dokument sehr nah an der API-Antwort. In PostgreSQL wird dieselbe fachliche Sicht aus mehreren Tabellen zusammengesetzt. Genau an diesem Punkt sieht man bereits den Kern des Vergleichs: gleiche fachliche Wirkung, andere strukturelle Kosten und Vorteile.

### Kernaussage

MongoDB und PostgreSQL koennen dasselbe Produkt liefern, aber nicht ueber dieselbe innere Modelllogik.

### Zeitbudget

3 Minuten

---

## Slide 5 - Live-Demo Teil 2: Schema-Evolution und zentrale Updates

### Ziel der Folie

Die zwei wichtigsten aktiven Demo-Szenarien zeigen: `lazy migration` und `category rename`.

### Folientitel

`Live-Demo Teil 2: Evolution und Aenderungskosten`

### Was auf der Folie stehen soll

- `regionalTaxCode` als spaeter eingefuehrtes Feld
- MongoDB: alte und neue Dokumente koennen parallel existieren
- PostgreSQL: explizite, kontrollierte Aenderung in Tabellenstruktur und Zeilen
- Kategorie-Umbenennung als Kontrast zwischen Denormalisierung und zentraler Pflege

### Live-Demo-Aktion

1. Im Story-Schritt `Schema` bleiben.
2. Ein Produkt mit alter Struktur zeigen oder nach `withoutTaxCode` filtern.
3. `lazy migration` auf MongoDB ausfuehren.
4. Auf PostgreSQL wechseln und dasselbe Szenario wiederholen.
5. Danach `category rename` fuer beide Backends ausfuehren.

### Gesprochener Text

Hier sieht man die Unterschiede nicht nur im Lesen, sondern im Veraendern des Modells. Beim Feld `regionalTaxCode` kann MongoDB alte und neue Dokumente vergleichsweise natuerlich nebeneinander tolerieren und nur die betroffenen Dokumente spaeter migrieren. PostgreSQL macht dieselbe Aenderung expliziter und kontrollierter. Beim Umbenennen einer Kategorie zeigt sich dann die Gegenrichtung: In MongoDB koennen eingebettete Kategorieschnappschuesse in vielen Produktdokumenten angepasst werden muessen, waehrend PostgreSQL eine zentrale Kategorienzeile aktualisiert.

### Kernaussage

Flexibilitaet und zentrale Pflege sind gegenlaeufige Staerken, keine allgemeine Siegerlogik.

### Zeitbudget

3 Minuten

---

## Slide 6 - Live-Demo Teil 3: Analytics und direkte Einordnung

### Ziel der Folie

Die Demo mit einem kleinen Analytics-Beispiel abrunden und die Trade-offs verdichten.

### Folientitel

`Live-Demo Teil 3: Analytics und Verdichtung der Unterschiede`

### Inhalt auf der Folie

| Aspekt | MongoDB | PostgreSQL |
| --- | --- | --- |
| Produkt lesen | nahe am Dokument | aus Relationen hydratisiert |
| Schema-Evolution | flexibel und schrittweise | explizit und kontrolliert |
| Kategorie-Update | bei Einbettung breiter verteilt | zentral oft einfacher |
| Analytics | Aggregation ueber Dokumente | Aggregation ueber SQL-Joins |

### Live-Demo-Aktion

1. `Analytics` oeffnen.
2. `avgPriceByType` oder `avgRatingByManufacturer` fuer MongoDB zeigen.
3. Direkt auf PostgreSQL umschalten und denselben Fall zeigen.
4. Query- und Code-Ansicht kurz einblenden.

### Gesprochener Text

Das Analytics-Beispiel rundet die Demo ab, weil es zeigt, dass beide Systeme dieselbe Frage beantworten koennen, aber mit anderer innerer Logik. MongoDB aggregiert ueber Dokumente und eingebettete Strukturen, PostgreSQL ueber explizite relationale Pfade. Spaetestens hier laesst sich die gesamte Demo verdichten: Die Unterschiede liegen nicht nur in Syntax, sondern im Modellierungsparadigma.

### Kernaussage

Die spannendste Differenz liegt in der inneren Modelllogik, nicht nur in der Abfragesprache.

### Zeitbudget

2 Minuten

---

## Slide 7 - Grenzen der Demo

### Ziel der Folie

Methodische Ehrlichkeit zeigen und bewusst benennen, was diese Live-Demo nicht leisten soll.

### Folientitel

`Was diese Demo bewusst nicht behauptet`

### Inhalt auf der Folie

- kein allgemeiner Performance-Beweis
- kein CAP-Nachweis
- keine Replica-Set- oder Failover-Demonstration
- keine Sharding-Aussage
- nur qualitative Architekturbeobachtung im selben Anwendungsszenario

### Gesprochener Text

Wichtig ist, was ich hier nicht behaupte. Diese Demo beweist keine allgemeine Ueberlegenheit, keine globale Performance-Aussage und auch kein CAP- oder Ausfallverhalten. Sie zeigt qualitativ, wie sich zwei unterschiedliche Persistenzmodelle im selben Anwendungsszenario anfuehlen und welche Architekturfolgen sichtbar werden.

### Kernaussage

Die Live-Demo ist ein qualitativer Architekturvergleich, keine vollstaendige wissenschaftliche Endvalidierung.

### Zeitbudget

1 Minute

---

## Slide 8 - Kritisches Fazit

### Ziel der Folie

Den Vortrag sauber abschliessen, ohne zu uebertreiben, und den Problem-Fit betonen.

### Folientitel

`Fazit: Keine Siegerdatenbank, sondern ein Problem-Fit`

### Inhalt auf der Folie

- MongoDB ist stark bei:
  - dokumentnahen Aggregaten
  - polymorpher Modellierung
  - schrittweiser Evolution
- PostgreSQL ist stark bei:
  - expliziter Struktur
  - zentralen Updates
  - kontrollierter relationaler Logik
- Schlussgedanke: Die Wahl haengt von Workload, Aenderungsmustern und Kontrollbedarf ab.

### Gesprochener Text

Mein Fazit ist bewusst kein Siegerfazit. MongoDB wirkt in diesem Produktkatalog stark, wenn fachliche Aggregate, Polymorphie und schrittweise Evolution wichtig sind. PostgreSQL wirkt stark, wenn Strukturkontrolle, zentrale Pflege und explizite relationale Logik im Vordergrund stehen. Die Datenbankwahl ist deshalb keine Glaubensfrage, sondern eine Architekturentscheidung in Abhaengigkeit vom Problem-Fit.

### Kernaussage

Die Datenbankwahl ist kontextabhaengig und sollte aus der Domaene und den Aenderungsmustern abgeleitet werden.

### Zeitbudget

1.5 Minuten

---

## Empfohlene Live-Demo-Reihenfolge in Kurzform

1. MongoDB auswaehlen.
2. Produktdetail und Storage Shape zeigen.
3. Auf PostgreSQL wechseln und dieselbe fachliche Sicht zeigen.
4. Schema-Evolution mit `regionalTaxCode` erklaeren.
5. `lazy migration` auf beiden Backends zeigen.
6. `category rename` auf beiden Backends zeigen.
7. Eine Aggregation fuer beide Backends zeigen.
8. Mit dem Problem-Fit-Fazit schliessen.

Diese Reihenfolge entspricht dem aktuellen Aufbau der Demo-App und vermeidet unnoetiges Herumklicken.

---

## CLI-Backup fuer die Praesentation

Falls das Frontend im Praesentationsmoment nicht stabil verfuegbar ist, kann dieselbe Story ueber die CLI abgesichert werden:

```powershell
npm run demo:health:mongo
npm run demo:health:postgres
npm run demo:read:mongo
npm run demo:read:postgres
npm run demo:rename:mongo
npm run demo:rename:postgres
npm run demo:migrate:mongo
npm run demo:migrate:postgres
```

Damit bleibt die Demo auch ohne Browser inhaltlich vorfuehrbar.

---

## Was du bewusst nicht sagen solltest

- Nicht sagen: MongoDB ist generell performanter.
- Nicht sagen: PostgreSQL ist fuer moderne Anwendungen schlechter geeignet.
- Nicht sagen: Diese Demo beweist CAP oder Ausfalltoleranz.
- Nicht sagen: Flexibilitaet ist automatisch besser als Explizitheit.

Stattdessen besser:

- In diesem Produktkatalog wirkt MongoDB bei dokumentnahen Aggregaten sehr natuerlich.
- In diesem Produktkatalog wirkt PostgreSQL bei zentraler Strukturkontrolle sehr stark.
- Die Demo zeigt qualitative Modellierungsfolgen im selben Anwendungsszenario.

---

## Letzte Praesentationstipps

1. Starte mit der Leitfrage, nicht mit der UI.
2. Zeige immer zuerst die gleiche fachliche Sicht und dann die interne Differenz.
3. Halte MongoDB und PostgreSQL im Vortrag symmetrisch.
4. Nutze die Szenarien `lazy migration`, `category rename` und `analytics` als rote Fadenpunkte.
5. Verbringe mehr Zeit mit Interpretation als mit Navigation.