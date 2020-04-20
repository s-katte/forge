from flask import Flask, render_template, request, redirect, url_for, session
from libraries import libr_makeacnt, libr_entrydir, libr_fgconfig, libr_makemail, libr_inbxpage, libr_trashcan, libr_contacts

versinfo = libr_fgconfig.versinfo
erorlist = libr_fgconfig.erorlist

software = Flask(__name__)
software.secret_key = "t0xic0der"

@software.route("/invalses/")
def invalses():
    return render_template("invalses.html", versinfo=versinfo)

@software.route("/dashbord/")
def dashbord():
    if 'username' in session:
        username = session['username']
        return render_template("dashbord.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/makemail/", methods=["GET", "POST"])
def makemail(erorcode=""):
    if 'username' in session:
        username = session['username']
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
            elif receiver == username:
                erorcode = "sameuser"
            else:
                isitexst = libr_makemail.acntexst(receiver)
                if isitexst == False:
                    erorcode = "recvabst"
                else:
                    erorcode = "mailsucc"
                    libr_makemail.sendmail(subjtext, conttext, username, receiver)
        return render_template("makemail.html", username=username, versinfo=versinfo, erorlist=erorlist, erorcode=erorcode)
    else:
        return redirect(url_for("invalses"))

@software.route("/folocont/<usercont>/")
def folocont(usercont):
    if 'username' in session:
        username = session['username']
        libr_contacts.addtocnt(usercont, username)
        return render_template("folocont.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/unfocont/<usercont>/")
def unfocont(usercont):
    if 'username' in session:
        username = session['username']
        libr_contacts.delfmcnt(usercont, username)
        return render_template("unfocont.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/rmovmail/<paradrct>/<mailiden>/")
def rmovmail(paradrct, mailiden):
    if 'username' in session:
        username = session['username']
        libr_inbxpage.movetrsh(paradrct, mailiden)
        return render_template("rmovmail.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/purgemsg/<paradrct>/<mailiden>/")
def purgemsg(paradrct, mailiden):
    if 'username' in session:
        username = session['username']
        libr_trashcan.purgemsg(paradrct, mailiden)
        return render_template("purgemsg.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/rstrmail/<paradrct>/<mailiden>/")
def rstrmail(paradrct, mailiden):
    if 'username' in session:
        username = session['username']
        libr_trashcan.moveinbx(paradrct, mailiden)
        return render_template("rstrmail.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/inbxpage/")
def inbxpage():
    if 'username' in session:
        username = session['username']
        recvdict = libr_inbxpage.fetcrecv(username)
        senddict = libr_inbxpage.fetcsend(username)
        return render_template("inbxpage.html", username=username, versinfo=versinfo, recvdict=recvdict, senddict=senddict)
    else:
        return redirect(url_for("invalses"))

@software.route("/contacts/", methods=["GET", "POST"])
def contacts(srchuser = [], erorcode = ""):
    if 'username' in session:
        username = session['username']
        savedone = libr_contacts.fetccont(username)
        if request.method == "POST":
            srchtext = request.form["srchtext"]
            if srchtext == "":
                erorcode = "srchemty"
            else:
                srchuser = libr_contacts.fetcuser(srchtext, username)
                if srchuser == []:
                    erorcode = "nouserfd"
        return render_template("contacts.html", username=username, versinfo=versinfo, savedone=savedone, srchuser=srchuser, erorcode=erorcode, erorlist=erorlist)
    else:
        return redirect(url_for("invalses"))

@software.route("/trashcan/")
def trashcan():
    if 'username' in session:
        username = session['username']
        recvdict = libr_trashcan.fetcrecv(username)
        senddict = libr_trashcan.fetcsend(username)
        return render_template("trashcan.html", username=username, versinfo=versinfo, recvdict=recvdict, senddict=senddict)
    else:
        return redirect(url_for("invalses"))

@software.route("/grupdata/")
def grupdata():
    if 'username' in session:
        username = session['username']
        return render_template("grupdata.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/brodcast/")
def brodcast():
    if 'username' in session:
        username = session['username']
        return render_template("brodcast.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/settings/")
def settings():
    if 'username' in session:
        username = session['username']
        return render_template("settings.html", username=username, versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/fglogout/")
def fglogout():
    if 'username' in session:
        session.pop('username', None)
        return render_template("fglogout.html", username="", versinfo=versinfo)
    else:
        return redirect(url_for("invalses"))

@software.route("/viewuser/<parauser>/<usercont>/")
def viewuser(parauser, usercont):
    if 'username' in session:
        username = session['username']
        userdict = libr_contacts.fetcsing(usercont)
        return render_template("viewuser.html", username=username, versinfo=versinfo, userdict=userdict, itempara=parauser)
    else:
        return redirect(url_for("invalses"))

@software.route("/readinbx/<paradrct>/<mailiden>/")
def readinbx(paradrct, mailiden):
    if 'username' in session:
        username = session['username']
        maildict = libr_inbxpage.mailread(paradrct, mailiden, username)
        return render_template("readinbx.html", username=username, versinfo=versinfo, maildict=maildict, itempara=paradrct)
    else:
        return redirect(url_for("invalses"))

@software.route("/readtrsh/<paradrct>/<mailiden>/")
def readtrsh(paradrct, mailiden):
    if 'username' in session:
        username = session['username']
        maildict = libr_trashcan.mailread(paradrct, mailiden, username)
        return render_template("readtrsh.html", username=username, versinfo=versinfo, maildict=maildict, itempara=paradrct)
    else:
        return redirect(url_for("invalses"))

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
                    session['username'] = username
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
    software.run(port=9696, host="0.0.0.0")