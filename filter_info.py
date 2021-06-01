import db
import classes
from flask import request

volun_criteria_dict= {
        'Status':['status','volun_detail'],
        'Induction':['induction','volun_detail'],
        'Interview':['interview','volun_detail'],
        'Gender':['gender','volun_detail'],
        'Volunteer Experience':['experience','volun_detail'],
        'Future Leader':['future_leader','volun_detail'],
        'Police Check':['police_check','volun_detail'],
        'University':['studying_uni','volun_detail'],
        'Course':['course','volun_detail'],
        'Current Year':['current_year','volun_detail'],
        'Completion Date':['completion_date','volun_detail']
        }

def get_criteria(d={}):
    cur = db.getCursor()
    criteria = {}
    for i in d.keys():
        cur.execute(f"SELECT DISTINCT {d[i][0]} FROM {d[i][1]} WHERE {d[i][0]} IS NOT null;")
        results = cur.fetchall()
        value_list = []
        if len(results) > 1:
            for j in results:
                value_list.append(j) if j != None else False
        else:
            value_list =[results[0][0]] if results != None else []
        criteria.setdefault(i,value_list)
    return criteria

def get_display_list(results,target_class):
    lists = []
    for i in results:
        target = list(i)
        obj = target_class(target)
        lists.append(obj)
    return lists

def get_sql(table, order,criteria_idct = {}):
    form = request.form.to_dict()
    query = ''
    count = 0
    for i in form.keys():
        column = criteria_idct[i][0]
        values = request.form.getlist(i)
        for j in range(0,len(values)):
            if count == 0 and j == 0:
                query += f"{column} = '{values[j]}'"
            elif j == 0:
                query += f" AND {column} = '{values[j]}'"
            else:
                query += f" OR {column} = '{values[j]}'"
        count += 1

        sql = f'SELECT * FROM {table} WHERE {query} ORDER BY {order};'
    return sql


