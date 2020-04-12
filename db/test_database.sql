DROP TABLE queue7;
DROP TABLE groceryStores;

CREATE TABLE queue (
	ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(25) DEFAULT 'Walk-In',
    position INT NOT NULL,
    ticket_gen_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone_num VARCHAR(12) NOT NULL, #'(555)-555-5555', could be unique but make not unique for revisiting store in same day scenario
    authentication VARCHAR(160) DEFAULT NULL #length determined by verification into string/sql storable value
);

CREATE TABLE groceryStores ( #used to keep track of all grocery stores, login info
	grocery_id INT AUTO_INCREMENT PRIMARY KEY, #something like zipcode + streename + storeName
    store_name VARCHAR(30),
    address VARCHAR(30), #doesnt include city, state, zip code
    city VARCHAR(20),
    state VARCHAR(2), #initials only
    zip_code VARCHAR(5),
	max_in_store INT DEFAULT 100
);

-- INSERTS --
INSERT INTO queue(cust_name, position, ticket_gen_time, phone_num) VALUES("Lindsay Lohan", 1, '2020-03-28 19:00:00', '+15555555555');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Eric Andre", 2, '234-775-3262');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Marisol Garcia", 3, '657-231-6763');

INSERT INTO groceryStores(store_name, address, city, state, zip_code) VALUES("Food Lion", "8600 University City Blvd", "Charlotte", "NC", 28213);
INSERT INTO groceryStores(store_name, address, city, state, zip_code) VALUES("Harris Teeter", "1704 Harris Houston Rd", "Charlotte", "NC", 27560);

SELECT * FROM queue1;
SELECT * FROM groceryStores;
ALTER TABLE groceryStores
MODIFY address VARCHAR(50);