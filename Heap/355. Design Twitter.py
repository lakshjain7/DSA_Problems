"""
Problem: 355. Design Twitter
Difficulty: Medium
Topics: Heap, Hash Map, Design, Linked List

Problem Statement:
Design a simplified version of Twitter where users can post tweets, follow/unfollow
another user, and see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:
  - Twitter(): Initializes your twitter object.
  - void postTweet(int userId, int tweetId): Composes a new tweet with ID tweetId by
    the user userId. Each call to this function will be made with a unique tweetId.
  - List[int] getNewsFeed(int userId): Retrieves the 10 most recent tweet IDs in the
    user's news feed. Each item in the news feed must be posted by users who the user
    followed or by the user themselves. Tweets must be ordered from most recent to least.
  - void follow(int followerId, int followeeId): The user with ID followerId starts
    following the user with ID followeeId.
  - void unfollow(int followerId, int followeeId): The user with ID followerId starts
    unfollowing the user with ID followeeId.

Examples:
  twitter = Twitter()
  twitter.postTweet(1, 5)   # User 1 posts tweet 5
  twitter.getNewsFeed(1)    # → [5]
  twitter.follow(1, 2)      # User 1 follows user 2
  twitter.postTweet(2, 6)   # User 2 posts tweet 6
  twitter.getNewsFeed(1)    # → [6, 5]  (most recent first)
  twitter.unfollow(1, 2)    # User 1 unfollows user 2
  twitter.getNewsFeed(1)    # → [5]

Constraints:
  - 1 <= userId, followerId, followeeId <= 500
  - 0 <= tweetId <= 10^4
  - All the tweets have unique IDs.
  - At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow.

Approach:
  Use a global timestamp counter to track tweet recency.
  - tweets: dict[userId → list of (timestamp, tweetId)]
  - following: dict[userId → set of followeeIds]

  getNewsFeed: use a max-heap (negate timestamp for Python's min-heap) initialized
  with the most recent tweet of each followed user + self. Then pop up to 10 times,
  pushing the next tweet from the same user each time (like k-way merge).

  This is the classic "merge k sorted lists" pattern applied to tweets.

Complexity:
  Time:  O(k log k) per getNewsFeed, where k = number of followed users
  Space: O(n) total for tweets and follow sets
"""

import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self):
        self.timestamp: int = 0
        # userId → list of (-timestamp, tweetId)  (stored newest-last so we can index -1)
        self.tweets: dict = defaultdict(list)
        # followerId → set of followeeIds
        self.following: dict = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((-self.timestamp, tweetId))
        self.timestamp += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        # Collect all users whose tweets we care about
        users = self.following[userId] | {userId}

        # Max-heap seeded with the most recent tweet from each user
        # Heap element: (neg_time, tweetId, userId, tweet_index_in_list)
        heap: list = []
        for uid in users:
            if self.tweets[uid]:
                idx = len(self.tweets[uid]) - 1
                neg_time, tid = self.tweets[uid][idx]
                heapq.heappush(heap, (neg_time, tid, uid, idx))

        result: List[int] = []
        while heap and len(result) < 10:
            neg_time, tid, uid, idx = heapq.heappop(heap)
            result.append(tid)
            if idx > 0:
                next_neg_time, next_tid = self.tweets[uid][idx - 1]
                heapq.heappush(heap, (next_neg_time, next_tid, uid, idx - 1))

        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)


# ─── Tests ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # LeetCode example
    twitter = Twitter()
    twitter.postTweet(1, 5)
    assert twitter.getNewsFeed(1) == [5]
    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    assert twitter.getNewsFeed(1) == [6, 5]
    twitter.unfollow(1, 2)
    assert twitter.getNewsFeed(1) == [5]

    # Only own tweets when not following anyone
    t2 = Twitter()
    t2.postTweet(1, 1)
    t2.postTweet(1, 2)
    t2.postTweet(1, 3)
    assert t2.getNewsFeed(1) == [3, 2, 1]  # most recent first

    # More than 10 tweets — only top 10 returned
    t3 = Twitter()
    for i in range(1, 13):
        t3.postTweet(1, i)
    feed = t3.getNewsFeed(1)
    assert len(feed) == 10
    assert feed == [12, 11, 10, 9, 8, 7, 6, 5, 4, 3]

    # Interleaved tweets from followed users, sorted by recency
    t4 = Twitter()
    t4.postTweet(1, 10)
    t4.postTweet(2, 20)
    t4.postTweet(1, 30)
    t4.follow(1, 2)
    feed4 = t4.getNewsFeed(1)
    assert feed4 == [30, 20, 10]

    # Unfollow removes their tweets from feed
    t4.unfollow(1, 2)
    assert t4.getNewsFeed(1) == [30, 10]

    # New user with no tweets/follows
    t5 = Twitter()
    assert t5.getNewsFeed(99) == []

    print("All 355 tests passed!")
