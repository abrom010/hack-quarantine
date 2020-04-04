CREATE DATABASE hackathon;
DROP TABLE queue;
DROP TABLE inStore;
DROP TABLE timeSpent;
DROP TABLE groceryStores;

CREATE TABLE queue (
	ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(25) DEFAULT 'Walk-In',
    position INT NOT NULL,
    ticket_gen_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone_num VARCHAR(12) NOT NULL, #'(555)-555-5555', could be unique but make not unique for revisiting store in same day scenario
    authentication VARCHAR(160) DEFAULT NULL #length determined by verification into string/sql storable value
);

CREATE TABLE inStore (	#used to track number of people in store
	ticket_id INT PRIMARY KEY,
    cust_name VARCHAR(25),
    sign_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    authentication VARCHAR(160)
);

CREATE TABLE timeSpent ( #used to track avg time spent in store for past MAXINSTORE customers
	ticket_id INT PRIMARY KEY,
    sign_in TIME,
    sign_out TIME DEFAULT CURRENT_TIMESTAMP, #needs to default to current time, not current_time()
    tot_time INT
);

CREATE TABLE groceryStores ( #used to keep track of all grocery stores, login info
	grocery_id INT AUTO_INCREMENT PRIMARY KEY, #something like zipcode + streename + storeName
    store_name VARCHAR(30),
    address VARCHAR(30), #doesnt include city, state, zip code
    city VARCHAR(20),
    state VARCHAR(2), #initials only
    zip_code VARCHAR(5),
    username VARCHAR(20),
    email VARCHAR(30), #possibly not needed
    passwd VARCHAR(64), #hashed value, might need a lot of chars
	max_in_store INT DEFAULT 100,
    push_back_penalty VARCHAR(10) DEFAULT "Function", #prob needs to be a function that takes number of times late to give how much person is pushed back
	wait_leniency INT DEFAULT 300 #how long store is willing to wait for a no-show before penilizing, in seconds
);

-- EXAMPLES --
#INSERT INTO tableName VALUES(col1Val, col2Val, col3Val, etc);	insert data into table
#SELECT * FROM tableName;	prints everything in the table
#ALTER TABLE tableName ADD  colName varType;
#ALTER TABLE tableName DROP COLUMN colName;
#DESCRIBE queue;	prints table columns with value types
#TIMESTAMP format 'YYYY-MM-DD HH:MM:SS' 24HR format

-- INSERTS --
INSERT INTO queue(ticket_id, cust_name, position, ticket_gen_time, phone_num) VALUES(12, "Lindsay Lohan", 1, '2020-03-28 19:00:00', '555-555-5555');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Eric Andre", 2, '234-775-3262');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Marisol Garcia", 3, '657-231-6763');

INSERT INTO inStore(ticket_id) VALUES(5);
INSERT INTO inStore(ticket_id, sign_in) VALUES(6, '2020-03-29 19:03:34');

INSERT INTO timeSpent(ticket_id, sign_in, sign_out) VALUES(4, '05:35:50', '06:00:00');

INSERT INTO groceryStores(store_name, address, city, state, zip_code) VALUES("Food Lion", "8600 University City Blvd", "Charlotte", "NC", 28213);
INSERT INTO groceryStores(store_name, address, city, state, zip_code) VALUES("Harris Teeter", "1704 Harris Houston Rd", "Charlotte", "NC", 27560);
INSERT INTO groceryStores(store_name, zip_code) VALUES("Kroger", "27560");
INSERT INTO groceryStores(store_name, zip_code) VALUES("Aldi", "27555");
-- --

-- get full address -- 
SELECT CONCAT(address, ", ", city, ", ", state, ", ", zip_code) AS FullAddress FROM groceryStores;

UPDATE timeSpent SET tot_time = TIMESTAMPDIFF(SECOND, sign_in, sign_out)
WHERE ticket_id = 4;
-- UPDATE queue
-- SET phone_number = '555-555-5555'
-- WHERE ticket_id = 4;

SELECT * FROM queue;
SELECT * FROM inStore;
SELECT * FROM timeSpent;
SELECT * FROM groceryStores;