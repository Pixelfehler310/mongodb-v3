# Analyse: Neues Konzept vs. aktuelles Konzept, Testfaelle und Demo-Projekt

## Ziel dieser Analyse

Dieses Dokument bewertet vier Dinge getrennt und im Zusammenhang:

1. das neue Konzept aus dem aktuellen Anforderungsdokument,
2. das aktuelle Konzept in `mongodb-v2`,
3. die aktuell implementierten Benchmark-Testfaelle in `mongodb-v2`,
4. das Demo-Projekt in `mongodb_demo`.

Bewertet werden jeweils:

- fachliche Passung zur eigentlichen Seminarfrage,
- wissenschaftliche Aussagekraft,
- Fairness des Vergleichs,
- Demonstrationswert in der Praesentation,
- Eignung als Grundlage fuer das bestmoegliche Gesamtergebnis.

Die Bewertung folgt bewusst nicht dem Aufwand. Massgeblich ist allein, welches Design die staerkste, sauberste und am besten verteidigbare Aussage ermoeglicht.

---

## Executive Summary

Das neue Konzept ist dem aktuellen Konzept klar ueberlegen, weil es die eigentliche fachliche Kernfrage direkt adressiert: Wie unterscheiden sich relationale und dokumentenorientierte Systeme bei polymorphen Daten, komplexen Aggregaten, Schema-Evolution und gezielten Performance-Trade-offs?

Das aktuelle Konzept in `mongodb-v2` beantwortet dagegen primaer eine andere Frage: Wie verhaelt sich ein lokal aufgebauter MongoDB-Cluster gegenueber einem PostgreSQL-Single-Node unter einem stark auf Sensor-Events und Regions-Sharding zugeschnittenen Lastmodell? Das ist nicht wertlos, aber es ist enger, technisch voreingenommen und nur begrenzt als allgemeiner Architekturvergleich belastbar.

Noch kritischer: Die aktuellen Testfaelle in `mongodb-v2` haben methodische Probleme, die ihre wissenschaftliche Aussagekraft deutlich schwaechen. Insbesondere wird PostgreSQL bei Paralleltests durch die Adapter-Implementierung kuenstlich serialisiert, waehrend MongoDB mit einem thread-sicheren Client und Connection Pool arbeitet. Dadurch messen T2 bis T4 nicht nur Datenbankverhalten, sondern auch einen asymmetrischen Client-Layer.

Das Demo-Projekt in `mongodb_demo` ist als Lehr- und Praesentationsartefakt gut. Es erklaert MongoDB klar, anschaulich und verlaesslich. Als wissenschaftliche Evidenz fuer die Forschungsfrage ist es aber schwach, weil es weder einen kontrollierten Vergleich noch eine belastbare empirische Methodik enthaelt.

Kurzurteil:

| Gegenstand                          | Gesamturteil                                                | Rolle im Endergebnis                                           |
| ----------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| Neues Konzept                       | Stark, mit wenigen methodischen Nachschaerfungen sehr stark | Sollte zum Hauptkonzept werden                                 |
| Aktuelles Konzept in `mongodb-v2`   | Nur eingeschraenkt tragfaehig                               | Hoechstens als Teilaspekt oder Vorstufe behalten               |
| Aktuelle Testfaelle in `mongodb-v2` | In aktueller Form nicht als Kernbeleg geeignet              | Fuer wissenschaftliche Nutzung neu aufsetzen                   |
| Demo-Projekt `mongodb_demo`         | Stark als Demo, schwach als Evidenz                         | Als Praesentations-Showcase behalten, nicht als Beweisfuehrung |

---

## Bewertungsrahmen

Ein Vergleich zwischen PostgreSQL und MongoDB ist nur dann wissenschaftlich belastbar, wenn mindestens die folgenden Fragen sauber beantwortet sind:

1. Wird wirklich dasselbe fachliche Problem verglichen, oder nur zwei unterschiedlich guenstige Modellierungen?
2. Wird Datenbankverhalten gemessen, oder in Wahrheit Treiber-, Pooling-, Locking- oder Infrastrukturverhalten?
3. Sind die Hypothesen direkt aus dem Datenmodell und den Workloads ableitbar?
4. Sind die Resultate verallgemeinerbar, oder nur fuer eine sehr speziell konstruierte Demo-Welt gueltig?
5. Kann man die Resultate in der Praesentation klar, knapp und ohne methodische Bauchschmerzen verteidigen?

