import psycopg2

connection = psycopg2.connect(
    host='ec2-23-21-229-200.compute-1.amazonaws.com',
    database='d80m409qj3pu8s',
    user='jffyzilbdtfxua',
    password='f7789ebaf7eea860725062241d3677b0030a61e772e6421fa71e1876b82fa22b')

cursor = connection.cursor()
cursor.execute("SELECT * FROM USERS")
print("Result ", cursor.fetchall())