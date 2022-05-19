import os
from database.DB import DB
from models.user import User


def create_folder():
    static_folder = 'static'
    images_folder = '/images/'
    full_path = static_folder + images_folder

    if not os.path.exists(full_path):
        return os.makedirs(static_folder + images_folder)


def init_db():
    DB.create_table("""CREATE TABLE IF NOT EXISTS `user` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `username` varchar(255) NOT NULL,
                        `password` varchar(255) NOT NULL,
                        PRIMARY KEY (`id`),
                        UNIQUE KEY `username_UNIQUE` (`username`)
                    ) ENGINE=InnoDB""")

    username = "admin"
    password = User.hash_password("admin123")

    DB.insert_into_query(
        "INSERT IGNORE INTO user (username, password) VALUES (%s, %s)", (username, password))

    DB.create_table("""CREATE TABLE IF NOT EXISTS `employee` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `first_name` varchar(255) NOT NULL,
                        `last_name` varchar(255) NOT NULL,
                        `email` varchar(255) NOT NULL,
                        `role` varchar(255) DEFAULT NULL,
                        `linked_in` varchar(255) NOT NULL,
                        `salary` decimal(15,2) NOT NULL,
                        `photo` varchar(255) NULL,
                        `date_started` date NOT NULL,
                        PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB""")


def init():
    create_folder()
    init_db()
