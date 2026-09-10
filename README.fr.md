<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — de l'attention, pas des tokens" width="820">
</p>

<p align="center">
  <a href="https://github.com/alexgreensh/attention-span/releases"><img src="https://img.shields.io/github/v/release/alexgreensh/attention-span?label=version&color=6f42c1" alt="Dernière version"></a>
  <img src="https://img.shields.io/github/directory-file-count/alexgreensh/attention-span/output-styles?type=file&extension=md&label=styles&color=blue" alt="styles">
  <img src="https://img.shields.io/badge/travail-inchang%C3%A9-2ea44f" alt="travail inchangé (benchmark à tests cachés)">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/alexgreensh/attention-span?color=orange" alt="AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/pour-Claude%20Code-d97757" alt="Pour Claude Code">
  <a href="https://github.com/alexgreensh/attention-span/stargazers"><img src="https://img.shields.io/github/stars/alexgreensh/attention-span?style=social" alt="Étoiles"></a>
</p>

<p align="center"><img src="assets/hero.png" alt="Mascotte d'Attention Span" width="900"></p>

<p align="center"><a href="README.md">English</a> · <a href="README.es-ES.md">Español</a> · <a href="README.zh-CN.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português</a> · <a href="README.de.md">Deutsch</a> · <b>Français</b></p>

Une petite collection de [styles de sortie](https://code.claude.com/docs/en/output-styles) pour Claude Code qui changent *sa façon de vous parler*, pas sa façon de coder. La réponse d'abord, un langage simple, facile à parcourir. Chacun est un seul fichier markdown à déposer et à activer.

Les règles de concision par défaut ménagent d'abord votre attention. Réduire la sortie de Claude est un effet secondaire bienvenu, pas l'objectif.

Trois pour l'instant : **Attention-kind** (le produit phare), **Spartan** (concis, zéro chaleur) et **Rundown** (briefings TL;DR). Chacun a sa propre section ci-dessous.

## Attention-kind

Un style adapté au TDAH. Claude répond d'abord, reste bref, abandonne le jargon et ne développe que ce qui mérite vraiment votre attention. Chaque point est espacé et marqué d'un `→`, et les mots importants sont en **gras**, pour que vous puissiez ne lire que le gras et obtenir quand même toute la réponse.

La même capacité d'ingénierie en dessous. Seule la forme de la réponse change.

**Pour qui :** toute personne dont l'attention est une ressource limitée. TDAH, fatigue, pleine concentration, ou simplement marre des murs de texte.

### Avant / après

La question : **« Quelle base de données pour une nouvelle app sociale, PostgreSQL ou MongoDB ? »** La même réponse, avant et après le style.

<table>
<tr>
<th align="left" width="50%">Par défaut &nbsp;·&nbsp; 430 mots</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 94 mots</th>
</tr>
<tr valign="top">
<td>

Pour une nouvelle app sociale, commencez avec PostgreSQL, et la barre pour choisir MongoDB à la place est haute. Les apps sociales sont naturellement riches en relations : les utilisateurs suivent d'autres utilisateurs, les posts appartiennent aux utilisateurs, les commentaires appartiennent aux posts, les likes relient les utilisateurs aux posts. C'est une toile de connexions, exactement ce pour quoi une base relationnelle est faite. Dans MongoDB, soit vous entassez les données liées dans un seul enregistrement et vous vous battez avec les limites de taille, soit vous les éclatez et finissez par les recoudre dans le code de votre app de toute façon. Le problème du fil d'actualité aggrave tout : les timelines, les « posts des gens que vous suivez » et les recherches d'amis communs reposent sur le genre de références croisées que Postgres fait en une seule requête. Vous obtenez aussi la cohérence gratuitement, car les compteurs de follows et les vérifications « ai-je déjà liké » exigent de vraies transactions… *[et ça continue comme ça]*

</td>
<td>

**→ Utilisez PostgreSQL.** Une app sociale, ce sont des relations (amis, follows, likes), et Postgres les gère nativement. Le bon choix pour ~90 % des nouvelles apps sociales.

**→ Vous gardez la flexibilité.** La colonne JSONB stocke des données sans schéma dans la même base, pour avoir la souplesse de MongoDB sans quitter Postgres.

**→ Ne choisissez MongoDB que si** vos données sont des documents autonomes sans liens, et que vous avez besoin d'un volume d'écriture massif dès le premier jour.

**→ Le piège initial de MongoDB :** six mois plus tard, cinq formes différentes d'« utilisateur » et aucune solution propre. Postgres impose la structure.

**→ Ensuite :** démarrez sur du Postgres managé (Supabase, Neon, RDS).

</td>
</tr>
</table>

La même information. L'une des deux se lit d'un coup d'œil.

### Est-ce que ça aide vraiment ? (mesuré, et reproductible)

Le benchmark mesure le travail et la sortie séparément, et les chiffres clés n'utilisent **aucun juge LLM**. Chaque chiffre est reproductible depuis ce dépôt. [Article complet et harnais exécutable.](benchmarks/results/2026-08-11-benchmark.md)

- **Le travail est intact.** 12 tâches de code avec des suites de tests cachées, style off vs on : taux de réussite égaux (**97 % des deux côtés**, dans la marge de bruit). Pas de juge, juste des tests qui passent.
- **Sortie ~43 % plus courte** en moyenne (médiane 41 %), et **50-71 % sur les réponses verbeuses** là où ça compte ; les réponses déjà courtes changent à peine.
- **Vous atteignez l'essentiel en ~6 mots au lieu de ~40.** La réponse est dans la première ligne **75 %** du temps contre **3 %**. (Les scores de lisibilité ne s'appliquent pas : ils ne mesurent que la longueur des mots et ne voient pas un mur de texte.)
- **Les livrables sortent propres 88 % du temps** contre 12 % sans style : demandez un message ou un commit et vous obtenez exactement ça, sans emballage.

