Description:
My solution is based on 3 steps:
1. loading all rows of all files and saves all the visits timestamp per user-site pair
2. for each visitor-site pair take all visits and calculate all sessions legnths for this pair
3. separation between the user data and site data:
    a. for each user saves the amount of websites
    b. for each site saves the amount of sessions
    c. for each site and session length pair save how many sessions were 
        (after I finished the exercise I think it was better to save the only the amount of sessions with length 0 
        and just save the rest of the sessions lenghts in 1 array that way I could simply go directly to the cell in the array that contains the median).
4. most of the data is now saved in key-value data structures so it is easy to answer the queries

Scale:
1. Because there are a lot of visitors and the process is based on visitors I would send each row 
    to a different stream where a different process machine would process all the data of the specific user.
2. In addition I would save for each session the beginning and end 
    that would give me the ability to process the data I get now and if later I will get additional data 
    I'll be able to identify the sessions that should change and recalculate them, in more stream-like processing rather than 1 big ETL process.
3. Because the loading and processing are done by key-value pairs we can use distibuted key value storage like cassandra and that way we can work
    on each entity separately

Space and time complexity:
The solution uses lot of memory because it loads the entire input into the memory, but the final structures are lot smaller.
Space:
for data on sites:
1. session count will be O(N) where N is the number of sites
2. session lengths will be O(N)*O(M) where N is the number of sites and M is the number of unique session length

for user data:
1. O(N) where N is the number of users.

Time (query):
number of sessions for site - O(1)
number of unique sites for user - O(1)
median session length for site - O(N) where N is the number of unique session lengths, in case I would implement the solution on the descrition(3)
it would increase the amount of space a little bit but the query will return in O(1)

Time (loading):
We save all the data once and process all of it once it would cost O(2N) where N is the amount of events we get in addition, 
we sort the timestamps in each user so it adds O(nlogn) or O(nlogn)+O(2N).
We save separate all the data based on sessions we built it would cost O(N) where N is the number of sessions (equal to number of events in worst case scenario).

How to setup:
1. run the application with cmd parameter "load" in order to load all the data

How to query:
1. choose info type to query (num_sessions/median_session_length/num_unique_visited_sites)
2. run the application with the method name as first parameter and site/user as second parameter
for example:
    userInteraction.py num_unique_visited_sites visitor_10 - will give the number of unique websites viseted by visitor_10