An genau diesen Punkten ist das neue Konzept stark und das aktuelle Benchmark-Konzept nur teilweise stark.

---

## 1. Bewertung des neuen Konzepts

## 1.1 Was das neue Konzept besser macht

Das neue Konzept verbessert den Scope an den entscheidenden Stellen.

### A. Es trifft die eigentliche Architekturfrage deutlich genauer

Der Fokus liegt auf:

- Object-Relational Impedance Mismatch,
- Datenlokalitaet,
- Schema-on-Read vs. Schema-on-Write,
- polymorphen Daten,
- kontrollierten Trade-offs zwischen Einbettung, Referenzen, Joins und Denormalisierung.

Das ist wesentlich naeher an der eigentlichen Frage "Wann ist ein dokumentenorientiertes Modell fachlich und technisch sinnvoller als ein relationales Modell?" als das aktuelle Sensor-/Cluster-Konzept.

### B. Es trennt qualitative und quantitative Aussage sauberer

Projekt 1 ist ein qualitativer Architektur-Showcase. Projekt 2 ist eine quantitative Metrifizierung. Diese Trennung ist wissenschaftlich sinnvoll, weil sie zwei verschiedene Arten von Aussagen nicht vermischt:

- Architekturelle Erklaerkraft und Developer Experience,
- empirische Performance-Aussagen.

Das aktuelle Konzept in `mongodb-v2` versucht beides teilweise zu vermengen, obwohl es faktisch fast nur quantitative Infrastrukturtests enthaelt.

### C. Es nutzt einen deutlich geeigneteren Domain-Fit

Ein polymorpher Produktkatalog ist fuer den SQL-vs.-Dokument-Vergleich besser geeignet als Sensor-Events, weil die Unterschiede nicht nur bei Skalierung oder Sharding sichtbar werden, sondern bereits im Datenmodell selbst:

- unterschiedliche Produkttypen mit stark variierenden Attributen,
- komplexe Aggregate aus Produkt, Varianten, Kategorien und Bewertungen,
- reale Schema-Evolution.

Das erlaubt eine viel direktere Demonstration von Modellierungs- und Wartungsfolgen.

### D. Es formuliert aussagekraeftigere Hypothesen

Die drei geplanten Lastszenarien sind inhaltlich staerker als die aktuellen Tests, weil sie bekannte Architekturspannungen direkt ansprechen:

- Lesevorteil durch Datenlokalitaet,
- Update-Kosten durch Denormalisierung,
- Join-/Lookup-Kosten bei vernetzten Daten.

Diese Hypothesen sind fuer ein wissenschaftliches Publikum leichter nachvollziehbar als "MongoDB-Cluster skaliert horizontal besser als PostgreSQL-Single-Node", weil sie an fachlich klaren Modellierungsentscheidungen haengen.

### E. Es macht Schema-Evolution zu einem echten Untersuchungsgegenstand

Das aktuelle Konzept untersucht Schema-Evolution praktisch gar nicht. Das neue Konzept nimmt sie explizit auf. Das ist wichtig, weil gerade Schema-Aenderungen im Betrieb oft ein zentrales Argument in der NoSQL-vs.-SQL-Diskussion sind.

### F. Es schafft eine bessere Bruecke zwischen Demo und Benchmark

Wenn dieselbe Produktkatalog-Domaene fuer Architektur-Showcase und Lasttests verwendet wird, entsteht ein roter Faden. Im aktuellen Stand gibt es drei thematisch getrennte Welten:

- Sensor-Events als Benchmark-Domaene,
- MongoDB-spezifische Demo-Skripte,
- ein separates Web-Demo fuer Sensor-Events.

Das ist praesentierbar, aber konzeptionell nicht maximal stark.

## 1.2 Kritische Bewertung der wissenschaftlichen Aussagekraft des neuen Konzepts

Das neue Konzept ist klar besser, aber noch nicht automatisch wissenschaftlich sauber. Es hat vier zentrale Risiken.

### Risiko 1: Ein unfairer SQL-Strohmann

Das neue Konzept nennt fuer PostgreSQL relationale Mapping-Tabellen oder EAV und schliesst JSONB explizit aus, um den "klassischen SQL-Weg" zu zeigen. Das ist fuer den didaktischen Kontrast nachvollziehbar, kann wissenschaftlich aber problematisch werden.

