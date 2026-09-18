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

# インテントの設定
intents = discord.Intents.default()
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
}

# 結果の選択肢と確率の設定（合計100%）
RESULTS = ["超大吉", "大吉", "中吉", "吉", "凶"]
WEIGHTS = [10, 22.5, 22.5, 22.5, 22.5]


@client.event
async def on_ready():
    await tree.sync()
    print(f"ログインしました: {client.user}")


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
