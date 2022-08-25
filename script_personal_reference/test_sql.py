import models as models
from sqlalchemy import select
with models.engine.connect():
    column = models.session.execute("Select hostname from hostname_table")
    # query with ORM columns
    statement = select(models.HostnameClass.hostname)

# list of tuples
    result = models.session.execute(statement).all()
    print(result[4])
