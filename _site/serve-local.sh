#!/usr/bin/env bash
set -euo pipefail

if ! command -v rbenv >/dev/null 2>&1; then
  echo "rbenv is required to run this site locally." >&2
  echo "Install rbenv, then run: eval \"\$(rbenv init - zsh)\"" >&2
  exit 1
fi

eval "$(rbenv init - bash)"

if [[ "$(ruby -e 'print RUBY_VERSION')" != "3.3.11" ]]; then
  echo "Expected Ruby 3.3.11 via rbenv, got $(ruby -e 'print RUBY_VERSION')." >&2
  echo "Install/select it with: rbenv install 3.3.11 && rbenv local 3.3.11" >&2
  exit 1
fi

bundle check >/dev/null 2>&1 || bundle install
exec bundle exec jekyll serve --livereload --host 127.0.0.1 --port 4000 "$@"