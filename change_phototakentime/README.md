# 画像・動画ファイルの更新時刻の修正

## 機能

Google Photos などからダウンロードした画像や動画のタイムスタンプが、ダウンロードした日時のものになっている。このスクリプトを使って、そのタイムスタンプを撮影時刻に修正することができる。このスクリプトは、次のような処理で画像や動画の撮影時刻を取得している。

1. Google Photos から画像や動画などを一括ダウンロードする際、ファイルのメタ情報が保存されている JSON ファイルも画像や動画と同じフォルダに自動的にダウンロードされいる。このスクリプトはまず各画像や動画と同じ名前の JSON ファイルを検索し、そこから撮影時刻を取得する。

2. 手順 1 で取得できなかった場合、ファイルを開いて EXIF の DateTimeOriginal から撮影時刻を取得する。

3. 手順 2 で取得できなかった場合（MP4 動画の場合）、FFMPEG を使ってファイルの creation\_time 情報を探し、その時刻を取得する。


## 実行方法

修正対象となる画像を from フォルダに入れる。from フォルダのし下にサブフォルダを作成してもよい。次に、修正後のファイルを保存するための空フォルダ to を作成する。from および to フォルダを要したあとに、次のようにスクリプトを実行する。


```bash
python format_images.py from to
```

更新された画像は to フォルダの下に保存される。この際に画像は撮影日時を利用して年、月のサブフォルダの下に保存される。たとえば、2024 年 3 月 20 日に撮影した画像の場合は、/to/2024/03 に保存される。