C'est plus court, plus clair et facile à saisir d'un coup d'œil, avec le travail intact. Nous ne prétendons pas que cela produit de meilleures réponses ; ce n'est pas son rôle.

### Ce qui change

- **La réponse d'abord.** La conclusion en première ligne. Pas de préambule.
- **Court par défaut.** Dit le minimum qui répond complètement, puis s'arrête.
- **Ne développe que l'essentiel**, donc la longueur elle-même signale l'importance.
- **Langage simple.** Les termes techniques rares reçoivent une définition de cinq mots, une fois.
- **Conçu pour être parcouru.** Marqueurs `→`, gras soutenu, vrais espaces entre les points.
- **Aucune répétition.** Chaque point avance un argument distinct, jamais reformulé ni redébattu.
- **Réancre les longues tâches** et pose une question à la fois, pour ne jamais perdre le fil.
- **Les commentaires aussi.** Les commentaires de code héritent de la règle de langage simple « expliquer le pourquoi », mais jamais du formatage de chat.

## Spartan

<p align="center"><img src="assets/cat-spartan.png" alt="Un chat casqué en spartiate vise une ligne allumée avec son laser" width="860"></p>

Le mode concis sans aucune chaleur. Mêmes flèches et gras qu'Attention-kind, mais direct et impératif, sans amorti, sans transitions, compression maximale. Pour le travail concentré quand vous voulez du signal, pas de la conversation.

La question : **« Trois priorités cette semaine, de la place pour deux, comment décider quoi couper ? »** Les deux sont de vraies sorties d'évaluation d'Opus 5.

<table>
<tr>
<th align="left" width="50%">Par défaut &nbsp;·&nbsp; 310 mots</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 168 mots</th>
</tr>
<tr valign="top">
<td>

Coupez celle qui échoue au test le moins cher : si elle glisse d'une semaine, qui le sent vraiment, et à quel point ? Passez les trois à travers quatre filtres rapides et la perdante tombe généralement d'elle-même. Conséquence du retard : deux de vos trois ont probablement des deadlines molles que vous avez inventées, et une en a une vraie, une personne qui attend, une dépendance en aval, une fenêtre qui se ferme. Coupez dans la pile auto-imposée, jamais dans la pile « quelqu'un est bloqué par moi ». Réversibilité : certaines choses deviennent plus dures en attendant, d'autres sont exactement aussi faciles la semaine prochaine, donc coupez celle dont la courbe de coût est plate. Qui d'autre la porte : si une priorité peut être déléguée ou faite à 80 % par quelqu'un d'autre, c'est un meilleur choix de coupe qu'une que vous seul pouvez faire… *[et ça continue comme ça]*

</td>
<td>

**→ Classez par coût de l'inaction, pas par effort ni par envie.** Demandez à chacune : qu'est-ce qui casse si ça glisse d'une semaine ? Celle à la conséquence la plus molle est coupée.

**→ Tuez la réversible.** Si une tâche peut attendre, être déléguée ou relancée plus tard sans pénalité, coupez-la. Protégez tout ce qui a une **deadline dure** ou une **dépendance** où d'autres sont bloqués par vous.

