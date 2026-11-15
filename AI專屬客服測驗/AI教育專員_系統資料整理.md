# AI 教育專員：依公司 SOP 客製化新人訓練

整理日期：2026-11-14。此文件是產品規劃與公開資料整理；資料夾建立時沒有既有 SOP 或測驗檔案。電商客服僅作為示範情境，不代表任何店家的實際政策。

## 目標與使用流程

讓企業上傳或填寫自己的政策，新人依職務學習、練習接案，主管根據可追溯的評分結果決定是否能獨立處理某類工單。

1. **企業建置**：填寫公司資料、通路、客服職責、退換貨與運費等規則；上傳已核准的 SOP、FAQ、話術與去識別化案例。
2. **內容審核**：每條規則標記負責人、版本、生效日、適用通路與例外；衝突或缺漏的內容退回給負責人確認。
3. **學習路徑**：依角色分配「訂單查詢 → 物流異常 → 取消訂單 → 退換貨與退款 → 客訴與升級」。
4. **練習與測驗**：先做短題辨識規則，再做模擬對話；AI 扮演顧客，依核准 SOP 提示與評分。
5. **上線判定**：主管查看錯誤類型和對話紀錄，決定可處理的案件範圍；高風險動作仍依企業授權執行。
6. **持續更新**：政策異動時，找出受影響的教材與題目，重新審核並通知相關學員複習。

## 可參考的產品做法

| 做法 | 公開資料顯示的能力 | 對本系統的啟示 |
|---|---|---|
| Intercom Knowledge | 管理公開文章、內部文章、PDF、網站與其他知識來源，並控制 AI 可使用的內容 | 訓練答案須連到有版本的來源，區分公開答覆與內部操作指示 |
| Zendesk QA | 用評分表檢查 AI 對話、人工複核，分析升級給真人的情況 | 情境演練要保存評分依據，並讓主管覆核 AI 分數 |
| Amazon Connect 評估 | 依評估表檢查互動，提供教練回饋與團隊趨勢 | 將「學習完成」和「實際處理品質」接起來，持續補強弱項 |
| 學習研究 | 提取練習、間隔複習有助知識保持；情境與回饋方式會影響效果 | 用短測驗與錯題複習取代一次看完文件，但實際間隔與成效須在公司內驗證 |

以上產品能力與研究效果分別來自廠商文件和教育研究，不能直接推論本系統會縮短多少上手時間。

## 最小可行版本（MVP）

- **管理端**：公司與職務設定、SOP 匯入、規則審核、版本管理、題庫審核。
- **學員端**：按主題閱讀、選擇題與簡答題、情境對話、錯題回看、進度頁。
- **AI 能力**：從已核准資料檢索引用、產生待審題目、扮演顧客、按明確規準提出評分建議。遇到資料不足時指出缺口並要求查證。
- **報表**：主題正確率、關鍵失誤、重測結果、主管覆核結果、獨立接案時間。基準與目標由企業自行設定。

## 每家公司要填的資料

| 類別 | 最低必要欄位 | 常見待確認點 |
|---|---|---|
| 基本設定 | 品牌、商品類型、服務通路、服務時間、語氣 | 各通路是否有不同政策 |
| 訂單 | 查詢系統、身分核對方式、可變更狀態 | 已出貨後能否改地址或取消 |
| 物流 | 承運商、查詢方式、異常判定、升級窗口 | 多久未更新需聯絡物流 |
| 退換貨 | 申請期限、排除商品、商品狀態、運費 | 瑕疵品和一般退貨是否不同 |
| 退款 | 退款方式、授權人、確認節點、預估處理時間 | 跨平台付款與部分退款 |
| 客訴 | 補償權限、敏感案件、主管升級規則 | 哪些情況不得自行承諾 |
| 資安 | 個資遮蔽、可查看資料、資料保留 | 如何核對身分與處理可疑請求 |

填寫格式見 [公司客製化_SOP模板.md](公司客製化_SOP模板.md)。

## 建議的資料結構

每個 SOP 條目至少保存：`company_id`、`sop_id`、主題、適用通路、觸發條件、操作步驟、例外、升級條件、禁止行為、核准人、版本、生效日、來源連結。每道題至少保存：`question_id`、對應 `sop_id` 與版本、情境、題型、參考答案、評分規準、風險等級、審核狀態。公司之間的教材、對話與成績需要依 `company_id` 隔離。

## 驗收方式

1. 給新進客服一批匿名、已知正解的案例，檢查能否找到正確政策、正確判斷下一步，且不捏造期限或退款承諾。
2. 用政策缺漏與互相衝突的案例，檢查系統是否明確標示「需查證／升級」。
3. 由兩位主管評同一組情境，校準評分規準；再比較 AI 建議與主管判定。
4. 比較訓練前後的情境處理品質、主管介入率及達到獨立接案標準所需時間。這些是建議指標，並非已驗證的效益數字。

## 公開資料

- [Intercom：AI 與客服知識來源](https://www.intercom.com/help/en/articles/9440354-knowledge-sources-to-power-ai-agents-and-self-serve-support)
- [Zendesk：以 QA 評估 AI 客服對話](https://support.zendesk.com/hc/en-us/articles/7418648293018-Evaluating-the-performance-of-AI-agents-using-Zendesk-QA)
- [Amazon Connect：互動評估與教練回饋](https://docs.aws.amazon.com/us_us/connect/latest/adminguide/evaluations.html)
- [Nature Reviews Psychology：間隔學習與提取練習](https://www.nature.com/articles/s44159-022-00089-1)
- [Shopify：退貨規則與政策設定](https://help.shopify.com/en/manual/orders/self-serve-returns/return-rules)
- [Shopify：訂單物流追蹤](https://help.shopify.com/en/manual/fulfillment/setup/order-status-page/order-tracking)
- [Shopify：取消訂單](https://help.shopify.com/en/manual/fulfillment/managing-orders/canceling-orders)
- [Shopify：退款訂單](https://help.shopify.com/en/manual/orders/refund-cancel-order)
- [Shopify：退貨與換貨處理](https://help.shopify.com/en/manual/orders/refunds-returns/exchanges)
- [Shopify：商店權限](https://help.shopify.com/en/manual/your-account/users/roles/permissions/store-permissions)
