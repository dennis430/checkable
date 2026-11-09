import json

import pytest
from click.testing import CliRunner

from source_dependence.cli import cli
from source_dependence.directory import directory_record
from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source


def test_identical_and_similar_files_keep_separate_sources_with_unknown_lineage(tmp_path):
    (tmp_path / "a.txt").write_text("The lantern is lit.", encoding="utf-8")
    (tmp_path / "b.md").write_text("The lantern is lit.", encoding="utf-8")
    (tmp_path / "c.log").write_text("A lantern appears to be lit.", encoding="utf-8")
    result = CliRunner().invoke(cli, ["from-directory", str(tmp_path), "--claim", "The lantern is lit."])
    assert result.exit_code == 0, result.output
    record = json.loads(result.output)
    assert len(record["observations"]) == len(record["sources"]) == 3
    assert [source["name"] for source in record["sources"]] == ["a.txt", "b.md", "c.log"]
    assert len({source["id"] for source in record["sources"]}) == 3
    assert all(source["origin_group"] is None for source in record["sources"])
    assert all(item["uncertainty"] == {"lineage": "unknown"} for item in record["observations"])
    assert record["relationships"] == []
    assert record["observations"][0]["content"] == record["observations"][1]["content"]
    graph = build_graph(
        [Claim(**item) for item in record["claims"]],
        [Observation(**item) for item in record["observations"]],
        [Source(**item) for item in record["sources"]],
        [Relationship(**item) for item in record["relationships"]],
    )
    profile = analyze(graph, "c1")
    assert profile.observations_counted == 3
    assert profile.documented_origin_groups == []
    assert profile.sensitivity["distinct_documented_origin_group_count"] == 0
    assert profile.sensitivity["shared_origin_collapses_naive_count"] is False
    assert len(profile.unknowns) >= 3


def test_nested_source_files_preserve_unicode_newlines_and_empty_content(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "note.py").write_bytes("# café\r\n".encode("utf-8"))
    (tmp_path / "empty.txt").write_bytes(b"")
    record = directory_record(tmp_path, "User-supplied claim")
    assert [source["name"] for source in record["sources"]] == ["empty.txt", "nested/note.py"]
    assert [item["content"] for item in record["observations"]] == ["", "# café\r\n"]
    assert directory_record(tmp_path, "User-supplied claim") == record


@pytest.mark.parametrize("name,data", [
    ("scan.pdf", b"%PDF-1.7\nplain-looking PDF syntax"),
    ("document.docx", b"plain-looking bytes"),
    ("book.xlsx", b"plain-looking bytes"),
    ("image.png", b"plain-looking bytes"),
    ("image.jpg", b"plain-looking bytes"),
    ("invalid.txt", b"\xff\xfe"),
    ("binary.txt", b"a\x00b"),
])
def test_unreadable_or_nontext_files_fail_without_a_partial_record(tmp_path, name, data):
    (tmp_path / "a.txt").write_text("Readable text", encoding="utf-8")
    (tmp_path / name).write_bytes(data)
    result = CliRunner().invoke(cli, ["from-directory", str(tmp_path), "--claim", "A claim"])
    assert result.exit_code != 0
    assert result.stdout == ""


def test_empty_directory_blank_claim_and_symbolic_links_are_refused(tmp_path):
    with pytest.raises(ValueError, match="no text files"):
        directory_record(tmp_path, "A claim")
    with pytest.raises(ValueError, match="claim is empty"):
        directory_record(tmp_path, " ")
    (tmp_path / "link.txt").symlink_to(tmp_path / "missing.txt")
    with pytest.raises(ValueError, match="symbolic links"):
        directory_record(tmp_path, "A claim")


def test_symbolic_link_input_directory_is_refused_without_reading_target(tmp_path):
    target = tmp_path / "private-notes"
    target.mkdir()
    (target / "note.txt").write_text("Should not be admitted via a link", encoding="utf-8")
    linked = tmp_path / "linked-notes"
    linked.symlink_to(target, target_is_directory=True)

    result = CliRunner().invoke(cli, ["from-directory", str(linked), "--claim", "A claim"])
    assert result.exit_code != 0
    assert result.stdout == ""
    assert "symbolic links" in result.stderr
