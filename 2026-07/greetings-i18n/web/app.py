from flask import Flask, request

app = Flask(__name__)
FLAG = "Alpaca{REDACTED}"

translations = {
    "hello": {
        "en": "Hello, {username}!",
        "ja": "こんにちは、{username}さん!"
    },
    "error": {
        "en": "An error has occurred: {err}",
        "ja": "エラーが発生しました: {err}",
    }
}


def parse_accept_language() -> str:
    header = request.headers.get("Accept-Language")
    if not header:
        return "en"

    first = header.split(",")[0]
    lang = first.split(";")[0].strip().split("-")[0].strip()

    return lang or "en"

# Translation function
def _(key: str):
    custom = request.form.get(f"custom-{key}")
    if custom:
        return custom
    lang = parse_accept_language()
    return translations.get(key).get(lang, key)


@app.get("/")
def index():
    try:
        username = request.args.get("username", "anonymous user")
        return _("hello").format(username=username), 200, {'Content-Type': 'text/plain;charset=utf-8'}
    except Exception as e:
        return _("error").format(err=e), 500, {'Content-Type': 'text/plain;charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
