from settings import SITE_CONFIGS


def get_site_config(url: str):
    for domain, config in SITE_CONFIGS.items():
        if domain in url:
            return config
    return None


def is_url_supported(url: str) -> bool:
    return any(domain in url for domain in list(SITE_CONFIGS.keys()))