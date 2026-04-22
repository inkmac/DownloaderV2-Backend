from src.core.config import AppConfig


def get_site_config(url: str):
    site_configs = AppConfig.get_site_configs()

    for domain, config in site_configs.items():
        if domain in url:
            return config
    return None


def is_url_supported(url: str) -> bool:
    site_configs = AppConfig.get_site_configs()
    return any(domain in url for domain in list(site_configs.keys()))