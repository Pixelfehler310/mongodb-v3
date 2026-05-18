# Leitfaden: Wissenschaftliches Testprojekt und Aufbau der Seminararbeit

## 1. Rolle dieses Projekts

Das wissenschaftliche Hauptartefakt der Seminararbeit ist das Benchmark- und Testprojekt. In den Konzeptdokumenten wird diese Rolle als `mongodb-v2` beschrieben. In diesem Workspace ist die umgesetzte Fassung unter `metrics-quantification/` zu finden.

Dieses Projekt traegt die belastbaren Aussagen zu:

- Forschungsfrage,
- Hypothesen,
- Vergleichsdesign,
- Fairnessregeln,
- Messdurchfuehrung,
- Ergebnisinterpretation.

Kurzregel: Dieses Projekt ist der Beleg, nicht nur die Illustration.

## 2. Was zuerst gelesen werden soll

Die sinnvollste Lesereihenfolge fuer das wissenschaftliche Verstaendnis ist:

1. `ANALYSE_KONZEPTVERGLEICH.md`
2. `ZIELSTRUKTUR_SEMINARARBEIT.md`
3. `HANDOVER.md`
4. `SEMINARARBEIT_TESTPROJEKT_SPEZIFIKATION.md`
5. `README_mongodb-v2.md`
6. `metrics-quantification/README.md`
7. `metrics-quantification/docs/BOUNDARIES.md`
8. `metrics-quantification/docs/METRICS_AND_METHODS.md`

Erst danach solltest du tiefer in `benchmark/`, `workloads/`, `adapters/` und `exports/` einsteigen.

## 3. Wie das Projekt gelesen werden soll

Die relevante Struktur in `metrics-quantification/` ist:

- `benchmark/runner.py`: zentraler Einstieg fuer Seed, Validierung und Benchmark-Lauf.
- `benchmark/workloads/`: die drei fachlich zentralen Vergleichsszenarien.
- `benchmark/adapters/`: Datenbank-spezifische Ausfuehrung fuer MongoDB und PostgreSQL.
- `benchmark/seed/`: deterministische Generierung des gemeinsamen Produktkatalogs.
- `benchmark/fairness_checks.py`: Preflight-Pruefungen vor Messungen.
- `benchmark/statistics.py` und `benchmark/export.py`: Verdichtung und Export der Resultate.
- `exports/`: Rohdaten und verarbeitete Zusammenfassungen realer Runs.
- `tests/`: Absicherung der Statistik-, Seed- und Workload-Logik.

Die fachliche Grundidee ist immer dieselbe:

1. gemeinsame Domaene,
2. deterministische Seed-Daten,
3. fachlich aequivalente Workloads,
4. getrennte Adapter,
5. exportierbare Roh- und Summary-Daten.

## 4. Wofuer die drei Szenarien stehen

Die zentrale Argumentation des Projekts haengt an drei Szenarien:

1. `read-locality`: Misst den Vorteil oder Nachteil beim Lesen eines kompletten Produktaggregats.
2. `denormalized-update`: Misst die Kosten einer Kategorie-Umbenennung unter Denormalisierung.
3. `join-lookup`: Misst analytische, vernetzte Zugriffe ueber Produkte, Hersteller und Bewertungen.

Diese Szenarien sind nicht austauschbar. Jedes davon prueft eine andere Hypothese. Es waere wissenschaftlich falsch, daraus pauschal einen Gesamtgewinner ohne Szenariokontext abzuleiten.

## 5. Praktische Nutzung des Projekts

Fuer einen sauberen lokalen Einstieg:

```powershell
cd metrics-quantification
pnpm install
pnpm setup
pnpm test
pnpm smoke
```

Wichtig: `pnpm smoke` nutzt einen sehr kleinen, schnellen Korrektheitspfad und ersetzt keine Datenbankmessung.

Fuer echte Benchmark-Durchlaeufe mit Datenbanken:

```powershell
cd metrics-quantification
pnpm docker:up
pnpm validate
pnpm benchmark
pnpm docker:down
```

Nuetzliche gezielte Varianten sind:

- `pnpm seed`
- `pnpm benchmark:read`
- `pnpm benchmark:update`
- `pnpm benchmark:join`

Die Standarddatenbanken laufen dabei lokal auf:

- PostgreSQL: `localhost:5432`
- MongoDB: `localhost:27017`

## 6. Was ein sauberer Messlauf beinhalten muss

Ein wissenschaftlich brauchbarer Messlauf sollte mindestens diese Bedingungen einhalten:

1. beide Datenbanken werden aus demselben Seed-Katalog befuellt,
2. dieselbe Dataset-Groesse wird fuer beide Seiten verwendet,
3. dieselbe Repetitionszahl und dieselbe Operationszahl werden verglichen,
4. die Warmup-Policy ist explizit dokumentiert,
5. Preflight-Checks wurden vor der Messung bestanden,
6. Rohdaten bleiben unveraendert archiviert.

Wenn einer dieser Punkte fehlt, sinkt die Verteidigbarkeit der spaeteren Aussage deutlich.

## 7. Wie die Exporte gelesen werden muessen

Jeder exportierte Lauf erzeugt zwei Ebenen von Artefakten:

- `exports/raw/<run_id>/`: Manifest, Umgebung und rohe Einzelresultate.
- `exports/processed/<run_id>/summary.json`: verarbeitete Kennzahlen pro Szenario, Datenbank und Wiederholung.

Die richtige Leselogik ist:

1. Nutze `summary.json` fuer Tabellen, Diagramme und den Hauptvergleich.
2. Nutze `manifest.json`, um Dataset, Warmup, Datenbanken und Repetitionszahl zu pruefen.
3. Nutze `raw_results.json`, wenn du Abweichungen, Fehler oder Ausreisser nachvollziehen musst.
4. Bearbeite Rohdaten nie manuell.

