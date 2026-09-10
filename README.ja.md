<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — トークンではなく、注意を" width="820">
</p>

<p align="center">
  <a href="https://github.com/alexgreensh/attention-span/releases"><img src="https://img.shields.io/github/v/release/alexgreensh/attention-span?label=%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3&color=6f42c1" alt="最新バージョン"></a>
  <img src="https://img.shields.io/github/directory-file-count/alexgreensh/attention-span/output-styles?type=file&extension=md&label=%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB&color=blue" alt="スタイル数">
  <img src="https://img.shields.io/badge/%E4%BD%9C%E6%A5%AD-%E3%81%9D%E3%81%AE%E3%81%BE%E3%81%BE-2ea44f" alt="作業はそのまま（非公開テストのベンチマーク）">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/alexgreensh/attention-span?color=orange" alt="AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/for-Claude%20Code-d97757" alt="For Claude Code">
  <a href="https://github.com/alexgreensh/attention-span/stargazers"><img src="https://img.shields.io/github/stars/alexgreensh/attention-span?style=social" alt="スター数"></a>
</p>

<p align="center"><img src="assets/hero.png" alt="Attention Span のマスコット" width="900"></p>

<p align="center"><a href="README.md">English</a> · <a href="README.es-ES.md">Español</a> · <a href="README.zh-CN.md">中文</a> · <b>日本語</b> · <a href="README.pt-BR.md">Português</a> · <a href="README.de.md">Deutsch</a> · <a href="README.fr.md">Français</a></p>