Wenn PostgreSQL absichtlich in eine unguenstige Modellierungsform gezwungen wird, misst der Vergleich nicht mehr primaer "SQL vs. MongoDB", sondern "absichtlich starre relationale Modellierung vs. nativer Dokumentansatz".

Das kann legitim sein, aber nur wenn die Forschungsfrage genau so formuliert wird. Sonst ist der Vergleich angreifbar.

### Risiko 2: TS-02 und TS-03 sind stark modellierungsabhaengig

Die Hypothesen "Kategorie umbenennen ist in PostgreSQL klar besser" und "$lookup skaliert schlechter als Joins" sind nicht allgemeingueltige Datenbankgesetze. Sie gelten nur unter bestimmten Modellierungsentscheidungen.

Beispiele:

- TS-02 gilt nur dann in der beschriebenen Schaerfe, wenn Kategorien in MongoDB eingebettet oder dupliziert vorliegen.
- TS-03 gilt nur dann in der beschriebenen Schaerfe, wenn MongoDB fuer den Hersteller-/Bewertungsfall wirklich ueber `$lookup` arbeiten muss.
- Wenn Bewertungen oder Herstellerinformationen anders modelliert werden, verschiebt sich das Ergebnis sofort.

Das neue Konzept ist also wissenschaftlich stark, wenn die Modellierungsannahmen vorab exakt fixiert und offen begruendet werden.

### Risiko 3: Schema-Evolution ist kein reiner Performance-Test

Das Hinzufuegen eines Pflichtfelds wie `regional_tax_code` ist ein sehr guter Showcase fuer Wartbarkeit und Flexibilitaet. Es ist aber kein klassischer Performance-Benchmark.

Daraus folgt:

- Als qualitativer Architektur- und DX-Test ist das exzellent.
- Als empirischer Performance-Beweis braucht es andere Metriken, zum Beispiel Anzahl betroffener Artefakte, Anzahl notwendiger Migrationsschritte, Downtime-Risiko, Rueckwaertskompatibilitaet, Zeit bis zur lauffaehigen Aenderung.

Wenn diese Metriken nicht definiert werden, bleibt der Teil argumentativ, aber nicht sauber gemessen.

### Risiko 4: Developer Experience darf nicht nur anekdotisch bleiben

Der Anspruch auf direkten Code-Vergleich ist stark. Er muss aber operationalisiert werden, sonst bleibt er subjektiv.

Sinnvolle DX-Metriken waeren zum Beispiel:

- Anzahl Dateien, die fuer eine Aenderung angepasst werden muessen,
- Anzahl Modell-/Schema-Artefakte,
- Anzahl Migrationsschritte,
- LoC-Differenz fuer denselben Use Case,
- Zahl der benoetigten Mapping-Ebenen,
- Zeitaufwand fuer eine vordefinierte Change-Task unter identischen Regeln.

Ohne solche Kriterien ist der DX-Teil praesentationsstark, aber wissenschaftlich weich.

## 1.3 Urteil zum neuen Konzept

Das neue Konzept ist das inhaltlich beste Fundament fuer das Gesamtprojekt.

Es ist dem aktuellen Konzept ueberlegen, weil es:

- die relevante Architekturfrage direkter trifft,
- bessere und verteidigbarere Hypothesen erzeugt,
- die qualitative und quantitative Ebene sauberer trennt,
- eine bessere Storyline fuer die Praesentation bietet.

Es braucht aber drei Nachschaerfungen, um wissenschaftlich wirklich belastbar zu sein:

1. Exakte, vorab fixierte Vergleichsschemata fuer beide Datenbanken.
2. Saubere Operationalisierung der DX- und Schema-Evolutionsaussagen.
3. Klare Trennung zwischen Aussagen ueber Datenmodell, Denormalisierung und Topologie.

---

## 2. Bewertung des aktuellen Konzepts in `mongodb-v2`

## 2.1 Was am aktuellen Konzept gut ist

Das aktuelle Konzept hat reale Staerken.

### A. Es vermeidet Web- und HTTP-Overhead bewusst

Der Reset auf ein Python-CLI-Benchmark-Tool war grundsaetzlich richtig. Dadurch wird keine Anwendungsarchitektur mitgemessen, die fuer die Forschungsfrage irrelevant ist.

### B. Es hat eine reproduzierbare Grundstruktur

Positiv sind insbesondere:

