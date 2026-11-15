"""把 100 個案件配上生活化情境，產生 500 題「真人視角」情境題。

不修改原本的來源檔與舊題庫；輸出新檔，並在最後自動檢查。
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "題庫案例來源.tsv"
SCENES = ROOT / "題庫生活化情境.tsv"
OUTPUT = ROOT / "電商客服_生活化情境500題.csv"

FRAME = "你是電商客服專員小安，剛接到這個案件："

QUESTION_TYPES = [
    ("查核", "優先查核", (
        "回覆之前，你會先查哪些資料？",
        "先別急著回答，你第一輪要確認什麼？",
        "你打開後台，會先核對哪些項目？",
        "為了不處理錯，你要先查證什麼？",
    )),
    ("判斷", "判斷邊界", (
        "這時候有哪個地方不能直接照顧客說的做？為什麼？",
        "你心裡要先提醒自己哪項限制？",
        "哪一個說法或假設，客服不能直接當成事實？",
        "處理這件事的界線在哪裡？",
    )),
    ("回覆", "對客回覆重點", (
        "你會怎麼回覆顧客？請寫出重點。",
        "現在能對顧客說什麼、不能說什麼？",
        "查證還沒完成，你要怎麼先回一句話安撫又不亂承諾？",
        "請用客服的口吻寫出回覆的重點內容。",
    )),
    ("處理", "下一步處理", (
        "查證完後，你接著要做什麼？",
        "你會如何推進這個案件？",
        "接下來要在系統或流程上做哪個動作？",
        "確認完資料，你的下一步是什麼？",
    )),
    ("升級", "升級條件", (
        "遇到什麼狀況，你就不該自己處理，要找主管或專責窗口？",
        "什麼時候要停止自己處理，轉給專責人員？",
        "哪些訊號代表這件事要升級？",
        "你什麼時候要把案件交給主管？",
    )),
]

# 知識治理的案件沒有顧客，回覆題改成向主管或同事回報。
INTERNAL_REPLY = (
    "你會怎麼向主管或同事回報這件事？請寫出重點。",
    "發現後，你要怎麼說明目前的狀況和你的處理建議？",
    "在正式文件還沒確認前，你能怎麼回應現場同事？",
    "請寫出回報訊息的重點內容。",
)

SOP_IDS = {
    "身分核對": "SOP-01", "訂單查詢": "SOP-02", "付款": "SOP-03", "取消訂單": "SOP-04",
    "修改訂單": "SOP-05", "物流追蹤": "SOP-06", "超商取貨": "SOP-07", "缺貨": "SOP-08",
    "預購": "SOP-09", "促銷": "SOP-10", "退貨": "SOP-11", "換貨": "SOP-12",
    "退款": "SOP-13", "瑕疵與缺件": "SOP-14", "發票": "SOP-15", "客訴": "SOP-16",
    "風險訂單": "SOP-17", "跨通路": "SOP-18", "交接與結案": "SOP-19", "知識治理": "SOP-20",
}


def read_pipe(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file, delimiter="|"))


def build() -> list[dict[str, str]]:
    cases = read_pipe(CASES)
    scenes = {row["案例編號"]: row["生活情境"] for row in read_pipe(SCENES)}
    if len(cases) != 100 or len(scenes) != 100:
        raise ValueError("案件或情境數量不是 100")

    rows: list[dict[str, str]] = []
    for index, case in enumerate(cases, start=1):
        case_id = f"C{index:03d}"
        scene = scenes[case_id]
        for kind, field, prompts in QUESTION_TYPES:
            pool = INTERNAL_REPLY if (kind == "回覆" and case["主題"] == "知識治理") else prompts
            prompt = pool[(index - 1) % len(pool)]
            rows.append({
                "題號": f"L{len(rows) + 1:03d}",
                "案例編號": case_id,
                "主題": case["主題"],
                "題型": "生活情境簡答",
                "能力面向": kind,
                "生活情境": scene,
                "題目": f"{FRAME}\n{scene}\n\n{prompt}",
                "參考答案": case[field],
                "案件摘要": case["情境"],
                "對應SOP": SOP_IDS[case["主題"]],
                "審核狀態": "示範題，待公司主管審核",
            })
    return rows


def check(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 500
    assert len({r["題號"] for r in rows}) == 500, "題號重複"
    assert len({r["題目"] for r in rows}) == 500, "題目重複"
    assert all(r["參考答案"] for r in rows), "有空白答案"
    assert len({r["生活情境"] for r in rows}) == 100, "情境重複"
    assert all("|" not in r["生活情境"] for r in rows)
    topics = Counter(r["主題"] for r in rows)
    assert len(topics) == 20 and set(topics.values()) == {25}, topics


if __name__ == "__main__":
    data = build()
    check(data)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
    print(f"完成：{len(data)} 題 → {OUTPUT.name}")
