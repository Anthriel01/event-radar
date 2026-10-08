import sys

import enrich_descriptions, fetch_confs, merge

if __name__ == "__main__":
    fetch_confs.main()
    enrich_descriptions.main()
    merge.main()
    sys.exit(0)
