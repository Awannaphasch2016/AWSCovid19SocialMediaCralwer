# Path
* dynamoDB/
    * description: get all the data (this needs to change to show all the dynamoDB data)
    * getbottomn/
        * description: get first n earliest data
    * gettopn/
        * description: get first n lastest data
    * getsamplepercent/
        * description: sample n percent of the period specify
    
* streams/
    * description: show all available kinesis streams
    * record/
        * description: to put record in 
    * records/
        * description: to put or get records. sharditerator parameter must be provided. 
         'sharditerator token' can be get from streams/{steam-name}/sharditerator/.
    * sharditerator/
        * description: output sharditerator token.


    

