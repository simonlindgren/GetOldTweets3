# GetOldTweets3
This project, originally by [Jefferson-Henrique](https://github.com/Jefferson-Henrique/GetOldTweets-python) and improved by [Mottl](https://github.com/Mottl/GetOldTweets3), is designed to perform searches for old tweets through [twitter.com](https://twitter.com) and store them as ordered datasets. This version writes the data to sql, and contains a wrapper script for easy launching of search jobs as well as a csv exporter.

## Wrapper
To use the wrapper script:

```
python got3.py
```

## Export to csv
After running a search:
```
python sql2csv.py
```

## Prerequisites
Run the following command to install package dependencies:
```
pip install -r requirements.txt
```
