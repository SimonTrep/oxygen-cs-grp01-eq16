import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()


# Connexion à la base de données
def get_conn():
    database_server_name = os.getenv("DATABASE_SERVER_NAME")
    database_name = os.getenv("DATABASE_NAME")
    user_name = os.getenv("USER_NAME")
    user_password = os.getenv("USER_PASSWORD")
    connection_string = (
        """Driver={ODBC Driver 18 for SQL Server};
                        Server=tcp:"""
        + str(database_server_name)
        + """.database.windows.net,1433;
                        Database="""
        + str(database_name)
        + """;
                        UID="""
        + str(user_name)
        + """;
                        PWD="""
        + str(user_password)
        + """;
                        Encrypt=yes;TrustServerCertificate=no;Connection Timeout=-1"""
    )
    return pyodbc.connect(connection_string)