- deterministische Datengenerierung,
- explizite Adapter-Schicht,
- getrennte Testfaelle,
- JSON-Exporte,
- Docker-basierte Reproduzierbarkeit.

Als Benchmark-Infrastruktur ist `mongodb-v2` grundsaetzlich gut organisiert.

### C. Es enthaelt interessante Lastbilder

T3 (Noisy Neighbor) und T4 (Resilienz) sind an sich gute Ideen. Sie koennen in einer Praesentation sehr stark wirken, wenn sie methodisch sauber umgesetzt sind.

## 2.2 Wo das aktuelle Konzept falsch gescoped ist

Das zentrale Scope-Problem ist: Das Projekt vergleicht meist nicht relationale gegen dokumentenorientierte Datenmodellierung, sondern Single-Node gegen Sharded Cluster.

Die Leitfrage in `HANDOVER.md` lautet sinngemaess bereits: Unter welchen Workload-Profilen und Topologien bietet ein horizontal verteiltes, dokumentenorientiertes System Vorteile gegenueber einem relationalen Single-Node-System?

Das ist eine andere Forschungsfrage als:

- Wann ist ein Dokumentmodell fachlich geeigneter als ein relationales Modell?
- Wann erzeugt Datenlokalitaet Vorteile?
- Wann werden Joins oder Schema-Migrationen zum echten Problem?

Das aktuelle Konzept verschiebt die Diskussion damit von "Datenmodell und Architekturparadigma" hin zu "Cluster faellt unter Parallelitaet weniger frueh an eine Grenze als Single-Node". Diese Aussage kann stimmen, ist aber inhaltlich enger und fuer die Seminarfrage weniger wertvoll.

## 2.3 Weitere konzeptionelle Schwaechen

### A. Die Domaene bevozugt das bestehende Mongo-Sharding-Narrativ

Sensor-Events mit einer klaren `region`-Partitionierung sind fast ideal fuer das bereits vorgedachte Sharding-Szenario. Das macht die Demo gut, aber den wissenschaftlichen Vergleich angreifbar, weil die Domaene schon auf die Zielarchitektur zugeschnitten ist.

### B. Es fehlen die wichtigsten Architekturkonflikte des neuen Konzepts

Nicht oder kaum untersucht werden:

- polymorphe Datenmodelle,
- komplexe Aggregate aus mehreren fachlichen Teilen,
- echte Schema-Evolution,
- Mapping-Overhead und Developer Experience.

Damit bleiben gerade die Aspekte unterbelichtet, wegen derer MongoDB gegenueber relationalen Systemen haeufig ueberhaupt diskutiert wird.

### C. Die aktuelle Forschungsfrage ist schwerer zu verteidigen

Ein Publikum kann auf das aktuelle Konzept relativ leicht antworten:

- "Ihr vergleicht eine Cluster-Architektur gegen einen Single-Node."
- "Dann beweist ihr vor allem, dass horizontale Verteilung unter bestimmten Lastbildern hilft."
- "Das sagt aber noch nicht viel darueber aus, wann man fachlich ein Dokumentmodell waehlen sollte."

Genau dieser Einwand trifft das neue Konzept deutlich weniger.

## 2.4 Urteil zum aktuellen Konzept

Das aktuelle Konzept ist als technische Benchmark-Uebung brauchbar, als bestes moegliches Konzept fuer eine Seminararbeit mit Praesentation aber nicht stark genug.

Es beantwortet eine engere, infrastrukturlastige und fuer MongoDB guenstig zugeschnittene Frage. Deshalb sollte es nicht das primaere Endkonzept bleiben.

---

## 3. Bewertung der aktuellen Testfaelle in `mongodb-v2`

Hier liegt der kritischste Teil der Analyse.

## 3.1 Positives an den Testfaellen

Die Testfaelle haben gute Absichten:

- T1 schafft eine Single-Node-Baseline,
- T2 testet Parallelitaet,
- T3 testet Stoerlast-Isolation,
- T4 testet Teilausfall.

Als Sammlung von Demonstrationsideen ist das brauchbar.

## 3.2 Warum die aktuelle wissenschaftliche Aussagekraft unzureichend ist

### Problem 1: PostgreSQL wird in den Paralleltests kuenstlich serialisiert

Im PostgreSQL-Adapter werden alle Operationen ueber genau eine Connection, genau einen Cursor und einen globalen Lock gefuehrt. Dadurch duerfen parallele Worker nie wirklich parallel auf PostgreSQL zugreifen.

