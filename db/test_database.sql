DROP TABLE queue;
DROP TABLE inStore;
DROP TABLE timeSpent;

CREATE TABLE queue (
	ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(25) DEFAULT 'Walk-In',
    position INT NOT NULL,
    ticket_gen_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone_num VARCHAR(12) NOT NULL #'(555)-555-5555', could be unique but make not unique for revisiting store in same day scenario
);

CREATE TABLE inStore (	#used to track number of people in store
	ticket_id INT PRIMARY KEY,
    sign_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE timeSpent ( #used to track avg time spent in store for past MAXINSTORE customers
	ticket_id INT PRIMARY KEY,
    sign_in TIME,
    sign_out TIME, #needs to default to current time, not current_time()
    tot_time INT
);

-- EXAMPLES --
#INSERT INTO tableName VALUES(col1Val, col2Val, col3Val, etc);	insert data into table
#SELECT * FROM tableName;	prints everything in the table
#ALTER TABLE tableName ADD  colName varType;
#ALTER TABLE tableName DROP COLUMN colName;
#DESCRIBE queue;	prints table columns with value types
#TIMESTAMP format 'YYYY-MM-DD HH:MM:SS' 24HR format

INSERT INTO queue(ticket_id, cust_name, position, ticket_gen_time, phone_num) VALUES(12, "Lindsay Lohan", 1, '2020-03-28 19:00:00', '555-555-5555');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Eric Andre", 2, '234-775-3262');
INSERT INTO queue(cust_name, position, phone_num) VALUES("Marisol Garcia", 3, '657-231-6763');

INSERT INTO inStore(ticket_id) VALUES(5);
INSERT INTO inStore(ticket_id, sign_in) VALUES(6, '2020-03-29 19:03:34');

INSERT INTO timeSpent(ticket_id, sign_in, sign_out) VALUES(4, '05:35:50', '06:00:00');


UPDATE timeSpent SET tot_time = TIMESTAMPDIFF(SECOND, sign_in, sign_out)
WHERE ticket_id = 4;
-- UPDATE queue
-- SET phone_number = '555-555-5555'
-- WHERE ticket_id = 4;

SELECT * FROM queue;
SELECT * FROM inStore;
SELECT * FROM timeSpent;