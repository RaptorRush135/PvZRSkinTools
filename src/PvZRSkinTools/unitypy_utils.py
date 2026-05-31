from pathlib import Path
from typing import TypeGuard

from UnityPy.classes import Object, PPtr, TextAsset, Texture2D
from UnityPy.enums import ClassIDType


def is_texture2d(data: PPtr[Object]) -> TypeGuard[PPtr[Texture2D]]:
    return data.type == ClassIDType.Texture2D


def is_text_asset(data: PPtr[Object]) -> TypeGuard[PPtr[TextAsset]]:
    return data.type == ClassIDType.TextAsset


def write_text_asset(text_asset: TextAsset, output_path: Path) -> None:
    output_path.write_text(text_asset.m_Script, encoding="utf-8")


def write_binary_text_asset(text_asset: TextAsset, output_path: Path) -> None:
    bytes = text_asset.m_Script.encode("utf-8", errors="surrogateescape")
    output_path.write_bytes(bytes)
