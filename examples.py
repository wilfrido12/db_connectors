from db_connectors import Connects

username = ''
password = ''
query = ''

# ORACLE Example
connects = Connects(username, password, query)
df = connects.to_oracle().head(10)
print(df)

# EXASOL Example
# Changes Attributes before creating object
Connects.exa_schema = ''
Connects.exa_dsn = ''
connects = Connects(username, password, query)
df = connects.to_exasol().head(10)
print(df)

# SPLUNK Example
# Changes Attributes before creating object
Connects.sp_earliest = ''
Connects.sp_latest = ''
Connects.sp_host = ''
connects = Connects(username, password, query)
df = connects.to_splunk().head(10)
print(df)

# CASSANDRA Example
# Changes Attributes before creating object
Connects.cass_cluster = []
Connects.cass_namespace = ''
connects = Connects(username, password, query)
df = connects.to_cassandra().head(10)
print(df)

# NEO4J Example
# Changes Attributes before creating object
Connects.neo_host = ''
connects = Connects(username, password, query)
df = connects.to_neo4j().head(10)
print(df)
