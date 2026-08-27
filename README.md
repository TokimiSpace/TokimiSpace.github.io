<div align="center">

# Tokimi Open Source

**四個 Tokimi 開源方向的雙語入口：公開內容、驗證證據與誠實邊界集中在一頁。**

[繁體中文](README.md) · [English](README.en.md)

[開源首頁・中文](https://tokimispace.github.io/?lang=zh-TW) ·
[Open-source hub・English](https://tokimispace.github.io/?lang=en) ·
[Tokimi 官網開源導覽](https://tokimi.space/open-source/) ·
[GitHub Organization](https://github.com/TokimiSpace)

</div>

> [!WARNING]
> **防詐提醒 / Fraud alert**
>
> 任何以 `@gmail.com` 結尾、並自稱代表 Tokimi／時見數位科技的帳號，都不是 Tokimi 官方聯絡管道；請勿付款或提供驗證碼。
>
> Any `@gmail.com` address claiming to represent Tokimi is not an official Tokimi contact channel; do not pay or share verification codes.
>
> **請只透過 / Verify only through：** [tokimi.space](https://tokimi.space/) · [ben@tokimi.space](mailto:ben@tokimi.space)

![Tokimi Open Source 社群預覽圖：訊號匯流排連結 Rover、AstroGroot、Darkforest Web 與 BridgeTime Kimi Privacy](social-card-open-source-v3.png)

這個 repository 是 [TokimiSpace GitHub Pages](https://tokimispace.github.io/?lang=zh-TW)
的 dependency-free 靜態原始碼，也是四個專案的共同入口。它同時說明「公開什麼」與
「沒有公開或不能證明什麼」，避免把本機 demo、研究索引或隱私 reference 誤認為完整正式服務。

## 四個專案的公開範圍

| 專案 | 公開內容 | 未包含／不能代表 |
| --- | --- | --- |
| 🚗 [Tokimi Rover](https://github.com/TokimiSpace/tokimi-rover) | 雙 ESP32-S3 韌體、接線文件、稽核紀錄、Supercar V3 Blender 車殼 CAD | 本次沒有重新做實車安全測試；CAD 尺寸衝突仍待 A4 實體 fit-check，不能視為已驗證裝配 |
| 🔭 [AstroGroot](https://github.com/topben/astrogroot) | MIT 授權的 Deno/Hono 應用、收集器、三語搜尋、知識圖、API 與 MCP | 不重新授權被索引的第三方內容；AI 摘要不是權威來源，需回原始資料核對 |
| 🌲 [Darkforest Web](https://github.com/TokimiSpace/darkforest-web) | 瀏覽器前端、12 組本機 fixtures、6 語介面與 QA 工具 | pre-alpha、loopback-only demo；不含正式配對、私人 game core、官方 service contract 或 LiveOps |
| 🛡️ [BridgeTime Kimi Privacy](https://github.com/TokimiSpace/bridgetime-kimi-privacy) | v0.2.0 Private Intent 五欄位白名單、固定 Kimi 出站邊界、離線 wire capture tests，並保留別名化比較模式 | 不含完整 BridgeTime 服務或部署證明；Kimi 仍會看到抽象操作與帳號／網路 metadata，別名化模式仍有重識別風險 |

相關正式服務：[AstroGroot](https://astrogroot.org/?lang=zh-TW) ·
[Darkforest](https://darkforest.tw/) · [BridgeTime](https://bridgetime.org/)。正式服務與上述開源範圍不等同。

## 60 秒本機預覽

網站只有 HTML、CSS 與 JavaScript，不需建置：

```bash
git clone https://github.com/TokimiSpace/TokimiSpace.github.io.git
cd TokimiSpace.github.io
python3 -m http.server 8000
```

- 中文：<http://localhost:8000/?lang=zh-TW>
- English：<http://localhost:8000/?lang=en>

發布前可執行：

```bash
python3 scripts/check_site.py
node --check main.js
```

## 語言 URL

- 正式中文：<https://tokimispace.github.io/?lang=zh-TW>
- Production English：<https://tokimispace.github.io/?lang=en>

兩種語言都直接寫在同一個靜態頁面，不使用自動翻譯。有效的 `lang` URL 參數優先於本機記住的
選擇，因此連結可以分享與加入書籤。

## 授權、品牌與分享

本 repository 依路徑採 **Apache-2.0** 與 **CC BY 4.0**，詳見
[LICENSES.md](LICENSES.md)。各連結專案維持自己的 license map；本入口不重新授權 AstroGroot
索引的第三方內容。

Tokimi、時見數位科技與官方專案識別不隨原始碼授權，詳見
[TRADEMARKS.md](TRADEMARKS.md)。fork 可以忠實標示來源，但不得暗示官方認證、贊助或合作關係。

網站不載入 analytics 或 tracker。LINE、Facebook 與 Twitter/X 分享使用 repository 內的
[1200 × 630 PNG](social-card-open-source-v3.png)。
