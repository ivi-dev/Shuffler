# Report on the code coverage in a HTML format.
# The results are stored in htmlcov/index.html.

. scripts/cov-run.sh
coverage html --data-file=coverage/.coverage -d coverage/html
open coverage/html/index.html