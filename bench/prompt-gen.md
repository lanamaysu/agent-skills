先讀 ./skills/taiwan-traditional-chinese/SKILL.md，照它的規則完成下面三項任務。

輸出格式：每題以 `## G1`／`## G2`／`## G3` 起始，接該題的內容，題與題之間空一行。
不要輸出任何說明、前言或結語。

---

## G1

依下面這段 diff 寫一則 commit message（中文）。

```diff
--- a/components/BookingForm/useSeatLock.js
+++ b/components/BookingForm/useSeatLock.js
@@ -18,9 +18,14 @@ export function useSeatLock(scheduleId) {
   useEffect(() => {
     if (!scheduleId) return
-    const timer = setInterval(() => {
+    let cancelled = false
+    const timer = setInterval(() => {
+      if (cancelled) return
       renewLock(scheduleId)
     }, 30_000)
-    return () => clearInterval(timer)
+    return () => {
+      cancelled = true
+      clearInterval(timer)
+      releaseLock(scheduleId)
+    }
   }, [scheduleId])
```

## G2

依下面這段 diff 寫一則 PR 描述（繁體中文），長度以審查者看得懂、能自己驗證為準。

```diff
--- a/lib/api/client.js
+++ b/lib/api/client.js
@@ -5,10 +5,26 @@ const TIMEOUT = 8000
+const RETRYABLE = new Set([502, 503, 504])
+
 export async function request(path, options = {}) {
-  const res = await fetch(BASE + path, { ...options, signal: timeoutSignal(TIMEOUT) })
-  if (!res.ok) throw new ApiError(res.status, await res.text())
-  return res.json()
+  for (let attempt = 0; attempt <= 2; attempt++) {
+    const res = await fetch(BASE + path, { ...options, signal: timeoutSignal(TIMEOUT) })
+    if (res.ok) return res.json()
+    if (!RETRYABLE.has(res.status) || attempt === 2) {
+      throw new ApiError(res.status, await res.text())
+    }
+    await sleep(200 * 2 ** attempt)
+  }
 }
```

## G3

替下面這個設定選項寫一段說明文件（繁體中文，兩到四句），對象是同團隊的前端工程師。

```js
// next.config.js
experimental: {
  // 開啟後，同一份查詢在同一次 render 內只會送出一次請求，
  // 結果存在 request 層級的暫存區，render 結束就丟掉。
  dedupeRequestsPerRender: true,
}
```
