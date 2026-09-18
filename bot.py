import random
import discord
from discord import app_commands
from discord.ext import commands

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
WEIGHTS = [10, 22.5, 22.5, 22.5, 22.5]  # 超大吉: 10%, その他4つ: 22.5%ずつ (計90%)


@client.event
async def on_ready():
    # スラッシュコマンドを同期
    await tree.sync()
    print(f"ログインしました: {client.user}")


# /fortune コマンドの定義
@tree.command(name="fortune", description="今日の運勢を占います")
async def fortune(interaction: discord.Interaction):
    # 重み（確率）に従って1つ選択
    result = random.choices(RESULTS, weights=WEIGHTS, k=1)[0]

    # 選択された結果に対応する一言メッセージをランダムに1つ選択
    message = random.choice(FORTUNES[result])

    # 返信メッセージの作成
    response = f"**[{result}]**\n{message}"

    await interaction.response.send_message(response)


# Botの起動
client.run(TOKEN)