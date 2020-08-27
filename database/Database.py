import psycopg2
from database.config import config
import os
import time



def registerOP(**info):
    """ Register user in database """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        # insert user to database
        try:
            queryCode = """insert into users(email, FirstName, LastName, password, phone, created_at, updated_at, user_type, regester_type, doctor_id) 
                    values(%s, %s, %s, %s, %s, now(), now(), %s, %s, %s)"""

            cur.execute(queryCode, (info['email'], info['FirstName'], info['LastName'], info['password'], info['phone'], info['user_type'], info['regester_type'], info['doctor_id']))
            conn.commit()
            cur.close()
            return 1
        except:
            cur.close()
            print("user has been registered before")
            return 0

	    # close the communication with the PostgreSQL
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1
        
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
def registerD(**info):
    """ Register user in database """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        cur.execute("select email from users where email=%s", (info['email'], ))
        
        # insert user to database if there is no user with this info
        if not cur.fetchone():
            queryCode = """insert into notverified(email, FirstName, LastName, password, phone, created_at, updated_at, user_type, regester_type, doctor_id) 
                    values(%s, %s, %s, %s, %s, now(), now(), %s, %s, %s)"""

            cur.execute(queryCode, (info['email'], info['FirstName'], info['LastName'], info['password'], info['phone'], 'Doctor', info['regester_type'], info['doctor_id']))
            conn.commit()
        else:
            print("you have been registered before")

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def userExist(email= None, password= None):
    """ Check exist user in database """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        cur.execute("select email, password from users where email=%s AND password= %s", (email, password, ))

        if cur.fetchone():
            cur.close()
            print("True")
            return 1
        else:
            cur.close()
            print("False")
            return 0


    except (Exception, psycopg2.DatabaseError) as error:
        return -1
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def doctorRegisterDone(email= None):
    """ save doctors in users database """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        
        # insert user to database if there is no user with this info
        queryCodeInsert = """insert into users(email, FirstName, LastName, password, phone, created_at, updated_at, user_type, regester_type, doctor_id) 
                select email, FirstName, LastName, password, phone, created_at, updated_at, user_type, regester_type, doctor_id from notverified
                where email=%s"""

        cur.execute(queryCodeInsert, (email, ))
        conn.commit()

        # remove doctor from not verified
        queryCodeRemove = """delete from notverified where email=%s"""

        cur.execute(queryCodeRemove, (email, ))
        conn.commit()


	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    


def changePass(new_Pass= None, email= None):
    """ Change password of user """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        # change password query code
        queryCode = """UPDATE users set password= %s, updated_at= now() 
                        where email= %s"""

        cur.execute(queryCode, (new_Pass, email))


        conn.commit()

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def deleteAccount(email= None):
    """ Delete user """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()


        # change password query code
        queryCode = """DELETE from users 
                        where email= %s"""

        cur.execute(queryCode, (email, ))

        conn.commit()

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def writeImage(imgPath= None, email= None):
    """ Save image in img table of database """
    conn = None
    try:
        # read data from a picture
        pic = open(imgPath, 'rb').read()
        format_pic = (imgPath.split("/")[-1].split("."))[-1]

        # read database configuration
        params = config()

        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)

        # create a new cursor object
        cur = conn.cursor()

        # find id of user
        cur.execute("select id from users where email= %s", (email, ))
        _id = cur.fetchone()[0]

        queryCode = """insert into img(owner_id, data_pic, format_pic, upload_at) 
                        values(%s, %s, %s, now())"""
        cur.execute(queryCode, (_id, psycopg2.Binary(pic), format_pic, ))

        conn.commit()

        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def readImage(email= None, pathToSave= None):
    """ read images from database """
    conn = None
    try:
        # read database configuration
        params = config()

        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)

        # create a new cursor object
        cur = conn.cursor()

        # find id of user
        cur.execute("select id from users where email= %s", (email, ))
        owner_id = cur.fetchone()[0]

        # execute the SELECT statement
        cur.execute(""" SELECT data_pic, upload_at, format_pic
                        FROM img
                        WHERE img.owner_id = %s """,
                    (owner_id,))

        imgs = cur.fetchall()
        for img in imgs:
            open(os.path.join(pathToSave, str(img[1]) + '.' + img[2]), 'wb').write(img[0])
        # close the communication with the PostgresQL database
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == "__main__":
    info = {}
    info['email'] = 'mahdi.sabour@aut.ac.ir'
    # info['FirstName'] = 'mahdi'
    # info['LastName'] = 'sabour'
    info['password'] = 'testpass'
    # info['phone'] = '09145178976'
    # # info['user_type'] = 'Ordinary person'
    # info['regester_type'] = 'App'
    # info['doctor_id'] = "9623070"
    # registerD(**info)  
    # doctorRegisterDone(email= 'mahdi.sabour@aut.ac.ir')
    # changePass(new_Pass= 'newPass2', email= 'mahdi.sabo@aut.ac.ir')
    # deleteAccount(email= 'mahdi.sabo@aut.ac.ir')
    # writeImage(email='mahdi.sabour@aut.ac.ir', imgPath= "test.png")
    # readImage(email='mahdi.sabour@aut.ac.ir', pathToSave= os.getcwd())
    userExist(email=info['email'], password= info['password'])