Praktische Folge:

- T2, T3 und T4 messen fuer PostgreSQL nicht primaer die Datenbank unter Parallelitaet,
- sondern das Verhalten eines serialisierten Client-Zugriffs.

MongoDB nutzt dagegen den thread-sicheren `MongoClient` mit internem Pooling. Damit ist die Vergleichsbasis asymmetrisch. Ein grosser Teil des gemessenen Vorteils von MongoDB in T2 bis T4 kann daher aus der Adapter-Implementierung stammen, nicht aus der Datenbankarchitektur selbst.

Das ist ein schwerer methodischer Fehler.

### Problem 2: T3 und T4 bilden die Regionslogik fuer PostgreSQL nicht sauber ab

Die Stoerlast- und Resilienztests arbeiten konzeptionell mit Regionen wie `EU-WEST` und `US-EAST`. In MongoDB wird `region` direkt im Dokument gespeichert und abgefragt. In PostgreSQL wird `region` aber ueber die zugehoerige Sensor-Tabelle bestimmt.

Gleichzeitig erzeugt `make_event_for_region(...)` neue Events fuer PostgreSQL mit festem `sensor_id="sensor-000"`. Dieser Sensor hat aber nur genau eine zufaellig vergebene Region aus dem Seed. Das heisst:

- Ein als `EU-WEST` erzeugtes Event ist in PostgreSQL nicht automatisch ein EU-WEST-Event.
- Ein als `US-EAST` erzeugtes Event ist in PostgreSQL nicht automatisch ein US-EAST-Event.
- Die T3-/T4-Hypothesen ueber Lastisolation und regionenspezifische Ausfaelle sind fuer PostgreSQL damit nicht sauber instanziiert.

Damit vergleicht der Test nicht denselben fachlichen Lastfall auf beiden Systemen.

Auch das ist wissenschaftlich gravierend.

### Problem 3: T2 misst den behaupteten Sharding-Lesevorteil nur eingeschraenkt

T2 verwendet fuer Reads konstant dieselbe Filterregion. Damit landen die Lesezugriffe nicht verteilt ueber mehrere Shards, sondern auf demselben logischen Bereich. Wenn die Hypothese horizontale Skalierung durch Sharding zeigen soll, ist dieses Read-Muster zu eng.

T2 zeigt damit eher:

- wie sich ein Cluster bei massiv parallelen Operationen verhaelt,

nicht aber sauber:

- wie sich eine gute Shard-Verteilung auf gemischte Lesezugriffe auswirkt.

### Problem 4: T4 vermischt Read- und Write-Verkehr in einer einzigen Metrik

T4 erzeugt gemischten Traffic aus Reads und Writes, fasst die Resultate aber in einer einzigen Kennzahl zusammen und labelt diese sogar als `FILTER_READ`.

Dadurch geht analytische Schaerfe verloren. Nach einem Ausfall ist entscheidend:

- welche Requests fehlschlagen,
- ob Reads anders reagieren als Writes,
- ob einzelne Regionen unterschiedlich betroffen sind,
- wie sich die Fehlerarten unterscheiden.

Die aktuelle Zusammenfassung macht diese Differenzierung nicht sauber sichtbar.

### Problem 5: Die Tests messen nicht die spannendsten Unterschiede zwischen SQL und Dokumentmodell

Die wichtigsten Architekturunterschiede bleiben ungetestet:

- komplexes Aggregate-Read mit mehreren fachlichen Unterobjekten,
- polymorphe Strukturen,
- kontrollierte Denormalisierungskosten,
- Schema-Evolution.

T1 testet nur Inserts, Point Reads, Filter Reads und eine einfache Durchschnittsaggregation. Das ist als technische Baseline okay, aber kein starker Architekturbeweis.

### Problem 6: Die Exportdaten wirken stark, sind aber methodisch ueberinterpretiert

Beispielsweise zeigen die vorhandenen Exporte fuer T2 sehr grosse MongoDB-Vorteile. Solche Differenzen sind in der aktuellen Implementierung nicht belastbar interpretierbar, weil der PostgreSQL-Pfad bereits durch Adapter-Locking benachteiligt wird.

Mit anderen Worten: Die Zahlen sehen eindrucksvoll aus, aber sie beweisen weniger, als sie auf den ersten Blick suggerieren.

