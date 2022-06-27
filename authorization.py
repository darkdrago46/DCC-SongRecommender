import tekore as tk
def authorize():
    CLIENT_ID = "150ea559aaa74f0f80373d00bf165aac"
    CLIENT_SECRET = "08f8055e7b5e4411b98d39b4cf05c213"
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)