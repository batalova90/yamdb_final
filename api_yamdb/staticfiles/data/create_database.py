import pandas as pd

# load the data into a Pandas DataFrame
genre = pd.read_csv('genre.csv')
# write the data to a sqlite table
# genre.to_sql('genres', conn, if_exists='append', index = False)
