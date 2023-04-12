def handler(event, context):
    print("INSIDE HANDLER")
    import json
    from sqlalchemy import create_engine, text
    host = 'database-1.c0kpxltmifsg.us-east-1.rds.amazonaws.com'
    port = 5432
    username = 'postgres'
    password = 'shukhapriya'
    database = 'image_predictions'
    engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (username, password, host, port, database))
    conn = engine.connect()
    print("After connecting")
    upload_query = "INSERT INTO predictions (image_url, image_class) VALUES ('s3://3.png', 'eagle');"
    print("defined upload query")
    conn.execute(text(upload_query))
    query = 'SELECT image_class FROM predictions'
    print('QUERY EXECUTED')
    query = 'SELECT image_class FROM predictions'
    result = conn.execute(text(query)).fetchall()
    print("result is: ", result)
    conn.commit()
    conn.close()
    print("CLOSING CONNECTION")
    return "Successful"

if __name__ == "__main__":
    handler(1, 1)