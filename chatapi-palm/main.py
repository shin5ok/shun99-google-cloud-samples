from typing import Any, Mapping
from verify_token import verify_id_token
from chat import Chat
import os
import flask
import functions_framework

e = os.environ
SKIP_VERIFICATION = e.get("SKIP_VERIFICATION")
PROJECT_ID = e.get("GOOGLE_CLOUD_PROJECT")
PROJECT_NUMBER = e.get("PROJECT_NUMBER")
MODEL_LOCATION = e.get("MODEL_LOCATION", "us-central1")

chat = Chat(PROJECT_ID, MODEL_LOCATION)

@functions_framework.http

def hello_chat(req: flask.Request) -> Mapping[str, Any]:
  
  if SKIP_VERIFICATION != "True":
    # ヘッダーよりAuthorizationを取得
    auth_header = flask.request.headers.get('Authorization')

    # Bear tokenの取得
    if auth_header:
        bearer_token = auth_header.split(' ')[1]  # Authorization: Bearer <token>
    else:
        print('Invalid header')
        flask.abort(401)

    # tokenの検証
    if not verify_id_token(PROJECT_NUMBER, bearer_token):
      flask.abort(403)
  
  request_json = req.get_json(silent=True)
  if request_json:
    text = (request_json["message"]["text"])
  else:
    text = "Hi!"

  # PaLM API実行
  res = chat.chat(text)

  # 応答をChat形式に変更
  chat_response = {
    "text": res
  }

  return flask.jsonify(chat_response)
  
