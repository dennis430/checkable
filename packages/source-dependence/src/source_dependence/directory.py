"""Read plain-text files without inferring claims, shared origins or derivation edges."""

from pathlib import Path

from .models import Claim, Observation, ObservationType, Source


NON_TEXT_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".zip",
}


def directory_record(directory: Path, claim: str) -> dict:
    """One source and observation per UTF-8 file, including nested files. No deduplication."""
    if not claim.strip():
        raise ValueError("claim is empty")
    if not directory.is_dir():
        raise ValueError("input must be a directory of plain-text files")
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symbolic links are not read: {path.relative_to(directory)}")
        if path.is_file():
            files.append(path)
    if not files:
        raise ValueError("directory contains no text files")

    sources, observations = [], []
    for index, path in enumerate(files, 1):
        name = path.relative_to(directory).as_posix()
        if path.suffix.lower() in NON_TEXT_SUFFIXES:
            raise ValueError(f"not a supported plain-text file: {name}; export text first")
        data = path.read_bytes()
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"file is not UTF-8 text: {name}") from error
        if "\x00" in content:
            raise ValueError(f"file contains NUL bytes, not plain text: {name}")
        source = Source(id=f"s{index}", name=name, origin_group=None)
        sources.append(source.model_dump(mode="json"))
        observations.append(Observation(
            id=f"o{index}", claim_id="c1", type=ObservationType.REPORTED,
            content=content, source_id=source.id, uncertainty={"lineage": "unknown"},
            coverage="Original UTF-8 file content. Relevance to the supplied claim was not interpreted.",
        ).model_dump(mode="json"))
    return {
        "claims": [Claim(id="c1", text=claim).model_dump(mode="json")],
        "sources": sources, "observations": observations,
        "relationships": [], "assumptions": [],
    }
