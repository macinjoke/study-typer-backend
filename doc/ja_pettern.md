# 概要
`ejdic-hand-utf8.txt` の日本語意味で使われる記号の意味を分析したメモ。

# 区切り

## /
最も大きな区切りに使われている。Web版ではこの区切りで改行されている。以下、 `/` で区切られた箇所をスラッシュ句と呼ぶ。

## ;
スラッシュ句内の区切り。 `;` で区切られた箇所をセミ句と呼ぶ
スラッシュ句よりも小さな区切り

## ,

スラッシュ句内での区切り。以下、 `,` で区切られた箇所をカンマ句と呼ぶ
セミ句よりも小さな区切り

## ; と , について
例(sabotage): (反乱分子や敵側による)破壊(妨害)行為;(争議中の労働者による)生産妨害 / 〈反乱分子・敵側が〉…‘を'破壊する,妨害する;〈労働者が〉…‘の'生産を妨害する
`;` があるスラッシュ句では `,` が必ずある。逆に `,` があるが `;` がないスラッシュ句は存在する。
よって `;` が出現した場合、まず セミ句として区切り、その中をカンマ句として区切るという見方をすれば良いかと思われる。

# 囲い

## ‘'
例(run): …‘を'『さっと動かす』 
例(run): 〈人・動物〉‘を'『走らせる』,競走させる 
`を` や `に` を強調するために用いられていると思われる。記号の使い方きもすぎる。
この `を` や `に` は スラッシュ句内文頭の`<>` や `()` の後で用いられ、動詞の目的語に対して使われている。

## 『』
例(run): 『走る』,駆ける
例(run): (ある状態,特に困った状態に)『なる』,陥る,達する 

スラッシュ句内で主な意味に使われるっぽい。
複数カンマ句があるときに使われる。
複数カンマ句があったとしても使われないときもある。

`《》` 内で `《+『for』(『to』)+『名』》`  のように使われる場合もある。

## 〈〉
例: 〈人が〉,〈公共の乗り物〉
主に日本語その動詞の主語や目的語となるものを示している。主語の場合は`〈hogeが〉`のように `が` が付く。目的語の場合は  `〈公共の乗物〉‘を'『運行させる』` のように `‘を'` や `‘に'`が付く。

例: <C>, <U>
可算名詞か不可算名詞かを表している。

## 《》
例:《単数形で》,《しばしば副詞[句]を伴って》
スラッシュ句内文頭について、文法上の注記を示す
例:《米》、《英》
スラッシュ句内文頭について、アメリカ英語かイギリス英語かを示す
例(run): 〈人が〉(…に)『急ぐ』,突進する《+『for』(『to』)+『名』》 
例(reason):《『reason』+『that節』》…‘と'推論する 
スラッシュ句内文頭や文末について、文法的な用法を示す

## ()
例: (…に), (…の)
文末などにつく `《》` (例:《+『for』(『to』)+『名』》) と組み合わせて使う。
その文法上の目的語に対して `に` or `の` を示す。
例(run): (ある方向へ)〈植物が〉伸びている,はい延びている
例(run):〈映画・劇など〉‘を'上映(上演)し続ける 
一般的なカッコの使い方と同様に、補足をしたり、類似後を付け加えたりしている。

# その他

## =
例(text): =textbook
例(test): =test match
単語の同一語を示している。 スラッシュ句内の文頭で用いられる。
= を使ったスラッシュ句だけの例も多い。
例(throw rug	): =scatter rug (これだけ)

## …
例(run): …‘を'『さっと動かす』 
例(run): (…に)立候補する《+『for』+『名』》 
`‘'` や `(…に)` のように使う。 `‘'` と `()` の項目を参照。


# 方針
study-typer ではどう日本語意味データを表示するか。そのまま表示しては長すぎる。

## 何個スラッシュ句を表示するか
2つ。2つめは弱めに表示。一番上のスラッシュ句は重要で主な意味っぽいので1つめとして必ず採用。2つめは7割目くらいのスラッシュ句を採用(複数の品詞をもっている単語は品詞順にスラッシュ句が並べられているため、違う品詞を採用するため。かといって最後尾はマイナーな意味の可能性がある)

## セミ句, カンマ句
- (ある場合)セミ句は1つのみにする。
- カンマ句は3つ以上は削る

## 囲い
- `()` 中の文字数が多い場合無くす。 表示を変える？
- `《米》`, `《英》` だけ残して表示変更。
  - 別案: `《》` は中の文字数が多い場合無くす。  
- `『』` 残す。表示は強調表示にしたりする。
- `〈〉` 残す。表示は変える。
- `〈U〉`, `〈C〉` は特別扱い。「可算」、「不可算」などにするか。
- `‘を'` この記号を無くす。 `‘を'` は `(…を)` に置き換える。( `‘に'` も同様)

## その他
- `=` はそのまま。 表示に工夫したい。
