# Take home project for TenantBase

## Assignment
Create a key-value storage server that speaks a small subset of the memcached protocol and persists data in SQLite. It should also have an HTTP server running out of the same process for monitoring. The monitoring page should include some basic Javascript interactivity.

Run server using: `python main.py database.sqlite`

The server process should start, using database.sqlite as its store and reading or initializing the database file as appropriate. The process should begin accepting connections on two ports:

 - On port `11211`, implementing a subset of memcached’s TCP protocol.
 - On port `8000`, implementing a HTTP server that serves a simple status page, with a
listing of keys and their associated values.

**Memcached Interface**  
The server will speak a tiny subset of the memcached protocol. It should support three
commands:
 - `set` - Ignore the exptime field. Stored values will never expire in
our system.
 - `get`
 - `delete`

**Web Server Interface**  
Upon visiting port 8000, your server should display a simple monitoring interface:
 - Show a list of keys stored in the server, with the values hidden.
 - Items in list should “toggle open” a key using Javascript, and see the associated
value stored for that key.