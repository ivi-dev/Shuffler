# Report on the code coverage in a HTML format.
# The results are stored in htmlcov/index.html.

. scripts/cov-run.sh
OUTPUT=coverage/html
coverage html --data-file=$COV_FILE -d $OUTPUT
open coverage/html/index.html