from core.config import settings

github_auth_url = (
    f"https://github.com/login/oauth/authorize"
    f"?client_id={settings.oauth.client_id}"
    f"&redirect_uri={settings.oauth.redirect_uri}"
    f"&scope=user:email"
)