## 3.3 Was man mit den aktuellen Testfaellen noch sagen kann

Man kann mit Vorsicht sagen:

- Die Suite illustriert anschaulich bestimmte Lastbilder.
- Sie ist als technische Demo fuer ein Benchmark-Framework brauchbar.
- Sie kann Ideen fuer spaetere, bessere Experimente liefern.

Man sollte aber nicht sagen:

- dass sie bereits sauber belegt, wann MongoDB wissenschaftlich belastbar besser ist als PostgreSQL,
- dass T2 bis T4 in der aktuellen Form faire Architekturvergleiche sind,
- dass die gemessenen Unterschiede primaer aus Datenbankeigenschaften folgen.

## 3.4 Urteil zu den aktuellen Testfaellen

Die aktuellen Testfaelle sind in ihrer jetzigen Form nicht als Kernbeleg fuer die Arbeit geeignet.

Sie muessen fuer eine wissenschaftlich starke Nutzung in wesentlichen Teilen neu konzipiert werden.

---

## 4. Bewertung des Demo-Projekts in `mongodb_demo`

## 4.1 Was das Demo-Projekt gut macht

Das Demo-Projekt ist fuer seinen eigentlichen Zweck gut gebaut.

Es zeigt klar und praesentationsfreundlich:

- Dokumente in MongoDB,
- Filter auf einfachen und verschachtelten Feldern,
- Arrays,
- sichtbare Query-Darstellung,
- sichtbare PyMongo-Codebeispiele,
- Aggregationen,
- deterministische Seed-Daten,
- Live-Inserts fuer Demo-Effekte.

Gerade fuer eine Live-Praesentation ist das stark, weil das Publikum die Beziehung zwischen UI, Dokumentstruktur, Query und Code direkt sieht.

## 4.2 Wo das Demo-Projekt wissenschaftlich limitiert ist

### A. Es ist ein MongoDB-Showcase, kein kontrollierter Vergleich

Das Projekt demonstriert MongoDB, aber es vergleicht MongoDB nicht kontrolliert mit einer relationalen Alternative. Deshalb kann es die Forschungsfrage nicht empirisch beantworten.

### B. Die Domaene ist wieder MongoDB-freundlich

Sensor-Events mit verschachtelten Dokumenten, Tags, Zeitreihen und einfachen Aggregationen passen gut zu MongoDB. Das ist fuer eine Demo richtig. Als wissenschaftlicher Vergleich waere es erneut voreingenommen.

### C. Es liefert kaum Evidenz, aber viel Erklaerkraft

Die Staerke des Projekts liegt in der didaktischen Veranschaulichung, nicht in der Beweisfuehrung. Genau deshalb sollte es auch so positioniert werden.

### D. Es ist etwas breiter als die Minimalanforderung

Mit Update-Endpoint, manuellem Sensor-Trigger und zusaetzlichen UI-Flaechen geht das Projekt etwas ueber den minimalen Kern hinaus. Das ist fuer eine Live-Demo nicht zwingend schlecht, kann aber die Botschaft verbreitern.

Die Zusatzfunktionen schaden der Demo nicht massiv, sie tragen aber nur begrenzt zur Forschungsfrage bei.

## 4.3 Urteil zum Demo-Projekt

`mongodb_demo` ist ein gutes Demo-Projekt, aber kein wissenschaftlicher Hauptbeleg.

Es sollte als:

- Erklaer- und Praesentationswerkzeug,
- MongoDB-Einstieg und Visualisierung,
- didaktischer Begleiter

behalten werden.

Es sollte nicht die argumentative Last der empirischen Beweisfuehrung tragen.

---

## 5. Direkter Vergleich der drei Richtungen

| Kriterium                                | Neues Konzept                    | Aktuelles Konzept (`mongodb-v2`) | Demo-Projekt (`mongodb_demo`)    |
| ---------------------------------------- | -------------------------------- | -------------------------------- | -------------------------------- |
| Passung zur eigentlichen Forschungsfrage | Sehr hoch                        | Mittel                           | Niedrig                          |
| Erklaerkraft fuer Architekturtrade-offs  | Sehr hoch                        | Mittel                           | Mittel bis hoch                  |
| Wissenschaftliche Aussagekraft           | Hoch, wenn methodisch geschaerft | Niedrig bis mittel               | Niedrig                          |
| Fairness des Vergleichs                  | Gut erreichbar                   | Aktuell klar problematisch       | Nicht anwendbar                  |
| Praesentationswert                       | Sehr hoch                        | Hoch                             | Sehr hoch                        |
| Reproduzierbarkeit                       | Gut erreichbar                   | Grundsaetzlich gut               | Gut                              |
| Risiko methodischer Angreifbarkeit       | Mittel                           | Hoch                             | Hoch, falls als Evidenz verkauft |
| Eignung als Hauptprojekt                 | Sehr hoch                        | Niedrig                          | Niedrig                          |

