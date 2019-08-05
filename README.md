# TenantBase Take Home Assignment

This repository contains the completed project for the TenantBase take home assignment. The main python program starts two processes as specified in the pdf instructions. The first starts the Flask app and delivers the client bundle on port 8000. The client receives the items list when it connects to the server using the socket io protocol. When the "return_items" event is emitted by the flask socket, the client will receive the list of items from the database. 

The second process starts the memcached server on port 11211 which emulates the [memcached protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) and implements the `get`, `set`, and `delete` methods. The server is multithreaded and can accept multiple clients from different terminal sessions. The memcached server will listen for input using sockets and update the SQLite database accordingly. On modifications to the database(`set` and `delete`), the server will issue a get request to the flask server to send the updated list of items back to the client.

### Requirements
 | Name  | Version  |
 |--------|---------|
 | Python | 3.7.4   |
 | Node   | 11.13.0 |
 | npm    | 6.7.0   |

### How to Run
Execute the following commands in order:
- `npm install` to install node modules
- `npm run build` to build distribution bundle
- `pip3 install -r requirements.txt` to install python dependencies

To run the program, execute:
- `python3 main.py <database.sqlite>` where `<database.sqlite>` is name of database you want to use
	- You can use the existing `database.sqlite` provided in the repository or you can specify a new one.


The following is an example of what the page should look like:

![Example](https://i.imgur.com/B60lPnR.png)

### Suggested improvements
- Authentication 
- Message queue (RabbitMQ)
- Material design
- Mobile styles
- GraphQL/Thrift
- Jest tests