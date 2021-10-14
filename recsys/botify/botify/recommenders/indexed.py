import random

from .random import Random
from .recommender import Recommender


class Indexed(Recommender):
    """
    Recommend personalized tracks for each user cached in Redis.
    Fall back to the random recommender if no recommendations found for the user.
    """

    def __init__(self, tracks_redis, recommendations_redis):
        self.recommendations_redis = recommendations_redis
        self.fallback = Random(tracks_redis)

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        recommendations = self.recommendations_redis.get(user)
        if recommendations is not None:
            shuffled = list(recommendations)
            random.shuffle(shuffled)
            return shuffled[0]
        else:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)