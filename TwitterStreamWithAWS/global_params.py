# =============
# == AWS Config
# =============
kinesiss_faucovidstreamsentiment = "faucovidstreamsentiment"
API_BASE_URL = "https://77ue66yk77.execute-api.us-east-2.amazonaws.com/dev/"
API_STREAM = API_BASE_URL + "streams/"
API_DYNAMODB = API_BASE_URL + "dynamodb/"


# --- kinesis
# kinesis_reddit_stream = "faucovidstream_input_from_reddit"
kinesis_reddit_stream = "faucovidstream-input-from-reddit"
kinesis_twitter_stream = "faucovidstream-input"
# kinesis_twitter_stream = "random"
# --- dynamodb
dynamodb_sentiment_table = "faucovidstream_twitter_with_sentiment"
# --- api gateway

# =============
# == Aspects
# =============
ALL_ASPECTS = [
    "work_from_home",
    "social_distance",
    "corona",
    "reopen",
    "lockdown",
]
LOCKDOWN_KEYWORDS = [
    "quarantine",
    "isolation",
    "quarantining",
    "lockdown",
    "isolate",
]
REOPEN_KEYWORDS = ["reopening", "reopen"]
SOCIAL_DISTANCE_KEYWORDS = ["social distance", "social distancing"]
WORK_FROM_HOME_KEYWORDS = [
    "distance learning",
    "work online",
    "remote work",
    "workonline",
    # "remote work",
    # "online learning",
]
COVID_KEYWORDS = ["covid", "corona", "sarscov2"]

# ======================
# == Reddit
# ======================
ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT = [
    "Corona",
    "COVID19",
    "China_Flu",
    "coronavirus",
]
ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT = ["CoronavirusUS", "coronavirusUK"]
ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT = [
    "CoronavirusMidwest",
    "CoronavirusSouth",
    "CoronavirusSouthEast",
    "CoronavirusWest",
]

# --------List of USA States
ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT = [
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "california",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "georgia",
    "hawaii",
    "idaho",
    "illinois",
    "indiana",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "massachusetts",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "newhampshire",
    "newjersey",
    "newmexico",
    "newyork",
    "northcarolina",
    "northdakota",
    "ohio",
    "oklahoma",
    "oregon",
    "pennsylvania",
    "rhodeisland",
    "southcarolina",
    "southdakota",
    "tennessee",
    "texas",
    "utah",
    "vermont",
    "virginia",
    "washington",
    "westvirginia",
    "wisconsin",
    "wyoming",
]

STREAM_COMMENTS_DATA_KEYS = [
    "author",
    "body",
    "body_html",
    "created_utc",
    # # NOTE: for distinguished, its type if Nonetype, and I don't know how to
    # #  check it because
    # #  this NoneType is not the same as None
    # 'distinguished',
    "edited",
    "id",
    "is_submitter",
    "link_id",
    "parent_id",
    "permalink",
    "replies",
    "score",
    "stickied",
    "submission",
    "subreddit",
    "subreddit_id",
]