---

## 6. Handlungsempfehlung

## Klare Empfehlung

Das neue Konzept sollte zur verbindlichen Hauptlinie des Projekts werden.

Die aktuelle Benchmark-Suite `mongodb-v2` sollte nicht in ihrer jetzigen Testlogik als primaere empirische Evidenz verwendet werden. Sie kann hoechstens als Vorarbeit, Prototyp oder Infrastruktur-Basis dienen. Die aktuell implementierten Testfaelle sollten fuer das Endergebnis fachlich nicht einfach "nachgeschaerft", sondern konzeptionell ersetzt werden.

Das Demo-Projekt `mongodb_demo` sollte behalten werden, aber explizit als Demo- und Erklaerartefakt, nicht als wissenschaftlicher Beleg.

## Konkrete Entscheidung

1. Uebernimm das neue Konzept als offizielles Zielmodell fuer die Arbeit.
2. Nutze `mongodb_demo` nur als Praesentations-Showcase fuer MongoDB-Grundideen.
3. Verwerfe die aktuellen Benchmark-Testfaelle in `mongodb-v2` als Kernbeleg.
4. Setze die quantitative Evaluation auf Basis des neuen Produktkatalog-Modells neu auf.

## Mindestanforderungen fuer die neue, wissenschaftlich starke Umsetzung

Damit das neue Konzept seine Staerke voll ausspielen kann, sollte die Neuimplementierung mindestens diese Regeln einhalten:

1. Die Vergleichsschemata muessen vorab fixiert werden.
2. Es muss exakt definiert werden, was eingebettet, referenziert oder normalisiert wird.
3. Beide Systeme muessen fair indexiert und mit vergleichbarer Treiber- und Pooling-Strategie betrieben werden.
4. Parallelitaet darf nicht durch einen asymmetrischen Client-Layer verzerrt werden.
5. Jeder Benchmark-Lauf sollte mehrfach wiederholt werden, idealerweise mit Konfidenzintervallen oder mindestens stabilen Wiederholungsmessungen.
6. Cache-, Warmup- und Seed-Bedingungen muessen explizit dokumentiert werden.
7. DX- und Schema-Evolution muessen ueber klare Metriken operationalisiert werden statt nur narrativ beschrieben zu werden.

## Beste moegliche Endarchitektur fuer das Gesamtprojekt

Die fachlich staerkste Endfassung waere:

1. Ein gemeinsames Produktkatalog-Datenmodell als roter Faden.
2. Ein qualitativer Architektur-Showcase fuer Polymorphie, Aggregate und Schema-Evolution.
3. Eine getrennte quantitative Benchmark-Suite fuer Datenlokalitaet, Denormalisierungs-Updates und Join-/Lookup-Kosten.
4. Ein kleines, klar ausgewiesenes Demo-Frontend nur zur Veranschaulichung, nicht zur Evidenzgewinnung.

Damit haettest du:

- eine klarere Forschungsfrage,
- eine wesentlich besser verteidigbare Methodik,
- eine staerkere Verbindung zwischen Theorie, Demo und Messung,
- und insgesamt das beste inhaltliche Endergebnis.

---

## Schlussfazit

Wenn das Ziel wirklich das beste und effektivste Ergebnis ist, dann ist die Entscheidung klar:

- Neues Konzept: ja, als neue Hauptlinie.
- Aktuelles Benchmark-Konzept: nein, nicht als finaler Scope.
- Aktuelle Testfaelle: nein, nicht als tragender wissenschaftlicher Beleg.
- Demo-Projekt: ja, aber nur als begleitender Showcase.

Der groesste Hebel liegt nicht im Reparieren einzelner bestehender Testfaelle, sondern im konsequenten Wechsel auf das neue, fachlich besser geschnittene Konzept mit sauber neu definierter Benchmark-Methodik.
