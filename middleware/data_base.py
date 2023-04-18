import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_manager(self, manager_id, date, channel_name):
        with self.connection:
            return self.cursor.execute(
                """
                INSERT INTO manager (manager_id, date, channel_name) VALUES (?, ?, ?)
                """, (manager_id, date, channel_name, )
            )

    def delete_manager(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM manager WHERE manager_id = ?", (user_id, ))

    def add_date(self, manager_id, user_id, date):
        with self.connection:
            return self.cursor.execute(
                """
                UPDATE all_statistic SET date = ? WHERE (manager_id = ?) AND (user_id = ?);
                """, (date, manager_id, user_id, )
            )

    def add_client_status(self, user_id, manager_id, client_status):
        with self.connection:
            return self.cursor.execute(
                """
                UPDATE all_statistic SET client_status = ? WHERE (manager_id = ?) AND (user_id = ?);
                """, (client_status, manager_id, user_id,)
            )

    def add_first_deposit(self, user_id, manager_id, first_deposit):
        with self.connection:
            return self.cursor.execute(
                """
                UPDATE all_statistic SET first_deposit = ? WHERE (manager_id = ?) AND (user_id = ?); 
                """, (first_deposit, manager_id, user_id, )
            )

    def add_start_capital(self, user_id, manager_id, start_capital):
        with self.connection:
            return self.cursor.execute(
                """
                UPDATE all_statistic SET start_capital = ? WHERE (manager_id = ?) AND (user_id = ?); 
                """, (start_capital, manager_id, user_id, )
            )

    def add_other_deposit(self, user_id, manager_id, other_deposit):
        with self.connection:
            check_other_deposit = self.cursor.execute(
                """
                SELECT other_deposits FROM all_statistic WHERE (manager_id = ?) AND (user_id = ?);
                """, (manager_id, user_id, )
                ).fetchone()
            if check_other_deposit[0] is None:
                return self.cursor.execute(
                    """
                    UPDATE all_statistic SET other_deposits = ? WHERE (manager_id = ?) AND (user_id = ?); 
                    """, (other_deposit+".", manager_id, user_id, )
                )
            else:
                cell_value = self.cursor.execute(
                """
                SELECT other_deposits FROM all_statistic WHERE (manager_id = ?) AND (user_id = ?);
                """, (manager_id, user_id, )
                ).fetchone()
                oth_dep = ''
                for other_dep in cell_value[0].split('.'):
                    if other_dep:
                        oth_dep += other_dep + "."
                return self.cursor.execute(
                    """
                     UPDATE all_statistic SET other_deposits = ? WHERE (manager_id = ?) AND (user_id = ?);
                    """, (oth_dep+other_deposit, manager_id, user_id, )
                )

    def add_manager_to_channel(self, channel_name):
        with self.connection:
            return self.cursor.execute("""
            UPDATE channel
            SET manager_id = ManagerTable.manager_id
            FROM (SELECT channel_name, manager_id FROM manager) AS ManagerTable
            WHERE (ManagerTable.channel_name = ?) AND (ManagerTable.channel_name = channel.channel_name)
            """, (channel_name, ))
