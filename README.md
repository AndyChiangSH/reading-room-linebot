# reading-room-linebot

> 自習室數人數LINE bot

## 使用教學

1. 掃描底下QR Code加入好友：

![](https://i.imgur.com/OZgIFqM.png)

2. 「使用說明」：顯示機器人使用說明。
3. 「現在人數」：機器人回傳現在自習室的人數。
4. 「啟動機器人」：啟動後，機器人將每一小時回傳自習室的人數，直到關閉機器人。
5. 「關閉機器人」：關閉後，機器人將不會再回傳自習室的人數，直到下次啟動。
6. 因為本服務架在免費平台上，運行時間是有限制的，所以希望大家上班時啟動，下班時關閉。

## 部署

1. 點擊底下**Heroku一鍵部署按鈕**。

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AndyChiangSH/reading-room-linebot)

2. 輸入APP名稱，不能和我的APP名稱(reading-room-linebot)重複!

![](https://i.imgur.com/uifrcs8.png)

3. 再來需要填入一些配置變數，**CHANNEL_ACCESS_TOKEN**和**CHANNEL_SECRET**要到LINE Developers取得。

![](https://i.imgur.com/hZVY3Hr.png)


4. 前往[LINE Developers](https://developers.line.biz/zh-hant/)，登入你的LINE帳號。
5. 登入後，新增一個channel，選擇「Messaging API」。

![](https://i.imgur.com/sgufFEq.png)

6. 填入LINE bot基本資料，機器人名稱、簡介、分類為必填，其餘可填可不填，填完後按「Create」。

![](https://i.imgur.com/xgfkk1a.png)

7. 找到**Basic settings>>Channel secret**，複製內容到**CHANNEL_SECRET**欄位。

![](https://i.imgur.com/NyHudjA.png)

8. 找到**Messaging API>>Channel access token**，點擊「Issue」產生新的token，複製內容到**CHANNEL_ACCESS_TOKEN**欄位。

![](https://i.imgur.com/gYzfYAg.png)

9. **TIMEZONE**為UTC的時差(預設為台灣時間+8)。
10. **TOTAL_SEAT**為自習室總座位數量(預設為160)。
11. 確認所有欄位都已經填寫後，按「Deploy APP」。

![](https://i.imgur.com/ENh0F8o.png)

12. 執行完應該會長這樣。

![](https://i.imgur.com/Fy1MUiG.png)

13. 按「View」應該會顯示 **Server OK!**。
14. 回到LINE Developers，找到**Messaging API>>Webhook URL**，填入剛才 **Server OK!** 頁面的網址，在網址後方接上**callback**，如下圖：

![](https://i.imgur.com/q97CBOB.png)

15. 接著點擊「Verify」，出現Success即成功，成功後將「Use webhook」開啟。
16. 點擊**Basic settings>>Basic information**，底下的這個連結，前往官方帳號管理後台。

![](https://i.imgur.com/LRznVDu.png)

17. **回應設定>>自動回應訊息**設為**停用**。

![](https://i.imgur.com/TW9LcUp.png)

18. 在**主頁>>聊天室相關>>圖文選單**，點擊「建立」。

![](https://i.imgur.com/jKoSq43.png)

19. 設定自行決定，版型選擇**上一個大的下三個小的**配置，圖片可參考我做的：

![](https://i.imgur.com/WstIjyR.jpg)

20. 動作設定請如下：

![](https://i.imgur.com/T1iP2ps.png)

21. 回到LINE Developers，掃描**Messaging API>>QR code**，即可加入機器人好友。
22. 測試看看點擊選單，機器人會不會回應正確的訊息!
23. 最後，需要一個**觸發器**，在每天整點時可以觸發機器人推送訊息。我用[cron-job](https://console.cron-job.org/)這個工具，點擊「CREATE CRONJOB」新增觸發器。
24. 為了節省運行時間，可以分成平日和假日兩個不同的觸發器。
25. **平日觸發器**的設定(8:00~22:00)：`0 8-22 * * 1-5`
26. **假日觸發器**的設定(9:00~17:00)：`0 9-17 * * 0,6`
27. 測試看看啟動和關閉機器人後整點會不會收到通知。
28. 完成!


## 作者

江尚軒([@AndyChiangSH](https://github.com/AndyChiangSH))
