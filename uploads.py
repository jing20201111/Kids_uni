import db
import pandas as pd
import getid
import classes
import member_info
import volun_info
import destinations

def add_index(fun):
    def inner(*args,**kwargs):
        df = fun(*args,**kwargs)
        df.fillna('',inplace=True)
        df.loc[:,'index'] = df.index
        return df
    return inner




    
def mem_obj(l=[]):
    mem_obj = member_info.members(l)
    school_id = getid.get_schoolid(mem_obj.school)
    mem_obj.school = school_id
    cur = db.getCursor()
    cur.execute("SELECT * FROM members WHERE member_id = %s",(mem_obj.id,))
    result =cur.fetchone()
    if not result:
        mem_obj.id = int(getid.get_memid())
    return mem_obj
# obj = mem_obj('aaaaaaaaaaaaaaaaaaaaaaaa')
# print(obj.school)

# use pandas to read excel file and get data
def get_mem_df(excelpath):
    df_school = pd.read_excel(excelpath,0,header=None,nrows=5,dtype = str)
    df_school.dropna(axis='columns',how='all',inplace=True)
    df_school.fillna('', inplace=True)
    name = df_school.loc[0,3]
    df_mem = pd.read_excel(excelpath,0,header=[5],dtype = {"#":str,"Age":str})
    df_mem.update(df_mem.iloc[:,14:20].fillna(0)) 
    df_mem.iloc[:,14:20] = df_mem.iloc[:,14:20].astype(float)
    df_mem.dropna(axis = 0, how='all', subset=['First Name','Last Name','Age'],inplace=True)
    df_mem.dropna(axis='columns',how='all',inplace=True)
    df_mem.fillna('', inplace=True)
    df_up = pd.read_excel(excelpath,1,header=[5])
    if len(df_mem) != len(df_up):
        for i in range(0,len(df_mem)-len(df_up)):
            df_up.loc[len(df_up)]=[None]*4
    df_mem.insert(14,'USERNAME',df_up['USERNAME'].values)
    df_mem.insert(15,'PASSWORD',df_up['PASSWORD'].values)
    df_mem.insert(16,'School name',name)
    df_mem.loc[:,'index'] = df_mem.index
    df_coor = pd.read_excel(excelpath,1,header=[1],nrows=1,dtype=str)
    df_coor.dropna(axis='columns',how='all',inplace=True)
    df_coor[['School', 'Email','Phone','year']] = pd.DataFrame([[
            df_school.loc[0,3], 
            df_school.loc[2,3], 
            df_school.loc[3,3],
            df_school.loc[4,3]]], index=df_coor.index)
    
    return [df_mem,df_coor]

#  insert info of coordinator into database
def insert_coor(l=[]):
    cur = db.getCursor()
    school_id = getid.get_schoolid(l[4])

    sql = "INSERT INTO coordinator VALUES(%s, '%s', '%s','%s','%s','%s') ON CONFLICT \
        (school_id) DO UPDATE SET school_id = EXCLUDED.school_id, name = EXCLUDED.name, \
        email = EXCLUDED.email, phone_number = EXCLUDED.phone_number, username = EXCLUDED.username,\
        password = EXCLUDED.password;"%(school_id,l[0],l[5],l[6],l[2],l[3])
    cur.execute(sql)




def dest_obj(l=[]):
    dest_obj = destinations.destination(l)
    sql = "SELECT * FROM destinations WHERE ld_id = %s" % int(dest_obj.id)
    cur = db.getCursor()
    cur.execute(sql)
    result = cur.fetchone()
    if not result:
        dest_obj.id = int(getid.get_dest_id())
    return dest_obj

@add_index
def get_dest_df(excelpath):
    df_des = pd.read_excel(excelpath,0,header=[1],dtype = str)
    df_des.dropna(axis = 0, how='all', inplace=True)
    df_des.update(df_des.iloc[:,15:19].fillna('No'))
    df_des.update(df_des.iloc[:,20:].fillna('No'))
    return df_des




def volun_obj(l=[]):
    volun_obj = volun_info.volunteer(l)
    sql = "SELECT * FROM volunteers WHERE volun_id = %s" % int(volun_obj.id)
    cur = db.getCursor()
    cur.execute(sql)
    result = cur.fetchone()
    if not result:
        volun_obj.id = int(getid.get_volun_id())
    return volun_obj    

@add_index
def get_volun_df(excelpath):

    typedict = {"ID":str,
                "Student ID":str,
                "Mobile number":str, 
                "Emergency contact person - Mobile number":str,
                "Referee one - Phone number":str,
                "Referee two - Phone number":str}
    df_volun = pd.read_excel(excelpath,0, dtype=str)
    df_hours = pd.read_excel(excelpath,1,header=[4])
    df_joined = pd.concat([df_volun,df_hours.iloc[:,5:]],axis=1)

    df_joined.dropna(axis = 0, how='all', inplace=True)
    df_joined.update(df_joined.iloc[:,[4,14,15,17]].fillna('No'))
    df_joined.update(df_joined.iloc[:,38:].fillna('0')) 
    return df_joined
    




