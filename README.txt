INSTALL DB:
sudo apt-get remove mariadb*
sudo apt-get install mariadb-server -y
sudo mysql_secure_installation
sudo mysql -u root

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT USAGE ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'admin'@localhost;
exit;

DB UTILS:
select * from symbol;
