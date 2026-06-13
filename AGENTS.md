# Repository Guidelines

## Project Structure & Module Organization

This repository is a Jekyll/GitHub Pages academic homepage. Core site configuration lives in `_config.yml`, primary page content is in `_pages/about.md`, and navigation data is in `_data/navigation.yml`. Layout templates are in `_layouts/`, reusable fragments are in `_includes/`, Sass source is in `_sass/`, and compiled entry styles/scripts live under `assets/`. Static images and favicons are stored in `images/`. The generated site output is `_site/` and should not be edited by hand. The Google Scholar citation updater is isolated in `google_scholar_crawler/`, with its GitHub Actions workflow in `.github/workflows/google_scholar_crawler.yaml`.

## Build, Test, and Development Commands

- `bundle install`: install Ruby dependencies from `Gemfile`.
- `bash run_server.sh`: start the local Jekyll live server via `bundle exec jekyll liveserve`.
- `bundle exec jekyll build`: build the static site into `_site/` for validation.
- `cd google_scholar_crawler && pip3 install -r requirements.txt && python3 main.py`: run the citation crawler locally. Set `GOOGLE_SCHOLAR_ID` first.

## Coding Style & Naming Conventions

Use two-space indentation for YAML, Markdown front matter, HTML templates, and Sass to match the existing Jekyll style. Keep Liquid includes small and reusable, and prefer editing `_includes/` or `_layouts/` over duplicating markup in page files. Name new pages with lowercase, descriptive filenames such as `_pages/projects.md`. Keep CSS changes in `_sass/` partials unless a standalone asset is already present in `assets/css/`.

## Testing Guidelines

There is no formal automated test suite in this repository. Before submitting changes, run `bundle exec jekyll build` and inspect the site locally at `http://127.0.0.1:4000` after `bash run_server.sh`. For visual changes, verify desktop and mobile widths. For crawler changes, run `python3 main.py` with a test Scholar ID and confirm JSON output under `google_scholar_crawler/results/`.

## Commit & Pull Request Guidelines

Recent commits use short imperative or descriptive messages, sometimes with prefixes such as `style:` or `Fix:`. Prefer messages like `Add awards section` or `Fix sidebar centering`. Pull requests should describe the visible change, list validation commands run, link any related issue, and include screenshots for UI, layout, or styling changes. Note any configuration or secret requirements, especially changes involving `GOOGLE_SCHOLAR_ID` or GitHub Actions.

## Security & Configuration Tips

Do not commit secrets, analytics credentials beyond public IDs, or generated crawler credentials. Keep `GOOGLE_SCHOLAR_ID` in GitHub Actions secrets as documented in `README.md`. Treat `_config.yml` as the main source of site identity, SEO, analytics, and author profile settings.
