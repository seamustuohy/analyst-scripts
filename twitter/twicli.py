import argparse
import tweepy
import json
import sys
from bird import Bird


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check twitter easily')
    parser.add_argument('--user', '-u',
            help='Get user infos')
    parser.add_argument('--tweets', '-t',
            help='Download tweets of an user')
    parser.add_argument('--tweet', '-T',
            help='Download tweet with the given id')
    parser.add_argument('--save', '-s',
            help='save all infos about an user and their tweets')
    parser.add_argument('--file', '-f',
            help='File containing usernames, display user infos in CSV format')

    args = parser.parse_args()

    bird = Bird()

    if args.user:
        a = bird.get_profile_information(args.user)
        print json.dumps(a._json, sort_keys=True, indent=4, separators=(',', ': '))
    elif args.tweets:
        a = bird.get_user_tweets(args.tweets)
        for page in a:
            # FIXME : improve this
            print json.dumps(page._json, sort_keys=True, indent=4, separators=(',', ': '))
    elif args.tweet:
        a = bird.get_tweet(args.tweet)
        print json.dumps(a._json, sort_keys=True, indent=4, separators=(',', ': '))
    elif args.save:
        data = {}
        a = bird.get_profile_information(args.save)
        data["user"] = a._json
        b = bird.get_user_tweets(args.save)
        data["tweets"] = []
        for t in b:
            data["tweets"].append(t._json)
        print(json.dumps(data))
    elif args.file:
        f = open(args.file, 'r')
        data = f.read().split()
        f.close()
        print("Handle;Name;Id;Description;url;Location;Time zone;UTC offset;Created at;Last Tweet;lang;Tweet count;Favourite count;Followers count;Following count;List count;Verified;Geo enabled;Default profile;Default profile image;Contributors Enabled")
        for d in data:
            try:
                user = bird.get_profile_information(d.strip())
                print("%s;%s;%i;%s;%s;%s;%s;%i;%s;%s;%s;%i;%i;%i;%i;%i;%s;%s;%s;%s;%s" %
                        (
                            user.screen_name,
                            user.name,
                            user.id,
                            user.description.replace(";", ",").replace("\n", ""),
                            user.entities['url']['urls'][0]['expanded_url'] if user.url is not None else "",
                            user.location,
                            user.time_zone,
                            user.utc_offset if user.utc_offset is not None else 0,
                            user.created_at.strftime("%m/%d/%Y %H:%M:%S"),
                            user.status.created_at.strftime("%m/%d/%Y %H:%M:%S") if user.status is not None else "",
                            user.lang,
                            user.statuses_count,
                            user.favourites_count,
                            user.followers_count,
                            user.friends_count,
                            user.listed_count,
                            user.verified,
                            user.geo_enabled,
                            user.default_profile,
                            user.default_profile_image,
                            user.contributors_enabled
                        )
                )
            except tweepy.error.TweepError:
                sys.stderr.write("User %s not found\n" % d.strip())


