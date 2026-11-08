"""Local CLI. Pure analysis offline. Explicit command names independent of Click version."""

import json
import sys
from pathlib import Path

import click

from .graph import analyze, build_graph
from .models import Assumption, Claim, Observation, Relationship, Source


@click.group()
def cli():
    pass


@cli.command(name="analyze")
@click.argument("input_path", type=click.Path(exists=True))
def analyze_cmd(input_path):
    """Analyze a JSON record set and emit support profile."""
    data = json.loads(Path(input_path).read_text())
    claims = [Claim(**c) for c in data.get("claims", [])]
    observations = [Observation(**o) for o in data.get("observations", [])]
    sources = [Source(**s) for s in data.get("sources", [])]
    relationships = [Relationship(**r) for r in data.get("relationships", [])]
    assumptions = [Assumption(**a) for a in data.get("assumptions", [])]

    g = build_graph(claims, observations, sources, relationships)
    if not claims:
        click.echo("No claims", err=True)
        sys.exit(1)
    profile = analyze(g, claims[0].id, assumptions)
    click.echo(profile.model_dump_json(indent=2))


@cli.command(name="verify-bundle")
@click.argument("bundle_path", type=click.Path(exists=True))
def verify_bundle_cmd(bundle_path):
    """Verify a reconciliation bundle. Non-zero exit on verification failure."""
    from .bundle import verify_bundle
    result = verify_bundle(Path(bundle_path))
    click.echo(json.dumps(result, indent=2, default=str))
    if result.get("exit_code_recommended", 0) != 0 or result.get("envelope_commitment_consistent") is False:
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