Claude Code 用の[出力スタイル](https://code.claude.com/docs/en/output-styles)の小さなコレクションです。コードの書き方ではなく、*あなたへの話し方*を変えます。答えが最初、簡潔な表現、一目で読める。どれもマークダウン 1 ファイルを置いて有効にするだけです。

デフォルトで簡潔にするルールは、まずあなたの注意力に優しくあります。Claude の出力が減るのは嬉しい副作用であって、目的ではありません。

今のところ 3 つ: **Attention-kind**（フラッグシップ）、**Spartan**（簡潔、温度ゼロ）、**Rundown**（TL;DR ブリーフィング）。それぞれ下にセクションがあります。

## Attention-kind

ADHD フレンドリーなスタイル。Claude は最初に答え、短く保ち、専門用語を捨て、本当に注目する価値のあることだけを詳しく述べます。各ポイントは間隔を空けて `→` で示され、重要な言葉は **太字** になるので、太字だけ拾い読みしても答え全体がつかめます。

下では同じエンジニアリング能力のまま。変わるのは伝え方だけです。

**誰のためか:** 注意力が有限な資源のすべての人。ADHD、疲れている、フローに深く入っている、または長文の壁にうんざりしている人。

### ビフォー / アフター

質問: **「新しいソーシャルアプリにはどのデータベースを使うべき？ PostgreSQL と MongoDB のどちら？」** 同じ答えを、スタイル適用前と適用後で。

<table>
<tr>
<th align="left" width="50%">デフォルト &nbsp;·&nbsp; 430 語</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 94 語</th>
</tr>
<tr valign="top">
<td>

新しいソーシャルアプリなら、まず PostgreSQL から始めましょう。代わりに MongoDB を選ぶハードルは高いです。ソーシャルアプリは本質的に関係性だらけです。ユーザーがユーザーをフォローし、投稿はユーザーに属し、コメントは投稿に属し、いいねはユーザーと投稿を結びつけます。これはつながりの網であり、まさにリレーショナルデータベースが作られた目的です。MongoDB では、関連データを 1 つのレコードに押し込んでサイズ制限と戦うか、分割して結局アプリコードでつぎはぎして戻すかのどちらかです。フィードの問題がさらに悪化させます。タイムライン、「フォローしている人の投稿」、共通の友達の検索は、すべて Postgres が 1 クエリで行う横断的な参照に依存しています。整合性も無料で手に入ります。フォロー数や「すでにいいねしたか」のチェックには本物のトランザクションが必要だからです… *（この調子で続きます）*

</td>
<td>

**→ PostgreSQL を使いましょう。** ソーシャルアプリは関係性そのもの（友達、フォロー、いいね）で、Postgres はそれをネイティブに扱います。新規ソーシャルアプリの約 90% に適しています。

**→ 柔軟性も保てます。** JSONB カラムでスキーマレスなデータを同じデータベース内に保存できるので、Postgres を離れずに MongoDB の気楽さが得られます。

**→ MongoDB を選ぶのは** データがリンクのない自己完結ドキュメントで、初日から大量の書き込みが必要な場合だけです。

**→ MongoDB の初期の落とし穴:** 半年後、「user」が 5 種類の形で存在し、きれいな直し方がない。Postgres は構造を強制します。

**→ 次は:** マネージド Postgres（Supabase、Neon、RDS）から始めましょう。

</td>
</tr>
</table>

同じ情報。片方は一目で読めます。

### 本当に役立つのか？（測定済み、再現可能）

ベンチマークは作業と出力を分けて測定し、見出しの数字には **LLM ジャッジを使っていません**。すべての数値はこのリポジトリから再現可能です。[詳細なレポートと実行可能なハーネス](benchmarks/results/2026-08-11-benchmark.md)

- **作業は無傷です。** 非公開テストスイート付きの 12 のコーディングタスクで、スタイル off vs on: 合格率は同等（**両方 97%**、誤差範囲内）。ジャッジなし、テストが通るかどうかだけ。
- **出力は平均で約 43% 短縮**（中央値 41%）、特に重要な **冗長な答えでは 50〜71%**。もともと短い答えはほとんど変わりません。
- **要点に約 40 語ではなく約 6 語で到達。** 最初の行に答えがあるのは **75%** vs **3%**。（読みやすさ指標は当てはまりません。語数しか測れず、長文の壁を見抜けないからです。）
- **成果物は 88% の確率でそのまま完成** vs スタイルなしで 12%。メッセージやコミットを頼めば、余計な包装なしでそれだけが返ってきます。

短く、明確で、一目で把握でき、作業は無傷。より良い答えを生むとは主張しません。それはこのツールの目的ではないからです。

### 何が変わるか

- **答えが最初。** 結論が 1 行目。前置きなし。
- **デフォルトで短い。** 完全に答えるのに必要な最小限を言って、終わる。
- **重要なことだけ詳しく** 述べるので、長さそのものが重要度の合図になる。
- **平易な言葉。** 珍しい専門用語には 5 語の定義が一度だけ付く。
- **読み飛ばし用に構築。** `→` マーカー、強い太字、ポイント間の十分な余白。
- **繰り返しなし。** 各ポイントは 1 つの独立した主張をし、言い直しも再論証もしない。
- **長いタスクで方向を立て直し**、一度に 1 つの質問だけするので、話の筋を見失わない。
- **コメントも。** コードコメントも平易な言葉の「なぜを説明する」ルールを継承しますが、チャットの書式は使いません。

## Spartan

<p align="center"><img src="assets/cat-spartan.png" alt="スパルタの兜をかぶった猫が、光る 1 行にレーザーを向ける" width="860"></p>

温度を完全に取り除いた簡潔モード。Attention-kind と同じ矢印と太字ですが、率直で命令形。緩衝なし、つなぎ言葉なし、最大限の圧縮。会話ではなくシグナルが欲しい集中作業のときに。

質問: **「今週の優先事項が 3 つ、やれるのは 2 つ。何を切るかどう決める？」** どちらも実際の Opus 5 の評価出力です。

<table>
<tr>
<th align="left" width="50%">デフォルト &nbsp;·&nbsp; 310 語</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 168 語</th>
</tr>
<tr valign="top">
<td>

最も安く済むテストに落ちるものを切りましょう。1 週間遅れたら、実際に誰がどれだけ困りますか？ 3 つすべてを 4 つの簡単なフィルターに通せば、負けはだいたい自然に決まります。遅延の影響: 3 つのうち 2 つは自分で作った柔らかい締切で、1 つには本物のものがあるでしょう。待っている人、下流の依存関係、閉まる時間窓。自分で課した山から切り、誰かが自分を待っている山からは絶対に切らない。可逆性: 待つほど難しくなるものもあれば、来週でもまったく同じくらい簡単なものもある。コスト曲線が平坦なものを切る。自分以外の担当者: 委任できるか、他の人が 80% でできる優先事項は、自分にしかできないものより良い切り捨て候補です… *（この調子で続きます）*

</td>
<td>

**→ 努力や興味ではなく、やらないコストで順位付け。** それぞれに聞く: 1 週間遅れたら何が壊れる？ 影響が最も柔らかいものが切られる。

**→ 可逆なものを殺せ。** 待てる、委任できる、ペナルティなしで後で再開できるタスクは切れ。**厳しい締切** や他人が自分を待っている **依存関係** は守れ。

**→ 後悔テストを実行。** 金曜の夜、終わっていないと一番痛いのはどれ？ それを残せ。肩をすくめるだけのものが切り捨てだ。

**→ 声の大きさと重要性を分けろ。** あなたに叫んでいる優先事項は、往々にして最も価値があるのではなく、最も **不安** なだけ。音量ではなく影響で切れ。

**→ 3 つ全部を中途半端にするな。** 2 つの完成は 3 つの 66% に勝る。3 つ目への部分作業が罠。生産的に感じて何も出荷しない。

**→ 声に出して切れ。** 影響を受ける人に金曜ではなく今伝えろ。切ったと伝えるのは決断。隠すのは **遅延つきの失敗** だ。

</td>
</tr>
</table>

Attention-kind と同じスタイルのみの保証: 短く、読み飛ばしやすく、作業は無傷。[ベンチマーク](benchmarks/results/2026-08-11-benchmark.md)を参照。

## Rundown

<p align="center"><img src="assets/cat-rundown.png" alt="Rundown の猫がチェックリストにレーザーを向け、1 行が光る" width="860"></p>

ブリーフィングスタイル。**TL;DR** で始まり、状態を ✅ / 🟡 / ⬜ / ❔ のチェックリストで示し、次の選択肢に絵文字を付けて番号を振るので、番号で選べます。ステータス更新やスタンドアップ向け。**簡潔さではなく可読性とスキャンしやすさを最適化** するので、長さより明確さが大事なときに。与えられていないステータスを捏造しないガード付き。

質問: **「採用の状況を要約して: 応募者 20 人、スクリーニング 5 人、面接 2 件、オファーなし、強い候補者 1 人が離脱気味。」** どちらも実際の Opus 5 の評価出力です。

<table>
<tr>
<th align="left" width="50%">デフォルト &nbsp;·&nbsp; 読む段落</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; 見るボード</th>
</tr>
<tr valign="top">
<td>

採用はファネルの上部にあり、下部は薄い状態です。応募者 20 人、スクリーニング 5 人、面接予約 2 件。オファーはまだ出ていません。そのギャップが問題です。最も強い候補者の 1 人が、プロセスが空転している間に熱が冷めつつあります。数字: 応募者 20、スクリーニング済み 5、面接予約 2、オファー 0、リスク 1（強い候補者が離れつつある）。見立て: これは供給の問題ではなくスピードの問題。パイプラインの上部は健全ですが、オファーに転換したものがなく、最有力候補が流れています。最も価値の高い動きは、遅延が決断を代行する前に、離脱しつつある候補者を快速化すること。ボトルネック: オファー段階… *（この調子で続きます）*

</td>
<td>

TL;DR: パイプラインの上部は健全だがゴールラインが失速しており、最高の候補者が去ろうとしている。

**採用ファネル**
- ☑️ **応募者:** 20 人を確保
- ☑️ **スクリーニング:** 20 人中 5 人完了
- 🟡 **面接:** 2 件予約済み、未実施
- ⬜ **オファー:** 未作成、未送付

🔴 **ブロッカー:** 強い候補者 1 人が離脱気味。オファーの動きがなければ、何もせず失うことになる。

**次の一手:**
1. 🚀 強い候補者を快速化し、今日オファー交渉へ進む
2. 📞 決める前に予約済みの面接 2 件を実施する
3. 📋 予備として未着手の 15 人からさらにスクリーニングする
4. ✍️ いつでも出せるよう今オファーを作成する

番号を選んでください: 今候補者を救う (1)、それとも全プロセスを回して失うリスクを取る？

</td>
</tr>
</table>

## 本当にトークン代を削りたいですか？

Attention Span は、エージェントの答えを読みやすく一目で把握できるようにするためのものです。その答えのトークン代が軽くなるのは嬉しい副作用です。トークン消費の削減が本当の目標なら、大きなコストはエージェントの*話し方*ではなく、エージェントが行う*作業*です。それに真正面から取り組む姉妹ツールが 2 つあり、これらのスタイルと自然に組み合わせられます:

<p align="center"><img src="assets/save-tokens.png" alt="Outsourcerer の魔法使いと、Token Optimizer で幽霊トークンを吸い取る Attention Span の猫" width="900"></p>

**[Token Optimizer](https://github.com/alexgreensh/token-optimizer)** は、ほとんどのツールが触れないトークン浪費の 3 層に取り組みます:

- **構造的**: 肥大化した設定、未使用のスキル、古いメモリなど
- **実行時**: 冗長な出力、再読み込みなど
- **行動的**: モデルの誤った振り分け、キャッシュ期限切れ、リトライループなど

…それぞれに他にも多数。さらに出力スタックを圧縮し、作業をチェックポイント保存・復元してコンパクションをまたいでもセッションが継続するようにし、節約したトークンとドルをすべてライブダッシュボードに表示します。コンテキスト品質を測定し、それに合わせて調整する唯一のツールでもあります。安いセッションで仕事の質が落ちるのは節約とは言えないからです。

*Claude Code、Codex、OpenCode、OpenClaw、Hermes、Copilot で動作。*

**[Outsourcerer](https://github.com/alexgreensh/outsourcerer)** — お気に入りのエージェントの 1 セッションにとどまったまま。バックグラウンドで:

- すでに契約しているモデルとハーネスを横断してチームを動かす
- タスクごとに **価格ではなくベンチマークで** 最適なものを選ぶ
- 成果をチェックし、すべてのエンジンで上限を管理する

コックピットはあなたのもの。力仕事は別の場所で起きます。

*Claude Code、Codex、Antigravity、Devin、Droid、Cursor、Warp、Hermes で動作。*

Attention Span は Claude の発話量を削ります。この 2 つはスタック全体の消費を管理します。

## インストール

**一番簡単: プラグインをインストール。** 1 ステップで 3 つのスタイル、`/style` スイッチャー、ユーザー起動スキル（`/attention-kind`、`/spartan`、`/rundown`、`/tldr`）がすべて手に入ります。Claude Code で:

```
/plugin marketplace add alexgreensh/attention-span
/plugin install attention-span
```

その後 `/config` → *Output style* でスタイルを有効にするか、1 つの会話だけなら `/attention-kind` のようなスキルを入力するだけです。手動で設定したい場合は、以下の手動ステップも変わらず使えます。

**1.** スタイルを output-styles フォルダに置きます。グローバル（全プロジェクト）:

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

または 1 つのプロジェクト内の `.claude/output-styles/` に置きます。

**2.** `~/.claude/settings.json` でデフォルトに設定。一度やれば、すべてのセッションでずっと有効:

```json
{ "outputStyle": "Attention-kind" }
```

**3.** 再起動または `/clear`。これだけです。

**JSON を編集したくない場合は?** `/style` コマンドをインストールすればステップ 2 をやってくれます:

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/style.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/commands/style.md
```

`/style` でインストール済みスタイルのポップアップが表示されます。`/style spartan` で即座に設定。`/style default` で組み込みスタイルに戻ります。

`~/.claude/output-styles/` とプロジェクトの `.claude/output-styles/` を探します。グローバルスタイルは `~/.claude/settings.json` に書き込まれます。プロジェクトスタイルは `.claude/settings.local.json` に書き込まれるので、チームメイトのチェックアウトには影響しません。

**すでにインストール済みですか？** スタイルは更新されます。上の[バージョンバッジ](https://github.com/alexgreensh/attention-span/releases)と見比べて、今のバージョンを確認してください:

```bash
grep attention-span ~/.claude/output-styles/*.md
```

遅れていますか？ ステップ 1 のインストールコマンドを再実行して最新で上書きしてください。

まず 1 セッションで試したいですか？ `/config` を実行して *Output style* から選び、気に入ったら上のデフォルトを設定してください。

**コスト:** 約 650 トークン。セッションごとに 1 回追加され、最初のリクエスト後にキャッシュされます。ベンチマークでは出力が約 43% 短縮されたので、入力コストは最初の返答の後は無視できる程度です。

## Claude チャットでの使用（スキル）

スタイルは**スキル**としても提供されるので、Claude Code だけでなく Claude アプリ（claude.ai、デスクトップ、モバイル）でも使えます。上のプラグインをインストールするか、スキルファイルを直接追加して、コマンドを入力するだけです:

- `/attention-kind`、`/spartan`、`/rundown` — その会話の残りをそのスタイルで話す。
- `/tldr` — ドキュメント、スレッド、文字起こし、貼り付けたテキストをスキャンできるブリーフィングに圧縮。（スタイルは Claude が*自分の*作業を報告する形を整えます。`/tldr` は*他人が*書いたものを圧縮します。）

スキルは**ユーザー起動のみ**（`disable-model-invocation`）なので、呼ぶまでは受動的なコンテキストコストがゼロ。同じスタイルソース（`scripts/gen-skills.py`）から生成されるので、フラッグシップの文言からずれることもありません。

## 他のエージェントでの使用

スタイル本体は Claude 固有の動作を含まないプレーンなマークダウンです。Claude Code 固有の部分は各ファイル先頭の YAML フロントマター（`/config` ピッカーが読む `name`/`description` ブロック）だけです。他のエージェントはフロントマターを無視するか、エラーになるので、インストール時に取り除きます。

各スタイルファイルにはフロントマターの後に `<!-- body-start -->` マーカーがあります。取り除くコマンドは `sed` 1 つ:

```bash
curl -sfL <raw-url> | sed '1,/<!-- body-start -->/d'
```

これでクリーンな本体マークダウンが得られ、任意のエージェントのルールや指示ファイルにそのまま入れられます。

### エージェントごとのインストール

**Devin**（グローバル、Windsurf 互換経由）:

```bash
mkdir -p ~/.codeium/windsurf/memories
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && sed '1,/<!-- body-start -->/d' /tmp/attention-span.md > ~/.codeium/windsurf/memories/attention-kind.md
```

プロジェクトレベルの場合: リポジトリルートの `.windsurf/rules/attention-kind.md`。

**Codex**（グローバルな `AGENTS.md` に追記、フェンスマーカーで冪等）:

```bash
mkdir -p ~/.codex
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> ~/.codex/AGENTS.md
```

後で更新するには、まず古いブロックを（その場で）削除してからインストールを再実行: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' ~/.codex/AGENTS.md`。

**Antigravity CLI (agy)**（プロジェクトレベルの `GEMINI.md`、フェンスマーカーで冪等）:

```bash
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> GEMINI.md
```

リポジトリルートで実行してください。agy はカレントディレクトリからリポジトリルートまで遡って `GEMINI.md`（または `AGENTS.md`）を検出するので、そのプロジェクトとすべてのサブディレクトリにスタイルが適用されます。

後で更新するには、まず古いブロックを（その場で）削除してからインストールを再実行: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' GEMINI.md`。

グローバルインストール（ホームディレクトリ配下の全プロジェクト）の場合は `~/GEMINI.md` に追記してください。どのプロジェクトからの遡行でも agy が見つけます。

別のスタイルを入れるには `attention-kind.md` を `spartan.md` や `rundown.md` に置き換えてください。同じコマンドで、ファイル名だけ違います。

**注記:**

- Devin はネイティブのルールディレクトリではなく、Windsurf/Cursor 互換レイヤー経由でルールを読み込みます。`~/.codeium/windsurf/memories/` パスはグローバル、`.windsurf/rules/` はプロジェクトごとです。
- Codex は共有の `AGENTS.md` に追記するので、フェンスマーカー（`<!-- attention-span:start -->` / `<!-- attention-span:end -->`）で重複なくブロックを更新・削除できます。
- Antigravity CLI (agy) は cwd からリポジトリルートまで遡ってルールを検出し、見つかった `GEMINI.md` や `AGENTS.md` を読み込みます。単体ルールのフロントマターは非対応。グローバルインストールは、常に遡行パスに含まれる親ディレクトリ（例: `~/`）に `GEMINI.md` を置くことで実現します。
- 本体は約 650 トークンの入力で、各セッションの開始時に読み込まれます。Claude Code は最初のリクエスト後にキャッシュします。他のエージェントはプロバイダー次第でキャッシュするかもしれません。どちらにせよ、出力の節約（約 43%）は数回の返答で入力コストを大きく上回ります。
- `sed` の除去は macOS/Linux 前提です。Windows では WSL か Git Bash を使ってください。

## スタイル一覧

| スタイル | ファイル | 最適な用途 |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | ADHD、注意疲労、長文の壁にうんざりしている人 |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | スパルタンモード: 最大のシグナル、温度ゼロ、集中作業 |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | ブリーフィング、スタンドアップ、進捗更新（TL;DR + チェックボックス） |

どれも読みやすいマークダウン 1 ファイルで、調整しやすい。

## 注記

- スタイルは**メイン会話にのみ**適用されます。サブエージェントは独自のプロンプトで動きます。
- これらは Claude のコーディング動作をそのまま保ちます（`keep-coding-instructions: true`）。

## ライセンス

AGPL-3.0。[LICENSE](LICENSE) を参照。
