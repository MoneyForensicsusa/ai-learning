import os


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is missing."
        )

    return value


def get_settings():
    return {
        "endpoint": get_required_env("AZURE_OPENAI_ENDPOINT"),
        "api_key": get_required_env("AZURE_OPENAI_API_KEY"),
        "deployment": get_required_env("MODEL_DEPLOYMENT"),
    }