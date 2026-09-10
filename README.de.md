<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — Aufmerksamkeit statt Tokens" width="820">
</p>

<p align="center">
  <a href="https://github.com/alexgreensh/attention-span/releases"><img src="https://img.shields.io/github/v/release/alexgreensh/attention-span?label=version&color=6f42c1" alt="Neueste Version"></a>
  <img src="https://img.shields.io/github/directory-file-count/alexgreensh/attention-span/output-styles?type=file&extension=md&label=stile&color=blue" alt="Stile">
  <img src="https://img.shields.io/badge/arbeit-unver%C3%A4ndert-2ea44f" alt="Arbeit unverändert (Benchmark mit versteckten Tests)">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/alexgreensh/attention-span?color=orange" alt="AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/f%C3%BCr-Claude%20Code-d97757" alt="Für Claude Code">
  <a href="https://github.com/alexgreensh/attention-span/stargazers"><img src="https://img.shields.io/github/stars/alexgreensh/attention-span?style=social" alt="Sterne"></a>
</p>

<p align="center"><img src="assets/hero.png" alt="Attention-Span-Maskottchen" width="900"></p>

<p align="center"><a href="README.md">English</a> · <a href="README.es-ES.md">Español</a> · <a href="README.zh-CN.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português</a> · <b>Deutsch</b> · <a href="README.fr.md">Français</a></p>