**→ Faites le test du regret.** Vendredi soir, quelle tâche non faite fait le plus mal ? Gardez celle-là. Celle qui vous laisse indifférent est votre coupe.

**→ Séparez le bruyant de l'important.** La priorité qui vous crie dessus est souvent juste la plus **angoissante**, pas la plus précieuse. Coupez selon l'impact, pas le volume.

**→ Ne faites pas les trois à moitié.** Deux terminées valent mieux que trois à 66 %. Le travail partiel sur la troisième est le piège : ça semble productif et ça ne livre rien.

**→ Coupez à voix haute.** Dites-le aux personnes affectées maintenant, pas vendredi. Une coupe annoncée est une décision, une coupe cachée est un **échec différé**.

</td>
</tr>
</table>

La même garantie style-seul qu'Attention-kind : plus court, plus scannable, le travail intact. Voir le [benchmark](benchmarks/results/2026-08-11-benchmark.md).

## Rundown

<p align="center"><img src="assets/cat-rundown.png" alt="Le chat Rundown vise une checklist avec son laser, une ligne allumée" width="860"></p>

Style briefing. S'ouvre avec un **TL;DR**, montre l'état sous forme de checklist ✅ / 🟡 / ⬜ / ❔, marque les prochains choix avec des emojis et les numérote pour que vous puissiez choisir par numéro. Conçu pour les mises à jour de statut et les standups. **Il optimise la lisibilité et le balayage visuel, pas la brièveté**, donc utilisez-le quand la clarté compte plus que la longueur. Inclut une garde contre l'invention de statuts non fournis.

La question : **« Résumez où en est le recrutement : 20 candidatures, 5 présélectionnées, 2 entretiens, aucune offre, une candidate forte qui glisse. »** Les deux sont de vraies sorties d'évaluation d'Opus 5.

<table>
<tr>
<th align="left" width="50%">Par défaut &nbsp;·&nbsp; un paragraphe à lire</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; un tableau à parcourir</th>
</tr>
<tr valign="top">
<td>

Le recrutement est en haut de l'entonnoir et mince en bas. Vingt candidatures reçues, cinq présélectionnées, deux entretiens réservés. Aucune offre n'est encore partie, et cet écart est le problème : l'une des candidates les plus fortes refroidit pendant que le processus tourne au ralenti. Les chiffres : candidatures 20, présélectionnées 5, entretiens réservés 2, offres 0, à risque 1 candidate forte qui s'éloigne. La lecture : c'est un problème de vitesse, pas d'offre. Le pipeline est sain en haut, mais rien ne s'est converti en offre, et la meilleure piste dérive. L'action à plus forte valeur est d'accélérer la candidate qui glisse avant que le délai ne décide pour nous. Goulot d'étranglement : l'étape de l'offre… *[et ça continue comme ça]*

</td>
<td>

TL;DR : Le pipeline est sain en haut mais la ligne d'arrivée calle, et votre meilleure candidate est sur le point de partir.

**Entonnoir de recrutement**
- ☑️ **Candidatures :** 20 reçues
- ☑️ **Présélection :** 5 sur 20 faites
- 🟡 **Entretiens :** 2 réservés, pas encore menés
- ⬜ **Offre :** pas rédigée, pas envoyée

🔴 **Blocage :** Une candidate forte glisse. Sans mouvement d'offre, vous la perdez par défaut.

**À vous de jouer :**
1. 🚀 Accélérer la candidate forte, passer direct à la discussion d'offre aujourd'hui
2. 📞 Mener les 2 entretiens réservés avant de décider
3. 📋 Présélectionner davantage parmi les 15 candidatures non traitées en backup
4. ✍️ Rédiger l'offre maintenant pour qu'elle soit prête à envoyer

Choisissez un numéro : sauver la candidate maintenant (1), ou suivre tout le processus et risquer de la perdre ?

</td>
</tr>
</table>

## Vous voulez vraiment réduire votre facture de tokens ?

Attention Span sert à rendre les réponses de vos agents lisibles et faciles à saisir d'un coup d'œil. La facture de tokens allégée de ces réponses est un effet secondaire bienvenu. Si réduire les dépenses de tokens est votre vrai objectif, le plus gros coût est le *travail* que fait votre agent, pas sa façon de parler, et deux outils frères s'y attaquent directement, en s'associant naturellement à ces styles :

<p align="center"><img src="assets/save-tokens.png" alt="Le magicien Outsourcerer et le chat Attention Span aspirant les tokens fantômes avec Token Optimizer" width="900"></p>

