import importlib.metadata


def app_version() -> str:
    try:
        return importlib.metadata.version("ourcrm")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"