Eine kleine Sammlung von [Output-Styles](https://code.claude.com/docs/en/output-styles) für Claude Code, die ändern, *wie er mit dir spricht* – nicht, wie er codet. Antwort zuerst, klare Sprache, leicht zu überfliegen. Jeder Stil ist eine einzige Markdown-Datei, die du ablegst und aktivierst.

Die standardmäßig kurzen Regeln schonen zuerst deine Aufmerksamkeit. Claudes Output zu kürzen ist ein willkommener Nebeneffekt, nicht das Ziel.

Bisher drei: **Attention-kind** (der Flaggschiff-Stil), **Spartan** (knapp, null Wärme) und **Rundown** (TL;DR-Briefings). Jeder hat unten einen eigenen Abschnitt.

## Attention-kind

Ein ADHS-freundlicher Stil. Claude antwortet zuerst, bleibt kurz, lässt Fachjargon weg und geht nur auf das ein, was deine Aufmerksamkeit wirklich verdient. Jeder Punkt ist mit Abstand und einem `→` markiert, und die wichtigen Wörter sind **fett**, sodass du nur die Fettdrucke überfliegst und trotzdem die ganze Antwort hast.

Darunter steckt dieselbe Engineering-Fähigkeit. Nur die Art der Ausgabe ändert sich.

**Für wen:** alle, deren Aufmerksamkeit eine begrenzte Ressource ist. ADHS, müde, tief im Flow oder einfach fertig mit Textwänden.

### Vorher / nachher

Die Frage: **„Welche Datenbank soll ich für eine neue Social App nutzen, PostgreSQL oder MongoDB?"** Dieselbe Antwort, vor und nach dem Stil.

<table>
<tr>
<th align="left" width="50%">Standard &nbsp;·&nbsp; 430 Wörter</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 94 Wörter</th>
</tr>
<tr valign="top">
<td>

Für eine neue Social App fang mit PostgreSQL an – die Messlatte, stattdessen MongoDB zu wählen, ist hoch. Social Apps sind von Natur aus beziehungslastig: Nutzer folgen Nutzern, Posts gehören Nutzern, Kommentare gehören zu Posts, Likes verbinden Nutzer mit Posts. Das ist ein Geflecht von Verbindungen, genau das, wofür eine relationale Datenbank gebaut ist. In MongoDB stopfst du verwandte Daten entweder in einen Datensatz und kämpfst mit Größenlimits, oder du teilst sie auf und nähst sie am Ende ohnehin im App-Code wieder zusammen. Das Feed-Problem verschärft das: Timelines, „Posts von Leuten, denen du folgst" und Suchen nach gemeinsamen Freunden bauen auf genau die Querverweise, die Postgres in einer einzigen Query erledigt. Konsistenz bekommst du gratis dazu, denn Follower-Zahlen und „habe ich das schon geliked"-Prüfungen brauchen echte Transaktionen… *[und so geht es weiter]*

</td>
<td>

**→ Nutze PostgreSQL.** Eine Social App besteht aus Beziehungen (Freunde, Follows, Likes), und Postgres kann das nativ. Richtig für ~90 % neuer Social Apps.

**→ Du behältst Flexibilität.** Die JSONB-Spalte speichert schemalose Daten in derselben Datenbank – MongoDBs Lockerheit, ohne Postgres zu verlassen.

**→ Wähle MongoDB nur,** wenn deine Daten in sich geschlossene Dokumente ohne Verknüpfungen sind und du ab Tag eins massives Schreibvolumen brauchst.

**→ Die frühe MongoDB-Falle:** Nach sechs Monaten fünf verschiedene Formen von „Nutzer" und keine saubere Lösung. Postgres erzwingt die Struktur.

**→ Als Nächstes:** starte mit Managed Postgres (Supabase, Neon, RDS).

</td>
</tr>
</table>

Dieselbe Information. Eine davon liest du im Vorbeigehen.

### Hilft das wirklich? (gemessen und reproduzierbar)

Der Benchmark misst die Arbeit und die Ausgabe getrennt, und die Kernzahlen kommen **ohne LLM-Judge** aus. Jede Zahl ist aus diesem Repo reproduzierbar. [Ausführlicher Bericht und lauffähiges Harness.](benchmarks/results/2026-08-11-benchmark.md)

- **Die Arbeit bleibt unberührt.** 12 Coding-Aufgaben mit versteckten Test-Suites, Stil an vs. aus: Erfolgsraten gleich (**beide 97 %**, im Rauschbereich). Kein Judge, nur bestandene Tests.
- **~43 % kürzere Ausgabe** im Schnitt (Median 41 %), und **50–71 % bei ausufernden Antworten**, wo es zählt; schon kurze Antworten ändern sich kaum.
- **Du erreichst den Punkt in ~6 statt ~40 Wörtern.** Die Antwort steht in **75 %** der Fälle in der ersten Zeile vs **3 %**. (Lesbarkeits-Scores gelten nicht – sie messen nur Wortlänge und sehen eine Textwand nicht.)
- **Ergebnisse kommen in 88 % der Fälle sauber heraus** vs 12 % ohne Stil: Frag nach einer Nachricht oder einem Commit, und du bekommst genau das, ohne Verpackung.

Kürzer, klarer und auf einen Blick erfassbar, bei unveränderter Arbeit. Wir behaupten nicht, dass es bessere Antworten erzeugt – dafür ist es nicht gedacht.

### Was sich ändert

- **Antwort zuerst.** Fazit in Zeile eins. Kein Anlauf.
- **Standardmäßig kurz.** Sagt das Minimum, das vollständig antwortet, und hört dann auf.
- **Geht nur auf das Wesentliche ein**, sodass die Länge selbst Wichtigkeit signalisiert.
- **Klare Sprache.** Seltene Fachbegriffe bekommen eine Fünf-Wort-Erklärung, einmal.
- **Zum Überfliegen gebaut.** `→`-Marker, kräftige Fettdrucke, echter Abstand zwischen Punkten.
- **Keine Wiederholung.** Jeder Punkt bringt ein eigenes Argument, nie wiederholt oder neu argumentiert.
- **Verankert lange Aufgaben neu** und stellt jeweils nur eine Frage, damit du den Faden nie verlierst.
- **Kommentare ebenfalls.** Code-Kommentare erben die Klartext-Regel „erkläre das Warum", aber nie die Chat-Formatierung.

## Spartan

<p align="center"><img src="assets/cat-spartan.png" alt="Eine Katze mit spartanischem Helm zielt mit ihrem Laser auf eine leuchtende Zeile" width="860"></p>

Knappheit ohne jede Wärme. Gleiche Pfeile und Fettdrucke wie Attention-kind, aber hart und im Imperativ, keine Polsterung, keine Übergänge, maximale Kompression. Für konzentrierte Arbeit, wenn du Signal willst, nicht Konversation.

Die Frage: **„Drei Prioritäten diese Woche, Platz für zwei – wie entscheide ich, was ich streiche?"** Beides echte Opus-5-Eval-Ausgaben.

<table>
<tr>
<th align="left" width="50%">Standard &nbsp;·&nbsp; 310 Wörter</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 168 Wörter</th>
</tr>
<tr valign="top">
<td>

Streich die, die den billigsten Test nicht besteht: Wenn sie eine Woche rutscht – wer spürt das wirklich, und wie stark? Lass alle drei durch vier schnelle Filter laufen, und die Verliererin fällt meist von selbst heraus. Konsequenz der Verzögerung: Zwei deiner drei haben vermutlich weiche, selbst erfundene Deadlines, und eine hat eine echte – eine wartende Person, eine nachgelagerte Abhängigkeit, ein sich schließendes Zeitfenster. Streiche aus dem selbst auferlegten Stapel, nie aus dem Stapel „jemand wartet auf mich". Reversibilität: Manche Dinge werden mit dem Warten schwerer, andere sind nächste Woche genauso leicht – streiche also die mit flacher Kostenkurve. Wem gehört sie außer dir: Lässt sich eine Priorität delegieren oder von jemand anderem zu 80 % erledigen, ist sie ein besserer Kandidat als eine, die nur du kannst… *[und so geht es weiter]*

</td>
<td>

**→ Rangfolge nach den Kosten des NICHT-Tuns, nicht nach Aufwand oder Lust.** Frag bei jeder: Was bricht, wenn das eine Woche rutscht? Die mit der weichsten Konsequenz fliegt raus.

**→ Töte die reversible.** Wenn eine Aufgabe warten, delegiert oder später ohne Nachteil neu gestartet werden kann – streich sie. Schütze alles mit **harter Deadline** oder **Abhängigkeit**, bei der andere auf dich warten.

**→ Mach den Reue-Test.** Freitagabend: Welche unerledigte Aufgabe schmerzt am meisten? Die behältst du. Die, bei der du nur zuckst, fliegt raus.

**→ Trenne laut von wichtig.** Die Priorität, die dich anschreit, ist oft nur die **ängstlichste**, nicht die wertvollste. Streiche nach Wirkung, nicht nach Lautstärke.

**→ Mach nicht alle drei halb.** Zwei fertige schlagen drei zu 66 %. Teilarbeit an der dritten ist die Falle – fühlt sich produktiv an, liefert nichts.

**→ Streich es laut.** Sag es den Betroffenen jetzt, nicht am Freitag. Ein kommunizierter Schnitt ist eine Entscheidung, ein versteckter ein **verzögerter Misserfolg**.

</td>
</tr>
</table>

Dieselbe Nur-Stil-Garantie wie Attention-kind: kürzer, besser überfliegbar, Arbeit unverändert. Siehe den [Benchmark](benchmarks/results/2026-08-11-benchmark.md).

## Rundown

<p align="center"><img src="assets/cat-rundown.png" alt="Die Rundown-Katze zielt mit ihrem Laser auf eine Checkliste, eine Zeile leuchtet" width="860"></p>

Briefing-Stil. Beginnt mit einem **TL;DR**, zeigt den Stand als ✅ / 🟡 / ⬜ / ❔-Checkliste, versieht die nächsten Optionen mit Emojis und nummeriert sie, damit du per Zahl wählen kannst. Gebaut für Statusupdates und Standups. **Optimiert für Lesbarkeit und Überblick, nicht für Kürze** – also genau dann, wenn Klarheit mehr zählt als Länge. Enthält eine Schutzregel gegen erfundene Statusangaben.

Die Frage: **„Fass zusammen, wo das Hiring steht: 20 Bewerbungen, 5 gescreent, 2 Interviews, kein Angebot, eine starke Kandidatin rutscht ab."** Beides echte Opus-5-Eval-Ausgaben.

<table>
<tr>
<th align="left" width="50%">Standard &nbsp;·&nbsp; ein Absatz zum Lesen</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; ein Board zum Scannen</th>
</tr>
<tr valign="top">
<td>

Das Hiring steht oben im Trichter und ist unten dünn. Zwanzig Bewerbungen hereingekommen, fünf gescreent, zwei Interviews gebucht. Noch ist kein Angebot rausgegangen, und genau diese Lücke ist das Problem: Eine der stärksten Kandidatinnen kühlt ab, während der Prozess leer läuft. Die Zahlen: Bewerbungen 20, gescreent 5, Interviews gebucht 2, Angebote draußen 0, gefährdet 1 starke Kandidatin, die abrutscht. Die Einordnung: Das ist ein Tempoproblem, kein Angebotsproblem. Die Pipeline ist oben gesund, aber nichts ist in ein Angebot umgewandelt worden, und die beste Perspektive driftet davon. Der wertvollste Schritt ist, die abrutschende Kandidatin auf die Überholspur zu setzen, bevor die Verzögerung für uns entscheidet. Engpass: die Angebotsphase… *[und so geht es weiter]*

</td>
<td>

TL;DR: Die Pipeline ist oben gesund, aber die Zielgerade stottert – und deine beste Kandidatin ist kurz davor abzuspringen.

**Hiring-Trichter**
- ☑️ **Bewerbungen:** 20 eingegangen
- ☑️ **Screening:** 5 von 20 erledigt
- 🟡 **Interviews:** 2 gebucht, noch nicht geführt
- ⬜ **Angebot:** nicht entworfen, nicht verschickt

🔴 **Blocker:** Eine starke Kandidatin rutscht ab. Ohne Angebotsbewegung verlierst du sie automatisch.

**Dein Zug:**
1. 🚀 Starke Kandidatin auf die Überholspur, heute direkt ins Angebotsgespräch
2. 📞 Erst die 2 gebuchten Interviews führen, dann entscheiden
3. 📋 Zur Absicherung mehr von den 15 unbearbeiteten Bewerbungen screenen
4. ✍️ Das Angebot jetzt entwerfen, damit es startklar ist

Wähl eine Zahl: Kandidatin jetzt sichern (1) – oder den kompletten Prozess fahren und riskieren, sie zu verlieren?

</td>
</tr>
</table>

## Willst du wirklich deine Token-Rechnung senken?

Attention Span macht die Antworten deiner Agents lesbar und auf einen Blick erfassbar. Die leichtere Token-Rechnung dieser Antworten ist ein willkommener Nebeneffekt. Wenn Token-Ausgaben zu senken dein eigentliches Ziel ist, sind die größeren Kosten die *Arbeit* deines Agents, nicht seine Ausdrucksweise – und zwei Schwester-Tools gehen genau das an und passen natürlich zu diesen Styles:

<p align="center"><img src="assets/save-tokens.png" alt="Der Outsourcerer-Zauberer und die Attention-Span-Katze saugen mit Token Optimizer Geister-Tokens auf" width="900"></p>

**[Token Optimizer](https://github.com/alexgreensh/token-optimizer)** packt die drei Ebenen von Token-Verschwendung an, die die meisten Tools nie anfassen:

- **Strukturell**, z. B. aufgeblähte Configs, ungenutzte Skills, veraltetes Memory
- **Zur Laufzeit**, z. B. geschwätzige Ausgaben, erneutes Lesen
- **Verhaltensbedingt**, z. B. falsches Model-Routing, Cache-Ablauf, Retry-Schleifen

...und in jeder Ebene noch mehr. Darüber hinaus komprimiert er deinen Output-Stack, sichert und stellt deine Arbeit wieder her, damit deine Sessions über Kompaktierung hinweg zusammenhängend bleiben, und zeigt jedes gesparte Token und jeden Dollar auf einem Live-Dashboard. Er ist außerdem das einzige Tool, das deine Kontextqualität misst und sich darauf einstellt – denn eine billigere Session, die schlechtere Arbeit leistet, ist keine Ersparnis.

*Läuft auf Claude Code, Codex, OpenCode, OpenClaw, Hermes und Copilot.*

**[Outsourcerer](https://github.com/alexgreensh/outsourcerer)** – bleib in einer einzigen Session des Agents, den du am liebsten magst. Im Hintergrund:

- steuert er ein Team über die Modelle und Harnesses, die du bereits bezahlst
- wählt pro Aufgabe den besten **per Benchmark, nicht nur nach Preis**
- prüft deren Arbeit und wacht über deine Limits in jeder Engine

Du behältst das Cockpit; die Drecksarbeit passiert woanders.

*Funktioniert mit Claude Code, Codex, Antigravity, Devin, Droid, Cursor, Warp und Hermes.*

Attention Span kürzt, wie viel Claude sagt. Diese beiden steuern, was dein ganzer Stack ausgibt.

## Installation

**Am einfachsten: das Plugin installieren.** Ein Schritt bringt alle drei Styles, den `/style`-Wechsler und die
nutzeraufgerufenen Skills (`/attention-kind`, `/spartan`, `/rundown`, `/tldr`). In Claude Code:

```
/plugin marketplace add alexgreensh/attention-span
/plugin install attention-span
```

Danach aktivierst du einen Style unter `/config` → *Output style* – oder tippst einfach einen Skill wie `/attention-kind`
für eine einzelne Unterhaltung. Lieber manuell verdrahten? Die manuellen Schritte unten funktionieren weiterhin unverändert.

**1.** Lege den Style in deinen Output-Styles-Ordner. Global (jedes Projekt):

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

Oder lege ihn in `.claude/output-styles/` innerhalb eines einzelnen Projekts.

**2.** Setze ihn als Standard in `~/.claude/settings.json`. Einmal machen, und er ist in jeder Session für immer an:

```json
{ "outputStyle": "Attention-kind" }
```

**3.** Neustart oder `/clear`. Das war's.

**Keine Lust auf JSON-Bearbeitung?** Installiere den `/style`-Befehl – er erledigt Schritt 2 für dich:

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/style.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/commands/style.md
```

Dann zeigt `/style` ein Popup der installierten Styles. `/style spartan` setzt sofort einen. `/style default` stellt den eingebauten Style wieder her.

Er sucht in `~/.claude/output-styles/` und im `.claude/output-styles/` eines Projekts. Ein globaler Style wird in `~/.claude/settings.json` geschrieben. Ein Projekt-Style landet in `.claude/settings.local.json` und bleibt so aus den Checkouts deiner Teamkollegen raus.

**Schon installiert?** Die Styles werden aktualisiert. Prüfe deine Version und vergleiche sie mit dem [Versions-Badge](https://github.com/alexgreensh/attention-span/releases) oben:

```bash
grep attention-span ~/.claude/output-styles/*.md
```

Hinterher? Führe den Installationsbefehl aus Schritt 1 erneut aus, um mit der neuesten Version zu überschreiben.

Willst du ihn erst eine Session testen? Führe `/config` aus und wähle ihn unter *Output style* – danach setzt du oben den Standard, sobald du überzeugt bist.

**Kosten:** ~650 Tokens, einmal pro Session hinzugefügt und nach der ersten Anfrage gecacht. Der Benchmark maß ~43 % kürzere Ausgabe, die Eingabekosten sind also nach der ersten Antwort vernachlässigbar.

## Nutzung in Claude-Chats (Skills)

Die Styles gibt es auch als **Skills** – sie funktionieren damit in den Claude-Apps (claude.ai, Desktop, Mobile), nicht
nur in Claude Code. Installiere das Plugin oben oder füge die Skill-Dateien direkt hinzu und tippe einfach den Befehl:

- `/attention-kind`, `/spartan` oder `/rundown` – spricht für den Rest der Unterhaltung in diesem Stil.
- `/tldr` – komprimiert ein Dokument, einen Thread, ein Transkript oder eingefügten Text zu einem überfliegbaren Briefing. (Die
  Styles formen, wie Claude seine *eigene* Arbeit berichtet; `/tldr` komprimiert etwas, das *jemand anderes* geschrieben hat.)

Die Skills sind **nur nutzeraufrufbar** (`disable-model-invocation`), kosten also null passiven Kontext,
bis du einen aufrufst – und sie werden aus denselben Style-Quellen generiert (`scripts/gen-skills.py`), sodass sie
nie vom Flaggschiff-Wortlaut abweichen.

## Nutzung mit anderen Agents

Der Style-Body ist schlichtes Markdown ohne Claude-spezifisches Verhalten. Der einzige Claude-Code-Teil ist das YAML-Frontmatter am Anfang jeder Datei (der `name`/`description`-Block, den der `/config`-Picker liest). Andere Agents ignorieren Frontmatter oder scheitern daran – die Installation entfernt es daher.

Jede Style-Datei hat nach dem Frontmatter einen `<!-- body-start -->`-Marker. Der Entfernen-Befehl ist ein einziges `sed`:

```bash
curl -sfL <raw-url> | sed '1,/<!-- body-start -->/d'
```

Damit bekommst du sauberes Body-Markdown, bereit zum Ablegen in der Regel- oder Instruktionsdatei eines beliebigen Agents.

### Installation pro Agent

**Devin** (global, über Windsurf-Kompatibilität):

```bash
mkdir -p ~/.codeium/windsurf/memories
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && sed '1,/<!-- body-start -->/d' /tmp/attention-span.md > ~/.codeium/windsurf/memories/attention-kind.md
```

Oder auf Projektebene: `.windsurf/rules/attention-kind.md` im Repo-Root.

**Codex** (an globale `AGENTS.md` anhängen, idempotent über Markierungen):

```bash
mkdir -p ~/.codex
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> ~/.codex/AGENTS.md
```

Für ein späteres Update zuerst den alten Block (in place) entfernen, dann die Installation erneut ausführen: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' ~/.codex/AGENTS.md`.

**Antigravity CLI (agy)** (projektbezogene `GEMINI.md`, idempotent über Markierungen):

```bash
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> GEMINI.md
```

Führe das im Repo-Root aus. agy findet `GEMINI.md` (oder `AGENTS.md`), indem es vom aktuellen Verzeichnis bis zum Repo-Root hochläuft – der Style gilt also für dieses Projekt und alle Unterverzeichnisse.

Für ein späteres Update zuerst den alten Block (in place) entfernen und die Installation erneut ausführen: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' GEMINI.md`.

Für eine globale Installation (alle Projekte unter deinem Home-Verzeichnis) hänge stattdessen an `~/GEMINI.md` an – agy findet sie beim Hochlaufen von jedem Projekt aus.

Tausche `attention-kind.md` gegen `spartan.md` oder `rundown.md`, um einen anderen Style zu installieren. Gleiche Befehle, anderer Dateiname.

**Hinweise:**

- Devin lädt Regeln über seine Windsurf/Cursor-Kompatibilitätsschicht, nicht über ein natives Regelverzeichnis. Der Pfad `~/.codeium/windsurf/memories/` ist global; `.windsurf/rules/` gilt pro Projekt.
- Codex hängt an eine geteilte `AGENTS.md` an – die Markierungen (`<!-- attention-span:start -->` / `<!-- attention-span:end -->`) erlauben Updates oder Entfernen des Blocks ohne Duplikate.
- Antigravity CLI (agy) entdeckt Regeln beim Hochlaufen vom cwd zum Repo-Root und lädt jede gefundene `GEMINI.md` oder `AGENTS.md`. Kein Frontmatter-Support für eigenständige Regeln. Die globale Installation funktioniert, indem `GEMINI.md` in einem Elternverzeichnis (z. B. `~/`) liegt, das immer im Hochlauf-Pfad ist.
- Der Body hat ~650 Input-Tokens, die zu Beginn jeder Session geladen werden. Claude Code cached nach der ersten Anfrage; andere Agents cachen eventuell (anbieterabhängig). Die Output-Einsparung (~43 %) übertrifft die Eingabekosten in beiden Fällen nach wenigen Antworten deutlich.
- Das `sed`-Strip setzt macOS/Linux voraus. Unter Windows WSL oder Git Bash verwenden.

## Die Styles

| Style | Datei | Am besten für |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | ADHS, Aufmerksamkeitsmüdigkeit, alle, die Textwände satt haben |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | Spartan-Modus: maximales Signal, null Wärme, konzentrierte Arbeit |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | Briefings, Standups, Fortschrittsupdates (TL;DR + Checkboxen) |

Jeder ist eine einzige lesbare Markdown-Datei, leicht anzupassen.

## Hinweise

- Styles gelten **nur für die Hauptunterhaltung**. Subagents laufen mit ihrem eigenen Prompt.
- Sie lassen Claudes Coding-Verhalten intakt (`keep-coding-instructions: true`).

## Lizenz

AGPL-3.0. Siehe [LICENSE](LICENSE).
