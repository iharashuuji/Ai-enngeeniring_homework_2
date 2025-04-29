from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import urllib.request

app = FastAPI()

EXTERNAL_API_URL = "https://6ef9-34-16-195-216.ngrok-free.app/generate"

@app.post("/generate")
async def chat(request: Request):
    try:
        body = await request.json()
        message = body.get("message", "")
        
        # 外部APIに送信するペイロード
        payload = {
            "message": message
        }
        
        # 外部APIの呼び出しに必要なヘッダーとペイロード設定
        req = urllib.request.Request(
            EXTERNAL_API_URL,
            data=json.dumps(payload).encode(),  # ペイロードをJSONとしてエンコード
            headers={"Content-Type": "application/json"},  # ヘッダーを設定
            method="POST"  # POSTメソッドを指定
        )
        
        # 外部APIのレスポンスを取得
        with urllib.request.urlopen(req) as res:
            response_body = res.read()  # レスポンスを読み取る
            response_json = json.loads(response_body)  # JSONに変換

        # レスポンスをJSON形式で返す
        return JSONResponse(content={
            "success": True,
            "response": response_json.get("response", "No response")  # "response"キーがなければ"No response"を返す
        })

    except Exception as e:
        # エラーが発生した場合は500エラーを返す
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)  # エラーメッセージを返す
        })