**[Token Optimizer](https://github.com/alexgreensh/token-optimizer)** s'attaque aux trois couches de gaspillage de tokens que la plupart des outils ne touchent jamais :

- **Structurelle**, ex. configs gonflées, skills inutilisées, mémoire obsolète
- **À l'exécution**, ex. sortie verbeuse, relectures
- **Comportementale**, ex. mauvais routage de modèle, expiration de cache, boucles de retry

...et davantage dans chacune. En plus, il compresse votre pile de sortie, fait des checkpoints et restaure votre travail pour que vos sessions restent continues malgré la compaction, et affiche chaque token et dollar économisé sur un tableau de bord en direct. C'est aussi le seul outil qui mesure la qualité de votre contexte et s'y adapte, car une session moins chère qui fait du moins bon travail n'est pas une économie.

*Fonctionne sur Claude Code, Codex, OpenCode, OpenClaw, Hermes et Copilot.*

**[Outsourcerer](https://github.com/alexgreensh/outsourcerer)** — restez dans une seule session de l'agent que vous préférez. En arrière-plan, il :

- fait tourner une équipe sur les modèles et harnais que vous payez déjà
- choisit le meilleur par tâche **par benchmark, pas seulement par prix**
- vérifie leur travail et surveille vos limites dans chaque moteur

Vous gardez le cockpit ; le gros du travail se fait ailleurs.

*Fonctionne avec Claude Code, Codex, Antigravity, Devin, Droid, Cursor, Warp et Hermes.*

Attention Span réduit combien Claude dit. Ces deux-là gouvernent combien toute votre stack dépense.

## Installation

**Le plus simple : installez le plugin.** Une étape donne les trois styles, le sélecteur `/style` et les
skills invoquées par l'utilisateur (`/attention-kind`, `/spartan`, `/rundown`, `/tldr`). Dans Claude Code :

```
/plugin marketplace add alexgreensh/attention-span
/plugin install attention-span
```

Puis activez un style sous `/config` → *Output style*, ou tapez simplement une skill comme `/attention-kind`
pour une conversation. Vous préférez le câbler à la main ? Les étapes manuelles ci-dessous fonctionnent toujours, inchangées.

**1.** Déposez le style dans votre dossier output-styles. Global (tous les projets) :

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

Ou placez-le dans `.claude/output-styles/` dans un seul projet.

**2.** Définissez-le par défaut dans `~/.claude/settings.json`. À faire une fois, et c'est actif sur chaque session, pour toujours :

```json
{ "outputStyle": "Attention-kind" }
```

**3.** Redémarrez ou faites `/clear`. C'est tout.

**Vous ne voulez pas éditer de JSON ?** Installez la commande `/style` et elle fait l'étape 2 pour vous :

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/style.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/commands/style.md
```

Ensuite `/style` affiche un popup des styles installés. `/style spartan` en active un immédiatement. `/style default` restaure le style intégré.

Il cherche dans `~/.claude/output-styles/` et dans le `.claude/output-styles/` d'un projet. Un style global est écrit dans `~/.claude/settings.json`. Un style de projet est écrit dans `.claude/settings.local.json`, donc il reste hors des checkouts de vos coéquipiers.

**Déjà installé ?** Les styles se mettent à jour. Vérifiez votre version et comparez-la au [badge de version](https://github.com/alexgreensh/attention-span/releases) ci-dessus :

```bash
grep attention-span ~/.claude/output-styles/*.md
```

En retard ? Relancez la commande d'installation de l'étape 1 pour écraser avec la dernière version.

Envie de l'essayer pour une session d'abord ? Lancez `/config` et choisissez-le sous *Output style*, puis définissez le défaut ci-dessus une fois convaincu.

**Coût :** ~650 tokens, ajoutés une fois par session et mis en cache après la première requête. Le benchmark a mesuré ~43 % de sortie en moins, donc le coût d'entrée est négligeable après la première réponse.

## Utilisation dans les chats Claude (skills)

Les styles sont aussi livrés en **skills**, donc ils fonctionnent dans les apps Claude (claude.ai, desktop, mobile), pas
seulement dans Claude Code. Installez le plugin ci-dessus, ou ajoutez les fichiers skill directement, puis tapez la commande :

- `/attention-kind`, `/spartan` ou `/rundown` — parle dans ce style pour le reste de la conversation.
- `/tldr` — compresse un document, un thread, une transcription ou un texte collé en un briefing scannable. (Les
  styles façonnent comment Claude rapporte son *propre* travail ; `/tldr` compresse quelque chose que *quelqu'un d'autre* a écrit.)

Les skills sont **invoquées par l'utilisateur uniquement** (`disable-model-invocation`), donc elles coûtent zéro contexte passif
jusqu'à ce que vous en appeliez une, et elles sont générées depuis les mêmes sources de style (`scripts/gen-skills.py`), donc elles
ne dérivent jamais du texte phare.

## Utilisation avec d'autres agents

Le corps du style est du markdown simple sans comportement spécifique à Claude. La seule partie Claude Code est le frontmatter YAML en haut de chaque fichier (le bloc `name`/`description` que lit le sélecteur `/config`). Les autres agents ignorent ou bloquent sur le frontmatter, donc l'installation le retire.

Chaque fichier de style a un marqueur `<!-- body-start -->` après le frontmatter. La commande de suppression est un seul `sed` :

```bash
curl -sfL <raw-url> | sed '1,/<!-- body-start -->/d'
```

Cela donne un markdown de corps propre, prêt à déposer dans le fichier de règles ou d'instructions de n'importe quel agent.

### Installation par agent

**Devin** (global, via la compatibilité Windsurf) :

```bash
mkdir -p ~/.codeium/windsurf/memories
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && sed '1,/<!-- body-start -->/d' /tmp/attention-span.md > ~/.codeium/windsurf/memories/attention-kind.md
```

Ou au niveau projet : `.windsurf/rules/attention-kind.md` à la racine de votre dépôt.

**Codex** (ajout au `AGENTS.md` global, idempotent via les marqueurs balisés) :

```bash
mkdir -p ~/.codex
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> ~/.codex/AGENTS.md
```

Pour mettre à jour plus tard, retirez d'abord l'ancien bloc (en place), puis relancez l'installation : `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' ~/.codex/AGENTS.md`.

**Antigravity CLI (agy)** (`GEMINI.md` au niveau projet, idempotent via les marqueurs balisés) :

```bash
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> GEMINI.md
```

Lancez ceci à la racine de votre dépôt. agy découvre `GEMINI.md` (ou `AGENTS.md`) en remontant du répertoire courant vers la racine du dépôt, donc le style s'applique à ce projet et à tous les sous-répertoires.

Pour mettre à jour plus tard, retirez d'abord l'ancien bloc (en place), puis relancez l'installation : `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' GEMINI.md`.

Pour une installation globale (tous les projets sous votre répertoire personnel), ajoutez plutôt à `~/GEMINI.md` ; agy le trouvera en remontant depuis n'importe quel projet.

Remplacez `attention-kind.md` par `spartan.md` ou `rundown.md` pour installer un autre style. Mêmes commandes, nom de fichier différent.

**Notes :**

- Devin charge les règles via sa couche de compatibilité Windsurf/Cursor, pas un répertoire de règles natif. Le chemin `~/.codeium/windsurf/memories/` est global ; `.windsurf/rules/` est par projet.
- Codex ajoute à un `AGENTS.md` partagé, donc les marqueurs balisés (`<!-- attention-span:start -->` / `<!-- attention-span:end -->`) permettent de mettre à jour ou retirer le bloc sans doublons.
- Antigravity CLI (agy) découvre les règles en remontant du cwd vers la racine du dépôt, en chargeant tout `GEMINI.md` ou `AGENTS.md` trouvé. Pas de support du frontmatter pour les règles autonomes. L'installation globale fonctionne en plaçant `GEMINI.md` dans un répertoire parent (ex. `~/`) qui est toujours sur le chemin de remontée.
- Le corps fait ~650 tokens d'entrée, chargés au début de chaque session. Claude Code les met en cache après la première requête ; les autres agents peuvent ou non les mettre en cache (selon le fournisseur). Les économies de sortie (~43 %) dépassent largement le coût d'entrée en quelques réponses dans tous les cas.
- La suppression par `sed` suppose macOS/Linux. Sous Windows, utilisez WSL ou Git Bash.

## Les styles

| Style | Fichier | Idéal pour |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | TDAH, fatigue attentionnelle, tous ceux qui en ont marre des murs de texte |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | Mode spartiate : signal maximal, zéro chaleur, travail concentré |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | Briefings, standups, mises à jour de progression (TL;DR + cases à cocher) |

Chacun est un seul fichier markdown lisible, facile à adapter.

## Notes

- Les styles s'appliquent **à la conversation principale uniquement**. Les sous-agents tournent avec leur propre prompt.
- Ils préservent le comportement de code de Claude (`keep-coding-instructions: true`).

## Licence

AGPL-3.0. Voir [LICENSE](LICENSE).
