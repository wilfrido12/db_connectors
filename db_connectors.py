"""
DB Connectors
=============

A class containing the connectors to the different data sources we use, more can be added in the future as we needed or
the ones we have can be modified easily

It connects to:

- CASSANDRA
- EXASOL
- ORACLE
- SPLUNK
- NEO4J (Test pending)

They all take three main arguments:

- Username
- Password
- Query

With the exception of EXASOL and SPLUNK which take additional arguments passed inside the class as attributes,
they need to be change before creating the object.

"""

import neo4j
import pyexasol
import pandas as pd
import cx_Oracle as co
from datetime import datetime
import splunklib.client as client
import splunklib.results as results
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class Connects(object):
    """Class Connects
       --------------

       The Class contains the attributes and elements necessary
       to build the object and connect to different sources listed above"""

    def __init__(self, username, password, query):
        self.username = username
        self.password = password
        self.query = query

    ora_host = ''
    ora_service = ''

    def to_oracle(self):
        """This uses cx_Oracle to connect. Returns a pandas data frame as a result."""

        ora_config = {
            'host': Connects.ora_host,
            'port': 1521,
            'user': self.username,
            'psw': self.password,
            'service': Connects.ora_service
        }

        # Oracle connection
        constr = '{user}/{psw}@{host}:{port}/{service}'.format(**ora_config)
        conn = co.connect(constr)
        cursor = conn.cursor()

        # Optional
        cursor.execute("ALTER SESSION SET OPTIMIZER_FEATURES_ENABLE='12.1.0.1'")

        # Reads sql to dataframe, uses -conn
        results = pd.read_sql(self.query, conn)
        return results

    exa_schema = ''
    exa_dsn = ''

    def to_exasol(self):
        """This function uses pyexasol to connect, also uses the exa_schema attribute that needs to be specified
        before creating the object. Return a pandas data frame as a result.
        """

        C = pyexasol.connect(dsn=Connects.exa_dsn, user=self.username, password=self.password,
                             schema=Connects.exa_schema,compression=True)

        results = C.export_to_pandas(self.query)
        return results

    sp_host = ''
    sp_earliest = ''
    sp_latest = ''

    def to_splunk(self):
        """This function uses splunklib to connect, and uses the sp_earliest, sp_latest and sp_region which needs to be
        speficied before creating the object. Returns a splunk results object as a result that needs to be looped through
        """

        # The region comes from the Class Attributes, needs to be assigned before creating the object
        service = client.connect(
            host=Connects.sp_host,
            port='8089',
            username=self.username,
            password=self.password
        )

        jobs = service.jobs

        kwargs_query = {'earliest_time': Connects.sp_earliest,
                        'latest_time': Connects.sp_latest,
                        'search_mode': 'normal',
                        'count': 0}

        search_query = service.jobs.oneshot(self.query, **kwargs_query)

        reader = results.ResultsReader(search_query)

        return reader

    neo_host = ''

# Test the neo4j connector
    def to_neo4j(self):
        """This uses the neo4j library. Needs to be tested
        """
        # Unix timestamp, can't remember what is this for
        def regdate(string):
            date = string / 1000.0
            return datetime.fromtimestamp(date).strftime('%d-%m-%Y %H:%M:%S')

        # NEO4J connection
        connection = neo4j.connect(Connects.neo_host, self.username, self.password)
        cursor = connection.cursor()

        result = cursor.execute(self.query)
        return result

    cass_cluster = []
    cass_namespace = ''

    def to_cassandra(self):
        """This uses cassandra-driver library to connect. Returns a iterable object with the results.
        """

        # Connection credentials
        auth = PlainTextAuthProvider(username=self.username, password=self.password)
        cluster = Cluster(Connects.cass_cluster,
                          auth_provider=auth, port=9042)

        # Change the namespace if needed
        session = cluster.connect(Connects.cass_namespace)

        # Execution of the query and results
        results = session.execute(self.query)
        return results