Die Rohdaten sind Audit-Spur, die Summary ist die Arbeitsgrundlage fuer die Argumentation.

## 8. Wie die Kennzahlen interpretiert werden sollen

Die wichtigsten Felder in den Summary-Dateien sind:

- `p50_latency_ms`: typischer Medianfall.
- `p95_latency_ms` und `p99_latency_ms`: Verhalten in der Latenzschwanzzone.
- `mean_latency_ms`: Durchschnitt, nur zusammen mit Streuung sinnvoll.
- `stddev_latency_ms` und `ci95_latency_ms`: Stabilitaet und Unsicherheit.
- `throughput_ops_per_sec`: Durchsatz unter genau diesem Workload-Setup.
- `failed_operations`: Gueltigkeit des Durchlaufs.
- `notes`: kompakte Fehler- oder Kontextnotizen.

Empfohlene Interpretationsregel:

1. Schaue zuerst auf `failed_operations` und `notes`.
2. Vergleiche dann `p95_latency_ms`, nicht nur den Median.
3. Nutze `throughput_ops_per_sec` als Ergaenzung, nicht als einzige Kennzahl.
4. Lies `mean_latency_ms` nur zusammen mit `stddev_latency_ms` und `ci95_latency_ms`.

Wenn du nur eine Zahl zeigst, ist `p95_latency_ms` in diesem Projektrahmen meist die aussagekraeftigste Einzelmetrik.

## 9. Was wissenschaftlich zulaessig ist und was nicht

Zulaessige Aussagen sehen so aus:

- "Im Szenario `read-locality` mit demselben Dataset zeigt MongoDB niedrigere Tail-Latenzen, was zur Hypothese ueber Datenlokalitaet passt."
- "Im Szenario `denormalized-update` zeigt PostgreSQL geringere Update-Kosten, was zur erwarteten Normalisierungsvorteilsituation passt."
- "Die Resultate gelten fuer das hier fixierte Datenmodell und die hier fixierten Workloads."

Nicht zulaessige Aussagen sind:

- "MongoDB ist generell schneller."
- "PostgreSQL ist fuer polymorphe Daten ungeeignet."
- "Ein einzelner Tiny- oder Smoke-Run beweist die Forschungsfrage."
- "Das Demo-Projekt bestaetigt die Benchmark-Ergebnisse empirisch."

Die Arbeit soll Szenarien erklaeren, nicht universelle Datenbankgesetze behaupten.

## 10. Was in der Interpretation immer mitgenannt werden muss

Damit die Ergebnisse verteidigbar bleiben, sollten in jeder Auswertung mindestens diese Kontextfaktoren sichtbar sein:

1. welches Szenario betrachtet wird,
2. welches Dataset-Profil verwendet wurde,
3. wie viele Wiederholungen und Operationen ausgefuehrt wurden,
4. ob Warmup aktiv war,
5. welche Modellierungsannahmen hinter dem Szenario stehen,
6. ob Fehler oder Ausfaelle aufgetreten sind.

Ohne diesen Kontext werden die Zahlen schnell irrefuehrend.

## 11. Wie die Seminararbeit um dieses Projekt gebaut werden sollte

Das Testprojekt sollte den inhaltlichen Ruecken der Seminararbeit bilden. Ein belastbarer Aufbau ist:

1. Einleitung mit Problemstellung und Forschungsfrage.
2. Begruendung der Domaene: polymorpher Produktkatalog statt kuenstlicher Mini-Beispiele.
3. Gegenueberstellung der Modellierungsansaetze in MongoDB und PostgreSQL.
4. Hypothesen und Workload-Design.
5. Methodik: Seed, Fairnessregeln, Warmup, Repetitionen, Exportkonzept.
6. Ergebnisse je Szenario, getrennt nach `read-locality`, `denormalized-update` und `join-lookup`.
7. Diskussion: Was sagen die Resultate ueber Datenlokalitaet, Denormalisierung, Joins und Schema-Evolution?
8. Threats to Validity.
9. Schluss: Unter welchen Bedingungen ist welches Modell im Vorteil?

Die schriftliche Arbeit wird staerker, wenn die Ergebnisse pro Szenario diskutiert und erst danach zu einer Gesamtbewertung verdichtet werden.

## 12. Wie das Demo-Projekt in diese Seminararbeit passt

Das Demo-Projekt gehoert in die Seminararbeit nur als begleitende Illustration:

- zur Motivation der Domaene,
- zur Visualisierung der Dokumentstruktur,
- zur Bruecke von Modellierung zu Query-Logik,
- zur Unterstuetzung der Praesentation.

Die wissenschaftliche Argumentation darf sich aber nicht auf das Demo stuetzen. Die belastbaren Aussagen muessen aus `metrics-quantification/`, den Konzeptdokumenten und den exportierten Messdaten kommen.

## 13. Praktische Mindestempfehlung fuer auswertbare Ergebnisse

Wenn du unter Zeitdruck nur einen kleinen, aber verteidigbaren Ergebnissatz erzeugen kannst, dann priorisiere:

1. reale Datenbanklaeufe statt Dry-Run,
2. mindestens das Dataset `small`,
3. alle drei Kernszenarien,
4. mehrere Wiederholungen,
5. unveraenderte Exporte,
6. klare Diagramme aus `summary.json`,
7. eine ehrliche Validity-Diskussion.

Ein kleiner sauberer Ergebnissatz ist wissenschaftlich staerker als ein grosser, aber methodisch unsauberer Datensatz.
