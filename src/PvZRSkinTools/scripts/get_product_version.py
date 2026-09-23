from importlib.metadata import version

from packaging.version import Version


def get_product_version(package: str) -> str:
    v = Version(version(package))

    major = v.major
    minor = v.minor
    patch = v.micro
    build = v.dev if v.dev is not None else 0

    return f"{major}.{minor}.{patch}.{build}"


if __name__ == "__main__":
    print(get_product_version("pvzrskintools"))
