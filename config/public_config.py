class BaseConfig:
    URL = "https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd"
    MAX_PAGES = 150
    WAIT_TIMEOUT = 15
    CHROMEDRIVER_PATH = "/home/Igor/programs/chromedriver-linux64/chromedriver"
    CHROMIUM_PATH = "/usr/bin/chromium"
    OUTPUT_PARSER_PATH = "results/results.csv"
    OUTPUT_NORM_PATH = "results/resultsNorm.csv"