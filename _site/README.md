# McGill Centre for the Study of Democratic Citizenship Web Dev



This is the source code of the [McGill Centre for the Study of Democratic Citizenship Website](), as forked by the [Complex Data Lab Website](https://complexdatalab.com/) (originally forked from [McGill-NLP](https://github.com/McGill-NLP/mcgill-nlp.github.io)). It is built using [Jekyll](https://github.com/jekyll/jekyll) and [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes).

## Contribution Guide

<!-- 
RUN LOCAL
eval "$(rbenv init - zsh)" && bundle _2.4.22_ exec jekyll serve --livereload
-->
| Action | How-to | 
| -- | -- | 
| Add or update a member profile or publications | [Open a Github Issue](https://github.com/ekmpa/csdc-mcgill/issues/new/choose) | 
| Calendar sync setup | [Calendar documentation](./documentation/calendar.md) |
| Mistake made in the form | Refer to the [FAQ](#faq) below | 
| Technical issue | [Contact Developer](mailto:emma.kondrup@mila.quebec) |

## Further contributions

For other types of contribution (not covered by the issue form), please follow these steps:

1. [Fork](https://github.com/ekmpa/csdc-mcgill/fork) the repository.
2. Add your contribution by editing the desired files.
3. Create a pull request: Click on the [Pull Request](https://github.com/ekmpa/csdc-mcgill/pulls) tab and select "New pull request". Select the repository you forked and modified.
4. Wait for a team member to review and merge your pull request.

| Direct code modification | How-to | 
| -- | -- | 
| Adding members / contributors | [here](./documentation/members.md) |
| Utility (e.g. image-resizing) | [here](./documentation/utility.md) | 
| Creating pages under _post (paper publications, blogs, teaching) | [here](./documentation/creating-posts.md) |
| Modifying pages / dependicies / Local setup | [here](./documentation/advanced_mode.md) | 

## Topic Tags For Research Axes

The research cards under Research/Publications can display lightweight topic tags generated from publication metadata.

Run:

```bash
python -m src.python.generate_research_axis_topics
```

This command scans markdown files in `_posts/papers` and updates `_data/research_axis_topics.yml`, which is consumed by the shared include used in both English and French pages.

By default, it produces 2-3 word topic phrases, with 3-4 tags per axis.

Matching is robust and bilingual-aware:

- Publication text is normalized with accent folding (e.g. `citoyenneté` -> `citoyennete`) and token mapping to shared concepts.
- A publication can contribute to multiple axes (weighted relevance), instead of being forced into a single axis.
- Final tags are selected from axis-specific phrase banks with explicit EN/FR labels.
- The generated YAML includes a `matching` section with thresholds, axis document counts, and sample assignments for auditing.

To tune output density:

```bash
python -m src.python.generate_research_axis_topics --max_tags 6
```

You can also set a minimum:

```bash
python -m src.python.generate_research_axis_topics --min_tags 3 --max_tags 4
```

Language toggling on the site:

- The shared include reads `tags_en` or `tags_fr` based on the current page language.
- French variants like `fr` and `fr-*` are handled as French.

## FAQ

> I created a post but it doesn't show up. What's wrong?

Make sure it is in the right directory, and that the file name is correct. The file name should be `<YYYY>-<MM>-<DD>-<shorthand>.md`; this is not a convention or a preference, it is actually **needed** to render that file.

> I made a mistake when filling the form. How can I fix it?

After you fill the form, an issue is created with an appropriate *tag*. Then, a pull request (which is a "proposal" to make a change) is automatically created from that *tag*, based on the content of the issue. But if you made a mistake, then that PR is incorrect. So you should try to close it, or request the PR to be closed in a reply. Then, all you need to do is to modify the issue's content (makes sure the formatting stays the same, that's very important!). Once it's updated, you can remove the *tag*, refresh the page, then add back the same *tag*. This will create a new pull request, and a maintainer will review it.

> When filling out the form, how do I upload my profile picture or a thumbnail without having to use an external source, like imgur?

1. Open a [new blank issue](https://github.com/McGill-NLP/mcgill-nlp.github.io/issues/new).
2. Click on "Attach files by dragging & dropping, selecting, or pasting them".
3. Upload your picture.
4. Copy only the URL link (i.e. `https://user-images.githubusercontent.com/...png` only). Ignore the rest (i.e. `![text]()`).
5. Keep the link, but cancel the new issue. Paste that link in the form.

> Does OpenAlex require an API key?

OpenAlex works with an API key. Please set the environment variable `OPENALEX_API_KEY` to your API key and it will be automatically used. For GitHub Actions, look at `.github/workflows/auto-update-publications.yml` to see how the environment variable is assigned.
