import praw
from datetime import datetime, timedelta


def login_to_reddit():
    """
    Goes through the oauth process for reddit. It returns a r object which is
    the logged in object that can interact with reddit. Deliberately verbose.
    """
    # What app is this?
    user_agent = ""
    # username password
    username = ""
    password = ""
    # App id and secret, look up on reddit.
    client_id = ""
    client_secret = ""
    # create login object and create it.
    r = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=username,
                    password=password)
    return r


def main():
    r = login_to_reddit()
    user = r.redditor("vmachiel")
    oldest_day = datetime.utcnow() - timedelta(days=365)

    print("This script will delete old posts, and clean old comments")
    print("The cutoff time is {}.".format(oldest_day))
    proceed = input("Do you want to proceed? (y/n): ")

    if proceed != "y":
        print("Quiting..")
        import sys
        sys.exit(0)

    print("Deleting old submissions and cleaning old comments...")

    comments_new = user.comments.new(limit=None)
    comments_top = user.comments.top(limit=None)
    comments_controversial = user.comments.controversial(limit=None)
    comments_hot = user.comments.hot(limit=None)
    all_comments = [comments_new, comments_top, comments_hot,
                    comments_controversial]

    submissions_new = user.submissions.new(limit=None)
    submissions_controversial = user.submissions.controversial(limit=None)
    submissions_hot = user.submissions.hot(limit=None)
    submissions_top = user.submissions.top(limit=None)
    all_submissions = [submissions_controversial, submissions_hot,
                       submissions_new, submissions_top]

    edit_text = "Edit: Comment has been cleaned"

    for entry in all_comments:
        for c_found in entry:
            if datetime.fromtimestamp(c_found.created) < oldest_day and \
               c_found.body != edit_text:
                print("editing: {}".format(c_found.body))
                c_found.edit(edit_text)

    for entry in all_submissions:
        for s_found in entry:
            if datetime.fromtimestamp(s_found.created) < oldest_day and \
               s_found.subreddit != "thecultcast":
                print("Deleting post: {}".format(s_found.title))
                s_found.delete()


if __name__ == "__main__":
    main()
