This is a little project I made to find cheap houses for rent near the university.
It is comprised of two parts. It first scrapes the various info off the websites,
then it finds the distance to the university from each of these places via transit.

You need a google api key which you can obtain here: https://console.cloud.google.com/ for free (you need a google accout). You also need to enable the matrix distance api.

To use this program follow these steps:
1. put the api key into a file called api_key.txt in the folder with the program
2. run main.py with your custom settings. This will scrape zolo.ca for different house listings.
3. run analysis.py(). You can use the predefined sorting method, or choose your own from this file. This sort and output the houses in order defined by a cost function.
