from flask import Flask, render_template, request, redirect, url_for
import libr_makeacnt, libr_entrydir, libr_sessdata, libr_fgconfig, libr_makemail, libr_inbxpage

versinfo = libr_fgconfig.versinfo
erorlist = libr_fgconfig.erorlist

trgtuser = None

software = Flask(__name__)

@software.route("/dashbord/")
def dashbord():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("dashbord.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/makemail/", methods=["GET", "POST"])
def makemail(erorcode=""):
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        if request.method == "POST":
            receiver = request.form["receiver"]
            subjtext = request.form["subjtext"]
            conttext = request.form["conttext"]
            if receiver == "":
                erorcode = "norecvsp"
            elif subjtext == "":
                erorcode = "nosubjsp"
            elif conttext == "":
                erorcode = "contemty"
            else:
                isitexst = libr_makemail.acntexst(receiver)
                if isitexst == False:
                    erorcode = "recvabst"
                else:
                    erorcode = "mailsucc"
                    libr_makemail.sendmail(subjtext, conttext, trgtuser["username"], receiver)
            return render_template("makemail.html", username=trgtuser["username"], versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)
        return render_template("makemail.html", username=trgtuser["username"], versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)

@software.route("/rmovmail/<paradrct>/<mailiden>/")
def rmovmail(paradrct, mailiden):
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        libr_inbxpage.movetrsh(paradrct, mailiden)
        return render_template("rmovmail.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/inbxpage/")
def inbxpage():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        recvdict = libr_inbxpage.fetcrecv(trgtuser["username"])
        senddict = libr_inbxpage.fetcsend(trgtuser["username"])
        return render_template("inbxpage.html", username=trgtuser["username"], versinfo=versinfo, recvdict=recvdict, senddict=senddict)

@software.route("/contacts/")
def contacts():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("contacts.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/trashcan/")
def trashcan():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("trashcan.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/grupdata/")
def grupdata():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("grupdata.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/brodcast/")
def brodcast():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("brodcast.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/settings/")
def settings():
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        return render_template("settings.html", username=trgtuser["username"], versinfo=versinfo)

@software.route("/fglogout/")
def fglogout():
    global trgtuser
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        trgtuser = None
        return render_template("fglogout.html", username="", versinfo=versinfo)

@software.route("/readpage/<paradrct>/<mailiden>/")
def readpage(paradrct, mailiden):
    if trgtuser == None:
        return render_template("invalses.html", versinfo=versinfo)
    else:
        maildict = libr_inbxpage.mailread(paradrct, mailiden, trgtuser["username"])
        return render_template("readpage.html", username=trgtuser["username"], versinfo=versinfo, maildict=maildict, itempara=paradrct)

@software.route("/", methods=["GET", "POST"])
def entrydir(erorcode = ""):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "":
            erorcode = "usnmabst"
        elif password == "":
            erorcode = "passabst"
        else:
            isithere = libr_entrydir.acntexst(username)
            if isithere == False:
                erorcode = "noscuser"
            else:
                isittrue = libr_entrydir.chekuser(username,password)
                if isittrue == False:
                    erorcode = "wrngpswd"
                else:
                    global trgtuser
                    trgtuser = libr_sessdata.makesess(username)
                    return dashbord()
        return render_template("entrydir.html", versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)
    return render_template("entrydir.html", versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)

@software.route("/makeacnt/", methods=["GET","POST"])
def makeacnt(erorcode = ""):
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        passrept = request.form["passrept"]
        emailadr = request.form["emailadr"]
        if passrept != password:
            erorcode = "uneqpass"
        elif fullname == "":
            erorcode = "nameabst"
        elif username == "":
            erorcode = "usnmabst"
        elif password == "":
            erorcode = "passabst"
        elif passrept == "":
            erorcode = "reptabst"
        elif emailadr == "":
            erorcode = "mailabst"
        else:
            isithere = libr_makeacnt.acntexst(username)
            if isithere == True:
                erorcode = "userexst"
            else:
                pkcsiden = libr_makeacnt.saveuser(fullname,username,password,emailadr)
                return render_template("acntmade.html", versinfo=versinfo, username=username, fullname=fullname, emailadr=emailadr, pkcsiden=pkcsiden)
        return render_template("makeacnt.html", versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)
    return render_template("makeacnt.html", versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)

if __name__ == "__main__":
    software.run(port=9696)