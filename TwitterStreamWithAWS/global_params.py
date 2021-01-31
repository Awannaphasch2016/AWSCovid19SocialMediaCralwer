# =============
# == AWS Config
# =============
kinesiss_faucovidstreamsentiment = "faucovidstreamsentiment"
API_BASE_URL = "https://77ue66yk77.execute-api.us-east-2.amazonaws.com/dev/"
API_STREAM = API_BASE_URL + "streams/"
API_DYNAMODB = API_BASE_URL + "dynamodb/"

dynamodb_sentiment_table = "faucovidstream_twitter_with_sentiment"


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
# == APIGateway Path
# ======================
# platform=twitter/since=/aspect=trump/text=
# platform=twitter/aspect=trump # pull all data
# platform=twitter/ # pull all data with aspect=trump?
