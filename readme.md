view the web page
https://bumstigedy.github.io/earningsbeat/

This repo contains a personal project which tries to predict if a stock will beat the earnings estimated based on various features.  


The repo needs to be cleaned up a bit more.


The files in teh spy sub folder are the most up to date.  

files
- conversions.py   misc functions to convert to datetime or float format
- get_earnings.py  function to get the earnings data from the api
- get_prices.py    function to get the price history from the api
- testing.py  file to test out the api calls
- testing2.py  file to test out the function calls
- QQQ.csv      list of symbols
- extract_data.py   function to extract and curate the data
- gen_data.py       script to loop through the list of symbols and extract/curate the data then save as a csv file.  run this to generate the ~100 