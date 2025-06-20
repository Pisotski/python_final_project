import sys
import os

## FIXME:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.scrape import main

if __name__ == "__main__":
    main()
