CREATE TABLE groceryStores ( #used to keep track of all grocery stores, login info
	grocery_id INT AUTO_INCREMENT PRIMARY KEY, #something like zipcode + streename + storeName
    store_name VARCHAR(30),
    address VARCHAR(30), #doesnt include city, state, zip code
    city VARCHAR(20),
    state VARCHAR(2), #initials only
    zip_code VARCHAR(5),
	max_in_store INT DEFAULT 100
);