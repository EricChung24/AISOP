import csv, json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
def rd(n):
    with (R/n).open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))
short=[]
for r in rd("電商客服_生活化情境500題_含得分點.csv"):
    short.append(dict(id=r["題號"],t="short",topic=r["主題"],kind=r["能力面向"],scene=r["生活情境"],
        prompt=r["題目"].split("\n\n")[-1],answer=r["參考答案"],fail=r["關鍵失誤"].split("（")[0]))
mcq=[]
for r in rd("電商客服_最佳回覆選擇題100.csv"):
    q=r["題目"]; opts=re.findall(r"^[ABC]\. (.*)$",q,re.M)
    mcq.append(dict(id=r["題號"],t="mcq",topic=r["主題"],scene=q.split("\n",1)[1].split("\n\n")[0],
        options=opts,correct="ABC".index(r["正確答案"]),explain=r["解析"],fail=r["關鍵失誤"]))
src={r["案例編號"]:r for r in csv.DictReader((R/"題庫進階題型素材.tsv").open(encoding="utf-8-sig"),delimiter="|")}
multi=[]
for r in rd("電商客服_多輪追問題100.csv"):
    m=re.search(r"【第一輪】(.*?)\n你的回覆：「(.*?)」\n\n【第二輪】顧客接著說：「(.*?)」",r["題目"],re.S)
    multi.append(dict(id=r["題號"],t="multi",topic=r["主題"],scene=m[1],reply=m[2],follow=m[3],
        answer=r["參考答案"],esc=r["升級條件"],fail=r["關鍵失誤"]))
data=json.dumps(dict(short=short,mcq=mcq,multi=multi),ensure_ascii=False,separators=(",",":")).replace("</","<\/")
import base64
font=base64.b64encode((R/"網站"/"Cubic_11.woff2").read_bytes()).decode()
html=(R/"網站"/"template.html").read_text(encoding="utf-8").replace("__DATA__",data).replace("__FONT__",font)
(R/"網站"/"index.html").write_text(html,encoding="utf-8")
print(len(short),len(mcq),len(multi),len(html)//1024,"KB")
