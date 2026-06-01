from pathlib import Path

from UnityPy.classes import Object, PPtr

import unitypy_utils

import asset_classifier
import spine_converter


def asset_filter(path: str) -> bool:
    return (
        path.endswith((".png", ".atlas.txt", ".skel.bytes")) and "Caltrop" not in path
    )


def get_asset_file_name(path: Path) -> str:
    file_name = path.name if path.suffix == ".png" else path.stem
    return file_name.replace(".fla", "").replace("Kernel-pult", "Kernelpult")


def process_asset(output_directory: Path, file_name: str, obj: PPtr[Object]) -> None:
    dir_name = Path(file_name).stem
    classification = asset_classifier.get_asset_classification(dir_name)
    asset_dir = output_directory / classification / dir_name
    asset_dir.mkdir(parents=True, exist_ok=True)
    output_path = asset_dir / file_name

    if unitypy_utils.is_texture2d(obj):
        texture = obj.deref_parse_as_object()
        texture.image.save(output_path)
    elif unitypy_utils.is_text_asset(obj):
        text_asset = obj.deref_parse_as_object()
        v3_dir = output_path.parent / "v3"
        if file_name.endswith(".skel"):
            unitypy_utils.write_binary_text_asset(text_asset, output_path)

            spine_converter.convert_skeleton(
                output_path, output_path.with_suffix(".json")
            )

            v3_json = v3_dir / f"{output_path.stem}.json"
            v3_skel = v3_dir / f"{output_path.stem}.skel"
            spine_converter.convert_skeleton(output_path, v3_json, "3.8.0")
            spine_converter.convert_skeleton(v3_json, v3_skel)
        elif file_name.endswith(".atlas"):
            unitypy_utils.write_text_asset(text_asset, output_path)

            spine_converter.convert_atlas(
                output_path,
                v3_dir / output_path.name,
                spine_converter.AtlasVersion.V3,
            )
