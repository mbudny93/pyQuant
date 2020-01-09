----------------------------------------------------------------------------------------------------
INSTALL mysql on ARCHLINUX
----------------------------------------------------------------------------------------------------
sudo pacman -S mariadb
no-password installation:
    sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl start mariadb
cd ~/pyQuant
sudo mysql -u root < ./utils/create_db_user.sql
log in to mysql: sudo mysql -u root
----------------------------------------------------------------------------------------------------
UNINSTALL mysql on ARCHLINUX
----------------------------------------------------------------------------------------------------
sudo systemctl stop mariadb
sudo pacman -R mariadb
sudo pacman -R mariadb-clients
sudo rm -rf /var/lib/mysql
----------------------------------------------------------------------------------------------------
INSTALL mysql on ubuntu:
----------------------------------------------------------------------------------------------------
sudo apt-get install mariadb-server -y
sudo mysql_secure_installation
sudo mysql -u root -p < create_db_user.sql

----------------------------------------------------------------------------------------------------
UNINSTALL mysql:
----------------------------------------------------------------------------------------------------
arch:
    # systemctl stop mariadb
    sudo pacman -R mariadb
    sudo pacman -R mariadb-clients
    sudo rm -rf /var/lib/mysql
ubuntu:
    sudo apt-get remove mariadb*
----------------------------------------------------------------------------------------------------

DB UTILS:
----------------------------------------------------------------------------------------------------
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT USAGE ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'admin'@localhost;
exit;

select * from symbol;

----------------------------------------------------------------------------------------------------
INSTALL PYTHON PACKAGES:
----------------------------------------------------------------------------------------------------
python -m venv /tmp/pyQuant_venv
source /tmp/pyQuant_venv/bin/activate
pip install -r requirements.txt

