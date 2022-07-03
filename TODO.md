## Next steps and issues for the Scan class
- Add a method to convert a Scan into JSON
- add a __repr__ method 
- explore other ways to extend the Scan class other than through kwargs, **which may become cumbersome**
- require certain metadata to be included if necessary
- add a method to query just the metadata
- add a built-in visualization tool for the DS team (this might be overkill)

## Next steps and issues for LocalDB
- handle the construction of scans in fetch_data asynchronously, perhaps using a stream: 
    Waiting on fetch_data to return *all* of the scans may hinder the performance of any downstream programs that rely on it. Consuming the data and creating a Scan object as calls to the database return may fix this issue. I believe streams can accomplish this asynchronous behavior, but I didn't have time to look into it deeply. 
- add more options to the list of **kwargs in fetch_data so consumers of this method may be more specific
- add methods for other CRUD operations. So far, we've only done Reading through fetch_data

#### Other issues: 
- In fetch_data, when I grouped data together according to the test_id, I encountered a problem where a Cursor object can only be iterated once. To fix this, I used this one iteration to create a list with the same data—this strikes me as inefficient. On a second pass, I would refactor the code to handle all the grouping during this single iteration through the cursor. 
- There's likely a better way to assign attributes for metadata than what I did (constructing a dictionary then dropping the unnecessary fields)
- as the data pool grows, we'll clearly need to modify the LocalDB class to access a remote database. Eventually, it may be necessary to bring in some heavy-hitting big data tools to consume huge swaths of data as well. 
- my documentation doesn't follow any standard conventions. It's relatively simple, but as these classes are further integrated with other tools, I would need to configure it to maximize their usability. 