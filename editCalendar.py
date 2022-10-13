import googleapiclient.discovery
import google.auth

"""
事前にGCP(Google Cloud Platform)にてGoogle Calendar APIの有効化、
上記APIを用いてカレンダーを編集するアカウント作成、
カレンダー上で共有アカウントとして上記アカウントの追加を事前に行っている。
"""

def add_schedule(events):
    # 編集スコープ設定(Read,Writeを設定)
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # カレンダーIDの設定(自身のgmailのアドレスにて書き換え)
    calendar_id = 'XXXXX@gmail.com'

    # 認証ファイルを使用して認証用オブジェクトを作成
    # 同階層にGCPで作成したアカウントの鍵情報を作成、json形式でDLして「credentials.json」にリネームして配置
    gapi_creds = google.auth.load_credentials_from_file('credentials.json', SCOPES)[0]

    # 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
    for event in events:
        # 予定を追加する
        event = service.events().insert(calendarId = calendar_id, body = event).execute()