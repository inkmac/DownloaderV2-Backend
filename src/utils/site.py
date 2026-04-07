from settings import SITE_CONFIGS


def get_site_config(url: str):
    for domain, config in SITE_CONFIGS.items():
        if domain in url:
            return config
    return None