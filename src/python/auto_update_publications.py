import datetime
from pathlib import Path

from ruamel.yaml import YAML

from . import add_publications_by_author_openalex


def main(
    save_dir="_posts/papers",
    site_data_dir="_data/",
    use_ignore_list=True,
    year_start=None,
    year_end=None,
    all_years=False,
    doi_only=False,
):
    site_data_dir = Path(site_data_dir)
    current_year = datetime.datetime.now().year

    if all_years:
        year_start = 1900
        year_end = current_year
    else:
        if year_start is None:
            year_start = current_year
        if year_end is None:
            year_end = year_start

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.allow_duplicate_keys = True
    with open(site_data_dir / "authors.yml") as f:
        authors = yaml.load(f) or {}

    for author in authors.values():
        orcid = author.get("orcid", "")
        openalex_id = author.get("openalex_id", "")

        if orcid or openalex_id:
            print(
                f"Updating publications for {author['name']} via OpenAlex "
                f"({year_start}-{year_end})..."
            )
            add_publications_by_author_openalex.main(
                orcid=orcid or None,
                openalex_id=openalex_id or None,
                year_start=year_start,
                year_end=year_end,
                save_dir=save_dir,
                use_ignore_list=use_ignore_list,
                doi_only=doi_only,
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--save_dir",
        help="The directory to save the new files.",
        default="_posts/papers",
    )
    parser.add_argument(
        "--site_data_dir", help="The directory with the site data.", default="_data/"
    )
    parser.add_argument(
        "--use_ignore_list",
        help="Whether to use the ignore list.",
        default="true",
        choices=["true", "false"],
    )
    parser.add_argument(
        "--year_start",
        help="Start year for publication sync.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--year_end",
        help="End year for publication sync.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--all_years",
        help="Sync all years (1900-current year).",
        default="false",
        choices=["true", "false"],
    )
    parser.add_argument(
        "--doi_only",
        help="Only import works that have a DOI in OpenAlex.",
        default="false",
        choices=["true", "false"],
    )
    args = parser.parse_args()

    use_ignore_list = args.use_ignore_list == "true"
    all_years = args.all_years == "true"
    doi_only = args.doi_only == "true"
    if (
        args.year_start is not None
        and args.year_end is not None
        and args.year_start > args.year_end
    ):
        parser.error("--year_start cannot be greater than --year_end")

    main(
        save_dir=args.save_dir,
        site_data_dir=args.site_data_dir,
        use_ignore_list=use_ignore_list,
        year_start=args.year_start,
        year_end=args.year_end,
        all_years=all_years,
        doi_only=doi_only,
    )
