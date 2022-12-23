### Copyright (c) 2022 Syntegrate
###
### This software is released under the MIT License.
### https://opensource.org/licenses/MIT

import rhinoscriptsyntax as rs
import datetime
import os
import clr
### without bellow, cannot do "import Grasshopper" when condition of not opening gh yet
clr.AddReferenceByName("Grasshopper")
import Grasshopper


__commandname__ = "Commit"

def add_commit_version(objs):
    
    key = "CMT_VER"
    ver = []
     
    for obj in objs:
        ver_old = rs.GetUserText(obj, key)
        if ver_old:
            if ver_old.isdecimal():
                ver.append(str(int(ver_old)+1).zfill(2))
            else:
                ver.append("00")
        else:
            ver.append("00")           
                
    for i in range(len(objs)):        
        rs.SetUserText(objs[i], key, ver[i])

    print ("Updated CMT_VER:" + ver[0])

        
        
def add_commit_date(objs):

    date = str(datetime.datetime.now().strftime("%y%m%d"))
    key = []

    for i in range(len(objs)):
        key.append("CMT_DATE")       
        rs.SetUserText(objs[i], key[i], date)

    print ("Updated CMT_DATE:" + date)


def add_commit_operator(objs, operator):

    key = []

    for i in range(len(objs)):
        key.append("CMT_OPERATOR")       
        rs.SetUserText(objs[i], key[i], operator)

    print ("Updated CMT_OPERATOR:" + operator)


def add_commit_msg(objs, msg):
    key = []

    for i in range(len(objs)):
        key.append("CMT_MSG")      
        rs.SetUserText(objs[i], key[i], msg)

    print ("Updated CMT_MSG:" + msg)


def add_commit_ghsrc(objs):
    date = str(datetime.datetime.now().strftime("%y%m%d"))

    ghdoc_server = Grasshopper.GH_InstanceServer.DocumentServer
    values = []
    key = []
    v3 = ""
    for ghdoc in ghdoc_server:
        path = ghdoc.FilePath
        filename = os.path.basename(path)
        button = rs.MessageBox("Add " + "'" + filename +"'" + " to CMT_GH?", buttons = 4)

        ### Yes -> 6, No -> 7
        if button is 6:
            values.append(filename + "_" + date)
        v = str(values)
        v1 = v.replace("[", "")
        v2 = v1.replace("]", "")
        v3 = v2.replace("'", "")

        for i in range(len(objs)):
            key.append("CMT_GH")
            rs.SetUserText(objs[i], key[i], v3)

    if v3 is not None:
        print ("Updated CMT_GH:" + v3)



def RunCommand( is_interactive ):
    operator = os.environ.get('USERNAME')
    msg = rs.StringBox("Enter message")
    objs = rs.GetObjects("Select objects")
    ver = add_commit_version(objs)

    add_commit_date(objs)
    add_commit_operator(objs, operator)
    add_commit_msg(objs, msg)
    add_commit_ghsrc(objs)

