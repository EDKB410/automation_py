import logging

import mysql.connector
from mysql.connector import errors

from frame.logger import _init_logger
from frame.utils import Utils


class DB:

    def __init__(self,
                 host='127.0.0.1',
                 port=3306,
                 database=None,
                 user=None,
                 password=None) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._logger = _init_logger(type(self).__name__)
        self.connection = self.connect()

    def connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
        except Exception as e:
            self._logger.exception(e)
            raise e
        else:
            self._logger.info(
                "connected to DB %s@%s:%s", self.database, self.host, self.port)
            return connection

    def close(self):
        self._logger.info("closing DB connection")
        self.connection.close()

    def select(self, query, *args):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (args))
            except errors.Error as e:
                self._logger.exception(e)
                return None
            else:
                self._logger.debug("executing <%s>", query)
                return cursor.fetchall()

    def delete(self, query, *args):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (args))
            except errors.Error as e:
                self._logger.exception(e)
                return None
            else:
                self._logger.debug("executing <%s>", query)
                self.connection.commit()
            finally:
                cursor.close()

    def insert(self, query, *args):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, args)
            except errors.Error as e:
                self._logger.exception(e)
                return None
            else:
                self._logger.debug("executing <%s>", query)
                self.connection.commit()
            finally:
                cursor.close()

    def add_product(self, product):
        self._logger.info("adding <%s>", product.name)
        query_insert_product = """INSERT INTO oc_product
                                (product_id, model, sku, upc, ean, jan, isbn, mpn, location, quantity,
                                stock_status_id, manufacturer_id, price, tax_class_id, date_added, date_modified)
                                VALUES (NULL, %s, '', '', '', '', '', '', '', %s, 0, 0, %s, 0, NOW(), NOW())"""

        query_select_product_id = "SELECT product_id FROM oc_product WHERE model = %s"

        query_insert_description = """INSERT INTO oc_product_description
                                    (product_id, language_id, name, description,
                                    tag, meta_title, meta_description, meta_keyword)
                                    VALUES (%s, %s, %s, %s, '', %s, '', '')"""

        query_insert_product_to_category = """INSERT INTO oc_product_to_category
                                            (product_id, category_id) VALUES (%s, %s)"""

        self.insert(query_insert_product, product.model,
                    product.quantity, product.price)

        product_id = self.select(
            query_select_product_id, product.model).pop()[0]

        self.insert(query_insert_description, product_id, 1, product.name,
                    product.description, product.name)

        self.insert(query_insert_product_to_category, product_id, 33)

    def delete_product(self, name_prefix):
        self._logger.info(
            "deleting products with prefix <%s>", name_prefix)
        query_delete_product = """DELETE oc_product_description, oc_product_to_category, oc_product
                FROM oc_product INNER JOIN oc_product_description INNER JOIN oc_product_to_category
                WHERE oc_product_description.product_id = oc_product.product_id
                AND oc_product.product_id = oc_product_to_category.product_id
                AND oc_product_description.name LIKE %s"""

        self.delete(query_delete_product, f'{name_prefix}\_%')

    def create_customer(self, account):
        self._logger.info("creating customer <%s>", account.email)
        query_get_customer = "SELECT customer_id FROM oc_customer WHERE email = %s"

        query_create_customer = """INSERT INTO oc_customer
                                   (customer_group_id, language_id, firstname, lastname, email, telephone, fax,
                                   password, salt, custom_field, ip, status, safe, token, code, date_added)
                                   VALUES (1, 1, %s, %s, %s, %s, "", %s, %s, "", %s, 1, 0, "", "", NOW())"""

        result = self.select(query_get_customer, account.email)
        if len(result):
            return account

        ip = Utils.get_ip()
        salt, encrypted_password = Utils.encrypt_oc_password(
            account.password_1)
        self.insert(query_create_customer, account.fname, account.lname, account.email, account.phone,
                    encrypted_password, salt, ip)

        return account

    def delete_customer(self, email):
        self._logger.info("deleting customer <%s>", email)

        query_delete_customer = "DELETE FROM oc_customer WHERE email = %s"

        self.delete(query_delete_customer, email)
