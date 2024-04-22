import psycopg2
from generic_api_testing.common.config.config import GeneralSettings

class DatabaseConnection() :
    
    connections = {}
    database_connections_info = {}
    
    def obtain_connection(database_name):
        
        name = DatabaseConnection.obtain_database_name(database_name)
        
        if (name in DatabaseConnection.connections):
            print("Connection obtained for database " + database_name + "!")
        else:
            print("Connecting to database " + database_name + "...")
            
            try:
                conn_info = DatabaseConnection.database_connections_info[name]
                new_con = psycopg2.connect(database=conn_info['database'], user=conn_info['user'], password=conn_info['password'], host=conn_info['host'], port=conn_info['port'])
                new_cur = new_con.cursor()
                new_connection = { 'con': new_con, 'cur': new_cur }
                
                DatabaseConnection.connections[name] = new_connection
                print("Connection Established!")
                
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error obtaining connection {}".format(error))
                return error
    
    def select_one(database_name, query):
        
        name = DatabaseConnection.obtain_database_name(database_name)
        
        try:
            cur = DatabaseConnection.connections[name]['cur']
            cur.execute(query)
            query_result = cur.fetchone()
            return query_result
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error
    
    def select_all(database_name, query):
        
        name = DatabaseConnection.obtain_database_name(database_name)
        
        try:
            cur = DatabaseConnection.connections[name]['cur']
            cur.execute(query)
            query_result = cur.fetchall()
            return query_result
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error

    def update(database_name, query):
        
        name = DatabaseConnection.obtain_database_name(database_name)
        
        try:
            DatabaseConnection.connections[name]['cur'].execute(query)
            DatabaseConnection.connections[name]['con'].commit()
            print("Query successfuly executed!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error

    def obtain_database_name(database_name):
        return GeneralSettings.env + "_" + GeneralSettings.product + "_" + database_name