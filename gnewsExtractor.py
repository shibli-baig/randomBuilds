from GoogleNews import GoogleNews
import pandas as pd

googlenews = GoogleNews(start='05/01/2020', end='05/31/2020')
googlenews.search('ICICI Bank')
result = googlenews.result()
df = pd.DataFrame(result)
print(df.head())
print(df.columns)

for i in range(2, 20):
    googlenews.getpage(i)
    result = googlenews.result()
    df = pd.DataFrame(result)
