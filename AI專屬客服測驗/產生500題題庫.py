"""從人工撰寫的 100 個客服案件產生 500 道可匯入題庫的情境題。"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "題庫案例來源.tsv"
OUTPUT = ROOT / "電商客服_新增500題.csv"
SUMMARY = ROOT / "電商客服_500題使用說明.md"

FIELDS = ["主題", "情境", "優先查核", "判斷邊界", "對客回覆重點", "下一步處理", "升級條件"]
QUESTION_TYPES = [
    ("查核", ("接到這個案件，客服首先應查核哪些資訊？", "回覆顧客前需要先確認什麼？", "這起案件的第一輪查證重點是什麼？", "為避免處理錯誤，應先核對哪些資料？"), "優先查核"),
    ("判斷", ("此案的處理界線是什麼？", "哪項限制必須納入判斷？", "客服不能直接假定什麼？", "此請求有哪些判斷條件？"), "判斷邊界"),
    ("回覆", ("客服對顧客的回覆應包含什麼重點？", "目前可以向顧客說明什麼？", "在結果尚未確定時，應如何回覆顧客？", "這個案件的對客說法應包含什麼？"), "對客回覆重點"),
    ("處理", ("完成必要查核後，下一個處理步驟是什麼？", "核對完成後應如何推進案件？", "客服下一步應執行哪項作業？", "查證後應如何處理這個請求？"), "下一步處理"),
    ("升級", ("出現什麼情況時，應交給主管或專責窗口？", "哪種情況需要轉交專責人員？", "何時應停止自行處理並升級？", "需要主管介入的觸發條件是什麼？"), "升級條件"),
]

SOP_IDS = {
    "身分核對": "SOP-01",
    "訂單查詢": "SOP-02",
    "付款": "SOP-03",
    "取消訂單": "SOP-04",
    "修改訂單": "SOP-05",
    "物流追蹤": "SOP-06",
    "超商取貨": "SOP-07",
    "缺貨": "SOP-08",
    "預購": "SOP-09",
    "促銷": "SOP-10",
    "退貨": "SOP-11",
    "換貨": "SOP-12",
    "退款": "SOP-13",
    "瑕疵與缺件": "SOP-14",
    "發票": "SOP-15",
    "客訴": "SOP-16",
    "風險訂單": "SOP-17",
    "跨通路": "SOP-18",
    "交接與結案": "SOP-19",
    "知識治理": "SOP-20",
}


def load_cases() -> list[dict[str, str]]:
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file, delimiter="|"))
    if len(cases) != 100:
        raise ValueError(f"預期 100 個案件，實際 {len(cases)} 個")
    if list(cases[0]) != FIELDS:
        raise ValueError("案例欄位不符合預期")
    if any(not all(case.values()) for case in cases):
        raise ValueError("案件有空白欄位")
    if len({case["情境"] for case in cases}) != 100:
        raise ValueError("案件情境有重複")
    counts = Counter(case["主題"] for case in cases)
    if set(counts) != set(SOP_IDS) or any(count != 5 for count in counts.values()):
        raise ValueError(f"每個主題應有 5 個案件：{counts}")
    return cases


def make_questions(cases: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for case_number, case in enumerate(cases, start=1):
        for kind, prompts, answer_field in QUESTION_TYPES:
            number = 40 + len(rows) + 1
            rows.append(
                {
                    "題號": f"Q{number:03d}",
                    "案例編號": f"C{case_number:03d}",
                    "主題": case["主題"],
                    "題型": "情境簡答",
                    "能力面向": kind,
                    "情境": case["情境"],
                    "題目": f"{case['情境']}。{prompts[(case_number - 1) % len(prompts)]}",
                    "參考答案": case[answer_field],
                    "對應SOP": SOP_IDS[case["主題"]],
                    "審核狀態": "示範題，待公司主管審核",
                }
            )
    if len(rows) != 500 or len({row["題號"] for row in rows}) != 500:
        raise ValueError("題號或數量錯誤")
    if len({row["題目"] for row in rows}) != 500:
        raise ValueError("題目重複")
    if any(not row["參考答案"] for row in rows):
        raise ValueError("參考答案空白")
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["主題"] for row in rows)
    table = "\n".join(f"| {topic} | {count} |" for topic, count in counts.items())
    SUMMARY.write_text(
        "# 新增 500 題使用說明\n\n"
        "來源：`題庫案例來源.tsv` 中 20 個主題、每主題 5 個人工撰寫案件；每案各有查核、判斷、回覆、處理、升級 5 題。"
        "輸出檔：`電商客服_新增500題.csv`（UTF-8 BOM，適合用試算表開啟）。"
        "題號 Q041–Q540，作為目前的主要出卷題庫。先前兩份 Q001–Q040 是示範題，與本題庫有相近情境，不合併計數。\n\n"
        "| 主題 | 新增題數 |\n|---|---:|\n"
        + table
        + "\n\n## 使用前審核\n\n"
        "這是電商客服訓練示範題，不代表任何公司的實際政策。題目中的 SOP-01 至 SOP-20 是待映射的主題編號，"
        "企業必須替換成已核准的文件與版本，並審核答案、權限、話術與適用地區。"
        "若不用 Shopify，也須依實際平台改寫操作細節。\n\n"
        "建議主管先抽查每個主題的 5 個案件，再進行評分校準；法規和發票題應由法遵或財務覆核。"
        "每題可依是否抓到主要查核或處理點給 0–2 分；未授權退款、未核身洩露資料、捏造政策列關鍵失誤。\n\n"
        "## 參考官方資料\n\n"
        "- [Shopify 訂單與付款](https://help.shopify.com/en/manual/fulfillment/managing-orders)\n"
        "- [Shopify 付款授權與請款](https://help.shopify.com/en/manual/payments/payment-authorization)\n"
        "- [Shopify 折扣組合](https://help.shopify.com/en/manual/discounts/discount-combinations)\n"
        "- [Shopify 退貨規則](https://help.shopify.com/en/manual/orders/self-serve-returns/return-rules)\n"
        "- [Shopify 物流追蹤](https://help.shopify.com/en/manual/fulfillment/setup/order-status-page/order-tracking)\n"
        "- [全國法規資料庫：消費者保護法](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0170001)\n"
        "- [行政院消費者保護處：通訊交易解除權合理例外](https://cpc.ey.gov.tw/Upload/RelFile/2022/732504/dab37c8d-df9d-4fe1-ad73-4ef34bbf8a64.pdf)\n"
        "- [財政部稅務入口網：發票退貨或折讓](https://www.etax.nat.gov.tw/etwmain/tax-info/understanding/tax-q-and-a/national/business-tax/invoice/NELbx22)\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    cases = load_cases()
    questions = make_questions(cases)
    write_outputs(questions)
    print(f"產生 {len(questions)} 題，題號 {questions[0]['題號']}–{questions[-1]['題號']}")
