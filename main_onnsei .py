from services.recorder import record_audio
from services.speech_to_text import speech_to_text
from services.text_normalizer import normalize_text
from services.ai_parser import parse_with_llm
from services.item_matcher import match_item
from services.inventory_service import update_inventory


def main():

    try:

        print("🎤 音声入力を開始します（Enterで録音終了）")

        # 1 音声録音
        audio_file = record_audio()

        if not audio_file:
            print("❌ 録音に失敗しました")
            return

        print("📝 音声認識中...")

        # 2 Whisperで文字起こし
        text = speech_to_text(audio_file)

        if not text:
            print("❌ 音声認識できませんでした")
            return

        print("認識結果:", text)

        # 3 テキスト補正
        normalized_text = normalize_text(text)

        print("補正後:", normalized_text)

        # 4 AI解析
        parsed = parse_with_llm(normalized_text)

        if not parsed:
            print("❌ AI解析に失敗しました")
            return

        print("AI解析:", parsed)

        # 必須キー確認
        required_keys = ["item", "action", "quantity"]

        for key in required_keys:
            if key not in parsed:
                print(f"❌ AI結果に {key} がありません")
                return

        # 5 品目照合
        item = match_item(parsed["item"])

        if not item:
            print("❌ 品目DBに一致するものがありません")
            return

        print("品目一致:", item)

        # 6 在庫更新
        update_inventory(
            item_id=item["id"],
            action=parsed["action"],
            quantity=parsed["quantity"],
            department=parsed.get("department", "")
        )

        print("✅ 在庫更新完了")

    except Exception as e:
        print("❌ システムエラー:", e)


if __name__ == "__main__":
    main()