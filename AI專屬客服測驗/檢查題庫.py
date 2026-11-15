"""檢查三份題庫的題號、空值與跨案件相似度。"""

from __future__ import annotations

import csv
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_markdown(name: str) -> list[dict[str, str]]:
    result = []
    for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| Q\d+ \|", line):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if name.startswith("電商客服_新人"):
            number, topic, _kind, question, answer, _source = cells
        else:
            number, question, answer, _needed = cells
            topic = "進階題"
        result.append({"題號": f"Q{int(number[1:]):03d}", "主題": topic, "題目": question, "答案": answer, "案例": number})
    return result


def normalized(value: str) -> str:
    return re.sub(r"[\s，。、；：！？「」『』（）()·\-]", "", value)


def main() -> None:
    old = load_markdown("電商客服_新人測驗題庫.md") + load_markdown("電商客服_進階情境測驗題庫.md")
    with (ROOT / "電商客服_新增500題.csv").open(encoding="utf-8-sig", newline="") as file:
        new = [
            {"題號": row["題號"], "主題": row["主題"], "題目": row["題目"], "答案": row["參考答案"], "案例": row["案例編號"]}
            for row in csv.DictReader(file)
        ]
    all_rows = old + new
    ids = [row["題號"] for row in all_rows]
    questions = [normalized(row["題目"]) for row in all_rows]
    answers = [normalized(row["答案"]) for row in all_rows]
    assert len(old) == 40 and len(new) == 500
    assert len(set(ids)) == len(all_rows) == 540
    assert set(ids) == {f"Q{i:03d}" for i in range(1, 541)}
    assert len(set(questions)) == 540
    assert all(answers)
    print("total=540; active=500; legacy=40; duplicate_ids=0; duplicate_questions=0; blank_answers=0")

    # 只比較案例情境；共同的五種問法不能拿來判定跨案件重複。
    with (ROOT / "題庫案例來源.tsv").open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file, delimiter="|"))
    candidates = []
    for i, first in enumerate(cases):
        for j in range(i + 1, len(cases)):
            second = cases[j]
            score = SequenceMatcher(None, normalized(first["情境"]), normalized(second["情境"])).ratio()
            if score >= 0.45:
                candidates.append((score, i + 1, j + 1, first["情境"], second["情境"]))
    candidates.sort(reverse=True)
    print(f"similar_case_pairs_at_0.45={len(candidates)}")
    for score, a, b, _question_a, _question_b in candidates[:10]:
        print(f"{score:.2f} C{a:03d}/C{b:03d}")


if __name__ == "__main__":
    main()
