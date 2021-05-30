import praw
import csv

reddit = praw.Reddit(
    client_id="iAs8IyCBlgKCRQ",
    client_secret="m9cMmn8QR-US2Kl7zgErvWMFLnSYww",
    user_agent="windows:com.example.myredditapp:v1.2.3 (by u/No_Breakfast_346)",
)

id = 0
for submission in reddit.subreddit('depression').hot(limit=1000):
    print(submission.selftext)
    with open(f'Datasets\\testing_datasets\\reddit.csv', 'a', encoding="utf-8", newline='') as file:
        w = csv.writer(file, delimiter="|")
        w.writerow([submission.selftext, 1])
    id += 1
                                            
#[2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 26, 27, 28, 29, 30, 31, 76]