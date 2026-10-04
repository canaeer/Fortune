import os
import random
from threading import Thread

import discord
from discord import app_commands
from flask import Flask

# --------------------------------------------------
# Render用 Webサーバー設定 (スリープ防止用)
# --------------------------------------------------
app = Flask("")


@app.route("/")
def home():
    return "Bot is running!"


def run():
    # Renderで割り当てられるPORT番号を取得（デフォルトは8080）
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Botのトークンをここに貼り付けます
TOKEN = os.getenv("DISCORD_TOKEN")

# インテントの設定（メッセージ読み取り権限を追加）
intents = discord.Intents.default()
intents.message_content = True  # ←メッセージの内容を検出するために必須です

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# おみくじのデータ（結果: 一言メッセージのリスト）
FORTUNES = {
    "超大吉": [
        "これ以上ない最高の日になる予感がする...!!!!",
    ],
    "大吉": [
        "今日も頑張ろーーー！！なんでもできる気がするね!",
    ],
    "中吉": [
        "散歩でもしよっか！！",
    ],
    "吉": [
        "今日はアイスでも食べよ～",
    ],
    "凶": [
        "何もしない方がいいかもね...今日はもう寝よう...",
    ],
    "ドラ吉": [
        "運がいいね...!!今日はずっとそばにいるね！！",
    ],
}

# 結果の選択肢と確率の設定（合計100%）
RESULTS = ["ドラ吉", "超大吉", "大吉", "中吉", "吉", "凶"]
WEIGHTS = [1, 9, 22.5, 22.5, 22.5, 22.5]


# --------------------------------------------------
# 特定の発言に反応する応答の設定
# --------------------------------------------------
RESPONSE_PAIRS = {
    "おはよう": "おはよう～今日も頑張って行こ～！！",
    "おつかれ": "おつかれさま～～晩御飯早く作って！！",
    "おやすみ": "また明日ね、{name}！",
    "ドラゴン": "なぁに？",
    "どらごん": "ガォーーーーー！！",
    "ド": "よんだ？？",
    "呼んでない": "そっか...",
    "よんでない": "ﾌﾝ",
    "かわいい": "ｴﾍﾍ...",
    "了解": "{name}ﾘｮｰｶｲ!!",
    "寝": "...もう寝るの？？",
    "ごめん": "今日は一緒に遊んでくれる...？",
    "遊": "ありがとう{name}！！一緒に遊ぼ！！",
    "cana": "canaさんは今いないよ！！",
    "かな": "canaさんは今いないよ！！",
    
    # 追加したい場合はここに "キーワード": "返答" の形式で増やせます
}


@client.event
async def on_ready():
    await tree.sync()
    print(f"ログインしました: {client.user}")


# --------------------------------------------------
# メッセージ受信時の処理
# --------------------------------------------------
@client.event
async def on_message(message: discord.Message):
    # Bot自身のメッセージには反応しない
    if message.author == client.user:
        return

    # ユーザーの表示名（サーバー上のニックネーム、無ければアカウント名）を取得
    user_name = message.author.display_name

    # メッセージの中にキーワードが含まれているかチェックして返答
    for word, reply_template in RESPONSE_PAIRS.items():
        if word in message.content:
            # {name} の部分を実際のユーザー名に置き換えて送信
            reply = reply_template.format(name=user_name)
            await message.channel.send(reply)
            break


@tree.command(name="fortune", description="今日の運勢を占います")
async def fortune(interaction: discord.Interaction):
    # 重み（確率）に従って1つ選択
    result = random.choices(RESULTS, weights=WEIGHTS, k=1)[0]
    message = random.choice(FORTUNES[result])

    response = f"**[{result}]**\n{message}"
    await interaction.response.send_message(response)


# --------------------------------------------------
# 起動処理
# --------------------------------------------------
if __name__ == "__main__":
    keep_alive()  # Webサーバーをバックグラウンドで起動
    client.run(TOKEN)
