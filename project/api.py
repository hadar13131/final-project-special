# api.py
import json
import sqlite3
import hashlib
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Table, Column, create_engine, MetaData, String, Boolean, INTEGER, JSON, update, DateTime
from sqlalchemy.orm.session import sessionmaker
from project.models import Set, Exercise
from datetime import datetime

app = FastAPI(docs_url="/")

engine = create_engine("sqlite:///./PowerAppDatabase.db")

md = MetaData()

Session = sessionmaker(bind=engine)

# create table to save users information
user_table = Table(
    "users_tb", md,
    Column("name", String, primary_key=True),
    Column("password", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("phone_num", String),
    Column("email", String),
    Column("age", INTEGER),
    Column("gender", String),
    Column("goals", String),
    Column("public", Boolean)
)

md.create_all(engine)

# create table to save workouts information
workout_table = Table(
    "workouts", md,
    Column("workoutid", INTEGER, primary_key=True),
    Column("userid", String),
    Column("workout_name", String),
    Column("date", DateTime),
    Column("exerciselist", JSON)
)

md.create_all(engine)


#create table to save users massages
shared_workout_table = Table(
    "share_workout_tb", md,
    Column("msgid", INTEGER, primary_key=True),
    Column("userid", String),
    Column("workoutid", INTEGER)
)

md.create_all(engine)

# to hash the password
# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()


@app.get("/lst_of_workouts_by_username")
def lst_of_workouts_by_username(userid: str) -> dict[str, list[tuple]]:
    session = Session()
    # find = []
    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()
    # return find
    # return json.dumps(find)
    return {"response": find}


@app.get("/lst_of_exercise_names")
def lst_of_exercise_names(userid: str):
    session = Session()
    find = session.query(workout_table).filter(
        workout_table.c.userid == userid).all()  # filter by userid, get lst of workouts
    lst = []
    for f in find:
        n = f[4]
        for i in n:
            n2 = json.loads(i)
            lst.append(n2["name"])
    # return lst
    lst2 = set(lst)
    return {"response": lst2}


@app.get("/find_first_name")
def find_first_name(userid: str) -> dict[str, str]:
    session = Session()
    find = session.query(user_table).filter(user_table.c.name == userid).first()
    # return {"response": "find_first_name success"}
    return {"response": str(find[2])}
    # return find[2]


@app.get("/signup")
def signup(name: str, password: str) -> dict[str, str]:
    session = Session()

    # check if the username is available  - every user should have different username
    if session.query(user_table).filter_by(name=name).first():
        return {"response": "the username not valid"}

    session.execute(
        user_table.insert().values(
            name=name, password=password,
            first_name="",
            last_name="",
            phone_num="",
            email="",
            age="",
            gender="",
            goals="",
            public=False
        )
    )
    session.commit()

    return {"response": "signup success"}


# end signup

@app.get("/fill_info")
def fill_info(name: str, first_name: str, last_name: str, phone_num: str, email: str, age: int, gender: str,
              goals: str) -> dict[str, str]:
    session = Session()
    # if session.query(user_table).filter_by(name=name).first():
    # find = session.query(user_table).filter_by(name=username).first()

    find = session.query(user_table).filter(user_table.c.name == name).first()

    if find is not None:
        stmt = update(user_table).where(user_table.c.name == name).values(
            first_name=first_name,
            last_name=last_name,
            phone_num=phone_num,
            email=email,
            age=age,
            gender=gender,
            goals=goals,
            public=False
        )

        session.execute(stmt)

        session.commit()
        return {"response": "the information added"}

    return {"response": "the user doesnt exist"}


@app.get("/signout")
def signout(name: str, password: str) -> dict[str, str]:
    session = Session()

    users = session.execute(user_table.select())

    password_hash = password

    for user in users:
        # Check if the username and password match
        if user.name == name and user.password == password_hash:
            return {"response": "the details are correct"}

    return {"response": "the details are not match"}


# end signuout


@app.get("/delete")
def delete(name: str, password: str) -> dict[str, str]:
    session = Session()

    users = session.execute(user_table.select())

    password_hash = password

    for user in users:
        # Check if the username and password match
        if user.name == name and user.password == password_hash:
            session.execute(
                user_table.delete().where(
                    user_table.c.name == name and
                    user_table.c.password == password_hash
                )
            )

            session.commit()

            #delete the all user shared workouts in the table of the shared workouts
            response = delete_shared_workouts(chosed_user=name)

            find = session.query(workout_table).filter(workout_table.c.userid == name).all()
            for workuot in find: #delete all of his workouts
                session.execute(
                    workout_table.delete().where(
                        workout_table.c.workoutid == workuot[0]
                    )
                )

            session.commit()

            return {"response": "delete success"}

    return {"response": "user data not found"}


# end delete


@app.get("/authenticate")
def authenticate(name: str, password: str) -> dict[str, str]:
    session = Session()

    users = session.execute(user_table.select())
    password_hash = password

    for user in users:
        # Check if the username and password match
        if user.name == name and user.password == password_hash:
            return {"response": "user authenticated"}

    return {"response": "user data not found"}


# end authenticate

@app.get("/authenticate2")
def authenticate2(email: str, name: str, password: str) -> dict[str, str]:
    session = Session()

    users = session.execute(user_table.select())
    password_hash = password

    for user in users:
        # Check if the username and password match
        if user.name == name and user.password == password_hash:

            if user.email != email:
                return {"response": "the email doesnt match your user name"}

            else:
                return {"response": "user authenticated"}

    return {"response": "user data not found"}


# end authenticate2

@app.get("/check_email")
def check_email(email: str) -> dict[str, str]:
    session = Session()

    users = session.execute(user_table.select())

    for user in users:
        # Check if the email is existing - email should be unique
        if user.email == email:
            return {"response": "the email not valid, try to login"}

    return {"response": "the email is valid"}


# end check_email


@app.get("/addworkout")
def addworkout(userid: str, workout_name: str, date: datetime, exerciselist: str = None):
    session = Session()

    # at the beginning only the name and the date of the workout insert to the table

    if exerciselist != "":
        session.execute(
            workout_table.insert().values(
                userid=userid,
                workout_name=workout_name,
                date=date,
                exerciselist=[exerciselist]
            )
        )
        session.commit()

    else:
        session.execute(
            workout_table.insert().values(
                userid=userid,
                workout_name=workout_name,
                date=date,
                exerciselist=""
            )
        )
        session.commit()

    return {"response": "the workout added"}


@app.get("/deleteworkout")
def deleteworkout(userid: str, workout_name: str, date: datetime):
    session = Session()
    # all the workouts of the user
    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()

    # all the shared workout of the user
    lst_shared_workouts = bring_shared_workoutid(chosed_user=userid)["response"]

    # going over the lst
    for f in find:
        if date == f[3] and workout_name == f[2]: #if the date match the workout name
            for i in lst_shared_workouts: #going over the shared workouts
                if f[0] == i: #if the workout id of the workout equal to the workout id of the shared workoout

                    # delete from shared workout table
                    session.execute(
                        shared_workout_table.delete().where(
                            shared_workout_table.c.workoutid == i
                        )
                    )
                    session.commit()

            # delete from the full workout table
            session.execute(
                workout_table.delete().where(
                    workout_table.c.workout_name == workout_name and workout_table.c.date == date
                )
            )

            session.commit()

            return {"response": "delete success"}

    return {"response": "workout data not found"}


@app.get("/updateworkout")
def updateworkout(userid: str, workout_name: str, date: datetime, new_workout_name, new_date):
    session = Session()

    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()

    for f in find:
        if date == f[3] and workout_name == f[2]:
            workoutid1 = f[0]

            # if the user sent to change the workout name and the date
            if new_workout_name != "" and new_date != "":
                date1 = datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S')
                stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(
                    workout_name=new_workout_name, date=date1
                )
                session.execute(stmt)
                session.commit()
                return {"response": "update success"}

            # if the user sent only change of date
            elif new_workout_name == "" and new_date != "":
                date1 = datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S')
                stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(date=date1)
                session.execute(stmt)
                session.commit()
                return {"response": "update success"}

            # if the user sent only change of workout name
            elif new_workout_name != "" and new_date == "":
                stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(
                    workout_name=new_workout_name)

                session.execute(stmt)
                session.commit()

                return {"response": "update success"}

    return {"response": "nothing changed"}


@app.get("/addexercisetoworkout")
def addexercisetoworkout(userid: str, date: str, workout_name: str, exercise):
    session = Session()
    # find the all workouts of the user
    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()

    workout = find[0]

    # going over the list
    for f in find:
        #from datetime to string
        date1 = f[3]
        date2 = date1.strftime('%Y-%m-%d')
        if str(date1) == date: #if the dates match
            if f[2] == workout_name: #if the workout name match
                workout = f

    workoutid1 = workout[0]
    exercise1 = workout[4]

    exercise3 = []

    # if there are exercises the new exercise insert to the current list
    if exercise1 != "":
        exercise3 = exercise1
        exercise3.append(exercise)

    # if the list of the exercises is empty
    else:
        exercise3 = [exercise]

    stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(exerciselist=exercise3)
    session.execute(stmt)
    session.commit()
    return {"response": "the exercise added"}


@app.get("/deletexercisefromworkout")
def deletexercisefromworkout(userid: str, date: datetime, workout_name: str, exercise_name: str):
    session = Session()

    # find the all workouts of the user
    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()
    workoutid1 = find[0][0]
    workout = find[0]

    sign = False

    for f in find:
        # if the date and the workout name match
        if date == f[3] and workout_name == f[2]:
            workoutid1 = f[0]
            workout = f
            sign = True #this means the workout exist
            break

    exercise_lst = workout[4]
    # if the workout exists
    if sign:
        #going over the exercise list
        for e in exercise_lst:
            exercise = json.loads(e) #from string to dict
            if exercise["name"] == exercise_name: #if the name of the exercises match
                exercise_lst.remove(e) #remove the exercise from the list
                # update the exercise list in the table to the update list (after the remove)
                stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(exerciselist=exercise_lst)
                session.execute(stmt)
                session.commit()
                return {"response": "delete success"}

    return {"response": "the exercise data exists"}

@app.get("/updateexercise")
def updateexercise(userid: str, workout_name: str, date: datetime, exercise_name, power, new_exercise_name, new_power):
    session = Session()

    # find the all workouts of the user
    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()
    workoutid1 = find[0][0]
    workout= find[0]

    for f in find:
        if date == f[3] and workout_name == f[2]:
            workoutid1 = f[0]
            workout = f
            break

    exercise_lst = workout[4] #the exercise list - (list[str])

    # the sets in the list - the exercise turn from string to dict - the "sets" key bring dict value
    sets = json.loads(exercise_lst[0])["sets"]

    for e in exercise_lst:
        exercise = json.loads(e) #from string to dict
        if exercise["name"] == exercise_name: #there is no two exercises with the same name.
            sets = exercise["sets"] #save the list of the sest of the exercise
            exercise_lst.remove(e) #remove the exercise which need to be edit
            break

    obj_set_lst = []
    # to be able to create a new exercise, the sets should be in object format
    for i in sets:
        obj_set_lst.append(Set.load(i))

    if new_exercise_name != "" and new_power != "":
        new_exec = Exercise(name=new_exercise_name, power=new_power, sets=obj_set_lst)
        new_exec2 = json.dumps(new_exec.dump())
        exercise_lst.append(new_exec2)
        stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(
            exerciselist=exercise_lst)
        session.execute(stmt)
        session.commit()
        return {"response": "update success"}

    elif new_exercise_name == "" and new_power != "":
        new_exec = Exercise(name=exercise_name, power=new_power, sets=obj_set_lst)
        new_exec2 = json.dumps(new_exec.dump())
        exercise_lst.append(new_exec2)
        stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(
            exerciselist=exercise_lst)
        session.execute(stmt)
        session.commit()
        return {"response": "update success"}

    elif new_exercise_name != "" and new_power == "":
        new_exec = Exercise(name=new_exercise_name, power=power, sets=obj_set_lst)
        new_exec2 = json.dumps(new_exec.dump())
        exercise_lst.append(new_exec2)
        stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(
            exerciselist=exercise_lst)
        session.execute(stmt)
        session.commit()
        return {"response": "update success"}

    return {"response": "nothing changed"}

@app.get("/addsettoexercise2")
def addsettoexercise2(userid: str, date: str, workout_name: str, exercise_name: str, power: str, sets):
    session = Session()

    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()
    exec = find[0][4]  # the lst of exer of the first workout
    workoutid1 = find[0][0]  # the workout id of the first workout

    for f in find: #going over the workout list
        date1 = f[3]
        date2 = date1.strftime('%Y-%m-%d')
        if str(date1) == date:
            if f[2] == workout_name: #if the exercise name match
                exec = f[4] # list of str
                workoutid1 = f[0]
                break

    exercise2 = exercise_name
    ex = json.loads(exec[0]) #list of dict
    set1 = ex["sets"] #list of dict
    for e in exec:
        e1 = json.loads(e) #from str to dict
        if exercise2 == e1["name"]: #if the exercise name match
            set1 = e1["sets"]
            exec.remove(e) #remove the sets list from the exercise
            break
    s = json.loads(sets) # from str to dict

    set1.append(s) #insert to the list if sets, the new set
    set_lst = []#new set of objects- in this way I can create new Exercise object
    for s1 in set1:
        w = Set(repetitions=int(s1["repetitions"]), time=int(s1["time"]), weight=float(s1["weight"]),
                distance_KM=float(s1["distance_KM"]))
        set_lst.append(w)

    new_exec = Exercise(name=exercise2, power=power, sets=set_lst) #new exercise object
    new_exec2 = json.dumps(new_exec.dump()) #from object to str
    exec.append(new_exec2) #add to the list of exercises
    stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(exerciselist=exec) #update the exercise list
    session.execute(stmt)
    session.commit()
    return {"response": "the set added"}

@app.get("/deletesetfromexercise")
def deletesetfromexercise(userid: str, date: datetime, workout_name: str, exercise_name: str, sets_index: int):
    session = Session()

    find = session.query(workout_table).filter(workout_table.c.userid == userid, workout_table.c.date == date).all()
    exec_lst = find[0][4]  # the lst of exer of the first workout
    workoutid1 = find[0][0]  # the workout id of the first workout

    for f in find:
        if f[2] == workout_name:  # find the specific workout by name
            exec_lst = f[4]  # save the exercise list
            workoutid1 = f[0]
            break

    exercise = json.loads(exec_lst[0])

    for e1 in exec_lst:  # go over the exercises
        e = json.loads(e1)
        if e["name"] == exercise_name:  # find the specific exercise by name
            exercise = e  # save the exercise
            break

    chosen_set = exercise["sets"][sets_index]  # save the specific set in the exercise by index
    exercise["sets"].remove(chosen_set)  # delete the set from the exercise sets
    n = 0
    for i in exec_lst:  # go over the exercises
        e = json.loads(i)
        if e["name"] == exercise_name:  # find the specific exercise by name
            # i = json.dumps(exercise) #change the specific exercise
            exec_lst[n] = json.dumps(exercise)
            break
        else:
            n = n + 1

    # str_exer_lst = json.dumps(exec_lst) #from dict to string

    stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(exerciselist=exec_lst)
    session.execute(stmt)
    session.commit()
    return {"response": "the set deleted"}


@app.get("/updatesetinexercise")
def updatesetinexercise(userid: str, date: datetime, workout_name: str, exercise_name: str, sets_index: int,
                        updated_set):
    session = Session()

    find = session.query(workout_table).filter(workout_table.c.userid == userid, workout_table.c.date == date).all()
    exec_lst = find[0][4]  # the lst of exer of the first workout
    workoutid1 = find[0][0]  # the workout id of the first workout

    for f in find:
        if f[2] == workout_name:  # find the specific workout by name
            exec_lst = f[4]  # save the exercise list
            workoutid1 = f[0]
            break

    exercise = json.loads(exec_lst[0])

    for e1 in exec_lst:  # go over the exercises
        e = json.loads(e1)
        if e["name"] == exercise_name:  # find the specific exercise by name
            exercise = e  # save the exercise
            break

    exercise["sets"][sets_index] = json.loads(updated_set)

    n = 0
    for i in exec_lst:  # go over the exercises
        e = json.loads(i)
        if e["name"] == exercise_name:  # find the specific exercise by name
            # i = json.dumps(exercise) #change the specific exercise
            exec_lst[n] = json.dumps(exercise)
            break
        else:
            n = n + 1

    # str_exer_lst = json.dumps(exec_lst) #from dict to string

    stmt = update(workout_table).where(workout_table.c.workoutid == workoutid1).values(exerciselist=exec_lst)
    session.execute(stmt)
    session.commit()
    return {"response": "the set updated"}


# @app.get("/showimprovement")
# def showimprovement(userid: str, exercise_name: str, s_date: datetime, e_date: datetime):
#     session = Session()
#     exec_lst = []
#     find = session.query(workout_table).filter(
#         workout_table.c.userid == userid).all()  # filter by userid, get lst of workouts
#
#     for f in find:  # going through the workouts
#         if f[3] > s_date and f[3] < e_date:  # check if its in the right date
#             l = f[4]  # get the list of exercises
#             for l2 in l:  # going through the exercises
#                 l3 = json.loads(l2)  # from string to dict
#                 if l3["name"] == exercise_name:  # check if there is the exercise the user want
#                     exec_lst.append(f)  # add to lst the all workout
#                     break
#
#     repete = 0
#     time = 0
#     weight = 0
#     distance_KM = 0
#     n = 0
#
#     for e in exec_lst:  # going through the full workout
#         e2 = e[4]  # take the list of exercises
#         for j in e2:  # going through the exercises list
#             e3 = json.loads(j)  # change the str to dict
#             e3 = e3["sets"]  # find the value of the "sets" key
#             for i in e3:  # going through the lst of sets
#                 repete += i["repetitions"]
#                 time += int(i["time"])
#                 weight += int(i["weight"])
#                 distance_KM += int(i["distance_KM"])
#                 n = n + 1  # counter
#
#     # find the avg
#     if n != 0:
#         repete = repete / n
#         time = time / n
#         weight = weight / n
#         distance_KM = distance_KM / n
#
#         return {"count_sets": n, "repete": repete, "time": time, "weight": weight, "distance_KM": distance_KM}
#
#     else:
#         return {"count_sets": 0, "repete": 0, "time": 0, "weight": 0, "distance_KM": 0}


# its the Graph of the all parameters-
# get userid, exercise name, start date, end date
# return dict of the avg of each parameter in all the sets the user did at this time
@app.get("/showimprovement2")
def showimprovement2(userid: str, exercise_name: str, s_date: datetime, e_date: datetime):
    session = Session()
    exec_lst = []
    find = session.query(workout_table).filter(
        workout_table.c.userid == userid).all()  # filter by userid, get lst of workouts

    for f in find:  # going through the workouts
        if f[3] > s_date and f[3] < e_date:  # check if its in the right date
            l = f[4]  # get the list of exercises
            for l2 in l:  # going through the exercises
                l3 = json.loads(l2)  # from string to dict
                if l3["name"] == exercise_name:  # check if there is the exercise the user want
                    exec_lst.append(f)  # add to lst the all workout
                    break

    repete = 0
    time = 0
    weight = 0
    distance_KM = 0
    n = 0

    for e in exec_lst:  # going through the full workout
        e2 = e[4]  # take the list of exercises
        for j in e2:  # going through the exercises list
            e3 = json.loads(j)  # change the str to dict
            if e3["name"] == exercise_name:
                e3 = e3["sets"]  # find the value of the "sets" key
                for i in e3:  # going through the lst of sets

                    # the improvement of the time should be by 1 KM

                    if int(i["distance_KM"]) != 0:
                        time += (int(i["time"]) / i["distance_KM"])
                        distance_KM += int(i["distance_KM"])

                    else:
                        time += int(i["time"])
                        distance_KM += int(i["distance_KM"])

                    weight += int(i["weight"])
                    repete += i["repetitions"]

                    n = n + 1  # counter

    # find the avg
    if n != 0:
        repete = repete / n
        time = time / n
        weight = weight / n
        distance_KM = distance_KM / n

        return {"count_sets": n, "repete": repete, "time": time, "weight": weight, "distance_KM": distance_KM}

    else:
        return {"count_sets": 0, "repete": 0, "time": 0, "weight": 0, "distance_KM": 0}


def return_the_avg(sets, name: str) -> int:  # if the name is count_sets, its return the number of sets

    count = 0
    n = 0

    for i in sets:  # going through the lst of sets
        if name != "count_sets":
            count += i[name]
        n = n + 1  # counter

    if name == "count_sets":
        return n

    if n != 0:
        count1 = count / n
        return count1

    else:
        return 0


# its the Graph of the single parameters
# get userid, exercise name, start date, end date
# return dict of list, in each list there is avgs of the sets - each workout is different avg
@app.get("/improve_with_params2")
def improve_with_params2(userid: str, exercise_name: str, s_date: datetime, e_date: datetime):
    session = Session()
    workouts_lst = []
    find = session.query(workout_table).filter(
        workout_table.c.userid == userid).all()  # filter by userid, get lst of workouts

    full_workout_l = []
    dates_l = []
    count_sets_l = []
    repetitions_avg_l = []
    time_avg_l = []
    weight_avg_l = []
    distance_KM_avg_l = []

    for f in find:  # going through the workouts
        if f[3] > s_date and f[3] < e_date:  # check if its in the right date
            l = f[4]  # get the list of exercises
            for l2 in l:  # going through the exercises
                l3 = json.loads(l2)  # from string to dict
                if l3["name"] == exercise_name:  # check if there is the exercise the user want
                    full_workout_l.append(f)
                    break

    order_by_dates_l = return_dates_in_order(full_workout_l)

    for f in order_by_dates_l:
        l = f[4]  # get the list of exercises
        for l2 in l:  # going through the exercises
            l3 = json.loads(l2)  # from string to dict
            if l3["name"] == exercise_name:
                dates_l.append(f[3])
                repetitions_avg_l.append(return_the_avg(l3["sets"], "repetitions"))
                time_avg_l.append(return_the_avg(l3["sets"], "time"))
                weight_avg_l.append(return_the_avg(l3["sets"], "weight"))
                distance_KM_avg_l.append(return_the_avg(l3["sets"], "distance_KM"))
                count_sets_l.append(return_the_avg(l3["sets"], "count_sets"))

    dict1 = {"dates": dates_l, "count_sets": count_sets_l, "repetitions_avg": repetitions_avg_l, "time_avg": time_avg_l,
             "weight_avg": weight_avg_l, "distance_KM_avg": distance_KM_avg_l}

    return dict1


def return_dates_in_order(dates_lst) -> list:
    # get list of workouts and returned them in order by dates
    new_lst = sorted(dates_lst, key=lambda x: x[3])
    return new_lst


@app.get("/bring_info")
def bring_info(name: str):
    session = Session()

    find = session.query(user_table).filter(user_table.c.name == name).first() #find user row by his username

    if find is not None: #is the user exist
        first_name = find[2]
        last_name = find[3]
        phone_num = find[4]
        email = find[5]
        age = find[6]
        gender = find[7]
        goals = find[8]
        response = {"first_name": first_name, "last_name": last_name, "phone_num": phone_num, "email": email,
                    "age": age, "gender": gender, "goals": goals}

    else:
        response = {"first_name": "0", "last_name": "0", "phone_num": "0", "age": 0,
                    "gender": "0", "goals": "0"}
    return response


@app.get("/change_privacy")
def change_privacy(name: str, public: bool) -> dict[str, str]:
    session = Session()

    find = session.query(user_table).filter(user_table.c.name == name).first() #find user row by his username

    if find is not None: #if the user exist
        stmt = update(user_table).where(user_table.c.name == name).values(
            public=public
        )

        session.execute(stmt)

        session.commit()

        if not public: #if the user change to un public account, all his shared workout will delete from the shared workout table.
            response = delete_shared_workouts(chosed_user=name)



        return {"response": "the privacy changed"}

    return {"response": "the user does not exist"}


@app.get("/find_privacy")
def find_privacy(userid: str) -> dict[str, bool]:
    session = Session()
    find = session.query(user_table).filter(user_table.c.name == userid).first() #find user row by his username
    return {"response": find[9]} #bring his privacy status


@app.get("/public_user_lst")
def public_user_lst(userid: str) -> dict[str, list[Any]]:
    session = Session()

    find = session.query(user_table).filter(user_table.c.public == True).all()# list of all the public users

    username_public_lst = []

    for i in find:
        if i[0] != userid:
            username_public_lst.append(i[0]) #list of the usernames of all the public users

    return {"response": username_public_lst}

@app.get("/shareworkout")
def shareworkout(userid: str, workout_name: str, date: datetime):
    session = Session()

    find = session.query(workout_table).filter(workout_table.c.userid == userid).all()# list of all the workouts of the user

    for f in find:
        if date == f[3] and workout_name == f[2]: #if there is workout like the user sent, I add it to the shared workouts table
            session.execute(
                shared_workout_table.insert().values(
                    userid=userid,
                    workoutid=f[0]
                )
            )

            session.commit()

            return {"response": "share success"}

    return {"response": "workout data not found"}

@app.get("/unshareworkout")
def unshareworkout(workoutid: int):
    session = Session()

    find = session.query(shared_workout_table).filter(shared_workout_table.c.workoutid == workoutid).first() #the workout in the shared workout table

    if find: # if the workout exist there, it will be delete
        session.execute(
            shared_workout_table.delete().where(
                shared_workout_table.c.workoutid == workoutid
            )
        )
        session.commit()

        return {"response": "un share success"}

    return {"response": "workout data not found"}

@app.get("/bring_shared_workoutid")
def bring_shared_workoutid(chosed_user: str):
    session = Session()

    find = session.query(shared_workout_table).filter(shared_workout_table.c.userid == chosed_user).all() #list of all the shared workouts of specific user

    workoutid_lst = []
    for f in find:
        workoutid_lst.append(f[2])# list of all his workout id of the workouts he shared

    return {"response": workoutid_lst}

@app.get("/full_workout_by_workoutid")
def full_workout_by_workoutid(workoutid: str) -> dict[str, tuple]:
    session = Session()
    find = session.query(workout_table).filter(workout_table.c.workoutid == workoutid).first()
    return {"response": find}


@app.get("/delete_shared_workouts")
def delete_shared_workouts(chosed_user: str):
    session = Session()

    find = session.query(shared_workout_table).filter(shared_workout_table.c.userid == chosed_user).all()

    # delete from the shared workout table the all workouts of specific user-
    # when he become un public or delete his account
    session.execute(
        shared_workout_table.delete().where(
            shared_workout_table.c.userid == chosed_user
        )
    )

    session.commit()

    return {"response": "delete success"}


@app.get("/username_lst")
def username_lst():
    session = Session()
    find = session.query(user_table).all()

    user_lst = []
    for i in find:
        user_lst.append(i[0])

    return {"response": user_lst}


@app.get("/signed_up_users")
def signed_up_users():
    session = Session()
    find = session.query(user_table).all()

    user_lst = []
    for i in find:
        user_lst.append([i[0], i[9]])

    return {"response": user_lst}





