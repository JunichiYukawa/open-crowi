# /introduction

## これは何？

社内で散らばっているナレッジをまとめるためのツールです。

## どうやって使うの？

仕様や設計などを書きます。また、GoogleDriveへの参照を貼ったりできます。

## 今までのGoogleDocsやGithubで書き溜めたやつはどうするの？

この社内Wikiは今までのドキュメントを置き換えるものでは**ありません**。
今までのドキュメントへのURL参照を書いてくれればそれでOKです。

## GoogleのWikiもあるけど？

他部署に公開するものは、下記のWikiに書いたほうが良いです。本Wikiは参照するのにもアカウント発行が必要だからです。
別に社内からのアクセスを制限していないので、アカウント発行して見る分には全然問題ありません。

システム情報
https://sites.google.com/a/ohmae.ac.jp/system_info/

テクニカルサポート
https://sites.google.com/a/ohmae.ac.jp/tekunikarusapoto/home

#### 〜よく言われること〜

 <span style="color:red">Q. GoogleSiteがあるのに、このWiki要らないんじゃない？</span>
 A. GoogleSiteの更新が滞っている上、GoogleSiteが開発者向きに特化しておらず使いづらいためこのWikiを使っています。
このWikiはテキストベースで書けます。画像の表示やアップロードや表示も高速です。
プログラム言語を貼り付けたりモデル図も簡単に書くことができます。

 <span style="color:red">Q. GoogleSiteはどうするの？</span>
 A. 社外向けの資料はGoogleSiteを使っていくことになります。社内Wikiは必要に応じてGoogleSiteのリンクを貼るだけです。


### どうやって書いていくの

 - Markdownのフォーマットで書くことができます。
[Markdownチートシート](https://qiita.com/oreo/items/82183bfbaac69971917f)
 - 画像やファイルがマウスでのドラッグアンドドロップで置けます。
 - [plantUML](http://plantuml.com/)に対応しています。こんな図もテキストで書くことができます。

```plantuml
package "外部データベース" as ext <<Database>> {
    entity "顧客マスタ" as customer <<M,AAFFAA)>> {
        + 顧客ID [PK]
        --
        顧客名
        郵便番号
        住所
        電話番号
        FAX
    }
}

package "開発対象システム" as target_system {
    /'
      マスターテーブルを M、トランザクションを T などと安直にしていますが、
      チーム内でルールを決めればなんでも良いと思います。交差テーブルは "I" とか。
      角丸四角形が描けない代替です。
      １文字なら "主" とか "従" とか日本語でも OK だったのが受ける。
     '/
    entity "注文テーブル" as order <<主,FFAA00)>> {
        + 注文ID [PK]
        --
        # 顧客ID [FK]
        注文日時
        配送希望日
        配送方法
        お届け先名
        お届け先住所
        決済方法
        合計金額
        消費税額
    }

    entity "注文明細テーブル" as order_detail <<T,FFAA00)>> {
        + 注文ID   [PK]
        + 明細番号 [PK]
        --
        # SKU [FK]
        注文数
        税抜価格
        税込価格
    }

    entity "SKUマスタ" as sku <<M,AAFFAA)>> {
        + SKU [PK]
        --
        # 商品ID [FK]
        カラー
        サイズ
        重量
        販売単価
        仕入単価
    }

    entity "商品マスタ" as product <<M,AAFFAA)>> {
        + 商品ID [PK]
        --
        商品名
        原産国
        # 仕入先ID [FK]
        商品カテゴリ
        配送必要日数
    }

    entity "仕入先マスタ" as vendor <<M,AAFFAA)>> {
        + 仕入先ID [PK]
        --
        仕入れ先名
        郵便番号
        住所
        電話番号
        FAX番号
    }
}

customer       |o-ri-o{     order
order          ||-ri-|{     order_detail
order_detail    }-do-||      sku
sku             }-le-||     product
product        }o-le-||     vendor
```

### 記事の探し方
 - 全文検索できます

### ディレクトリ階層

- このWikiの使い方
- AirCampusポータル
  - ポータル概要
  - 仕様
  - 設計資料など
- Mobile
  - モバイル概要
  - 仕様
  - 設計資料など

随時更新していきます。
