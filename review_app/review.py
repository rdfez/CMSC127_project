# from misc import count, get_id, get_input, validator
from main import init
import mariadb


# View all reviews for a food item or establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
#   2. type (string): entity type (establishment, item)
#   3. id (int): entity id
#   4. is_recent (bool): if view_all() should return reviews not older than a month
def view_allreviews (cur, type, id, is_recent): 
  if (is_recent):
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {type}_id = ? AND DATEDIFF(NOW(), date) <= 30", (id,)) 
  else:
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {type}_id = ?", (id,)) 

  reviews = cur.fetchall()
  if (len(reviews) == 0):
      if (is_recent):
        print(f"\nThere are no recent reviews for that food {type}!")
      else:
        print(f"\nThere are no reviews for that food {type}!")
  else:
    for (review_id, rating, date, establishment_id, item_id, user_id) in reviews:
      # User name
      cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
      username = cur.fetchone()[0]

      # Establishment name
      cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
      establishment_name = cur.fetchone()[0]

      if (type == "item"):
        #Food name
        cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
        food_name = cur.fetchone()[0]
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \tDate: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print(f"Food Name: \t\"{food_name}\"")
        print("\n======================================")

      else:
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \t Date: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print("\n======================================")

  return
#################################

# Connect to MariaDB Platform
conn_bool = True
while conn_bool:
    mariadb_password = input("Enter password: ")

    try:
        conn = mariadb.connect(
            user = "root",
            password = mariadb_password,
            host = "localhost",
            autocommit = True
        )

        if(conn):
            conn_bool = False

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

# Get Cursor for DB functions
global cur 
cur = conn.cursor()

# Create database/tables on initial boot and use app database
cur.execute("CREATE DATABASE IF NOT EXISTS `review_app`;")
cur.execute("USE `review_app`;")
cur.execute('''
    CREATE TABLE IF NOT EXISTS `user` (
        `user_id` INT (50) NOT NULL,
        `email` VARCHAR (50) NOT NULL,
        `username` VARCHAR (50) NOT NULL,
        `login_credentials` VARCHAR (50) NOT NULL,
        `is_customer` BOOLEAN,
        `is_manager` BOOLEAN,
        PRIMARY KEY (`user_id`)
    );
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS `food_establishment` (
        `establishment_id` INT (50) NOT NULL,
        `establishment_name` VARCHAR (50) NOT NULL,
        `establishment_rating` INT (1) DEFAULT NULL,
        `location` VARCHAR (50),
        `manager_id` INT (50) NOT NULL,
        PRIMARY KEY (`establishment_id`),
        CONSTRAINT `foodestablishment_managerid_fk` FOREIGN KEY (`manager_id`) REFERENCES
    `user` (`user_id`)
    );
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS `food_item` (
        `item_id` INT (50) NOT NULL,
        `food_name` VARCHAR (50) NOT NULL,
        `price` INT (50) NOT NULL,
        `type` VARCHAR (50) NOT NULL,
        `establishment_id` INT (50) NOT NULL,
        `manager_id` INT (50) NOT NULL,
        PRIMARY KEY (`item_id`),
        CONSTRAINT `fooditem_establishmentid_fk` FOREIGN KEY (`establishment_id`) REFERENCES
    `food_establishment` (`establishment_id`),
        CONSTRAINT `fooditem_managerid_fk` FOREIGN KEY (`manager_id`) REFERENCES
    `user` (`user_id`)
    );
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS `food_review` (
        `review_id` INT (50) NOT NULL,
        `rating` INT (1) NOT NULL,
        `date` DATE NOT NULL,
        `establishment_id` INT (50) NOT NULL,
        `item_id` INT (50),
        `user_id` INT (50) NOT NULL, 
        PRIMARY KEY (`review_id`),
        CONSTRAINT `foodreview_establishmentid_fk` FOREIGN KEY(`establishment_id`) REFERENCES
    `food_establishment` (`establishment_id`),
        CONSTRAINT `foodreview_itemid_fk` FOREIGN KEY (`item_id`) REFERENCES
    `food_item` (`item_id`),
        CONSTRAINT `foodreview_userid_fk` FOREIGN KEY (`user_id`) REFERENCES
    `user` (`user_id`)
    );
''')


view_allreviews(cur, "establishment", 30, False)
view_allreviews(cur, "item", 4, False)