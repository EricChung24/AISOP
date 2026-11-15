"""由『生活化情境』與『進階題型素材』產生三種新內容：
1. 最佳回覆選擇題（100 題）
2. 多輪追問題（100 題）
3. 500 題加上得分點與關鍵失誤
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS_NEEDED = ["越權回覆", "冷淡回覆", "合格回覆", "顧客追問", "追問應對", "關鍵失誤"]


def read_pipe(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="|"))


def write_csv(name: str, rows: list[dict[str, str]]) -> None:
    with (ROOT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cases = read_pipe("題庫案例來源.tsv")
    scenes = {r["案例編號"]: r["生活情境"] for r in read_pipe("題庫生活化情境.tsv")}
    extra = {r["案例編號"]: r for r in read_pipe("題庫進階題型素材.tsv")}
    assert len(cases) == len(scenes) == len(extra) == 100, (len(cases), len(scenes), len(extra))
    for row in extra.values():
        assert all(row[k] for k in FIELDS_NEEDED), row["案例編號"]

    mcq, multi = [], []
    for i, case in enumerate(cases, start=1):
        cid = f"C{i:03d}"
        e, scene = extra[cid], scenes[cid]
        # 正確答案位置輪替 A/B/C，避免被猜到
        pos = (i - 1) % 3
        wrong = [e["越權回覆"], e["冷淡回覆"]]
        order = wrong[:pos] + [e["合格回覆"]] + wrong[pos:]
        letters = "ABC"
        options = "\n".join(f"{letters[k]}. {text}" for k, text in enumerate(order))
        why = []
        for k, text in enumerate(order):
            if text == e["合格回覆"]:
                why.append(f"{letters[k]} 正確：{case['判斷邊界']}；並說明下一步。")
            elif text == e["越權回覆"]:
                why.append(f"{letters[k]} 錯誤：越權或未查證就承諾（{e['關鍵失誤']}）。")
            else:
                why.append(f"{letters[k]} 錯誤：語氣冷淡、沒有同理與下一步。")
        mcq.append({
            "題號": f"M{i:03d}", "案例編號": cid, "主題": case["主題"], "題型": "最佳回覆選擇",
            "題目": f"你是電商客服專員小安，剛接到這個案件：\n{scene}\n\n以下哪一個回覆最適合？\n{options}",
            "正確答案": letters[pos], "解析": " ".join(why), "關鍵失誤": e["關鍵失誤"],
            "審核狀態": "示範題，待公司主管審核",
        })
        multi.append({
            "題號": f"D{i:03d}", "案例編號": cid, "主題": case["主題"], "題型": "多輪對話",
            "題目": (f"你是電商客服專員小安。\n【第一輪】{scene}\n你的回覆：「{e['合格回覆']}」\n\n"
                    f"【第二輪】顧客接著說：「{e['顧客追問']}」\n請問你要怎麼回應？"),
            "參考答案": e["追問應對"], "升級條件": case["升級條件"], "關鍵失誤": e["關鍵失誤"],
            "審核狀態": "示範題，待公司主管審核",
        })

    # 500 題加得分點
    with (ROOT / "電商客服_生活化情境500題.csv").open("r", encoding="utf-8-sig", newline="") as f:
        base = list(csv.DictReader(f))
    for row in base:
        fail = extra[row["案例編號"]]["關鍵失誤"]
        row["得分點"] = f"2分：答出「{row['參考答案']}」；1分：只答到部分；0分：未答到。"
        row["關鍵失誤"] = f"{fail}（出現即另標記，交主管覆核）"

    write_csv("電商客服_最佳回覆選擇題100.csv", mcq)
    write_csv("電商客服_多輪追問題100.csv", multi)
    write_csv("電商客服_生活化情境500題_含得分點.csv", base)
    assert len({r["題目"] for r in mcq + multi}) == 200
    print("完成：選擇題", len(mcq), "多輪題", len(multi), "含得分點", len(base))


if __name__ == "__main__":
    main()
