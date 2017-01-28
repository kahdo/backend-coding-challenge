####
# /user VIEW
####

from flask import Blueprint, Response, render_template, request, make_response

from ubcmhn.flaskapp.views.basictooling import config, make_urlprefix
from ubcmhn.controllers.datapresentation import DataPresentationController
from ubcmhn.util.json import dumpjson

# Main Page
MainPageView = Blueprint("MainPage", __name__,
                         template_folder="templates/",
                         url_prefix=make_urlprefix("/"))

# Entry!
@MainPageView.route("")
def index():
    cnt = DataPresentationController(config)
    languagelist = cnt.GetLanguages()

    lang = request.args.get('lang')
    currentlang = lang if lang else languagelist[0]

    d = cnt.GetIndexPageData(language=currentlang)

    return render_template("index.html", d=d, languagelist=languagelist, currentlang=currentlang)


# Item Comments!
@MainPageView.route("storycomments")
def storycomments():
    cnt = DataPresentationController(config)
    languagelist = cnt.GetLanguages()

    itemid = request.args.get('id')
    if not itemid:
        print("itemid={}".format(itemid))
        return make_response("Error", 400)

    lang = request.args.get('lang')
    currentlang = lang if lang else languagelist[0]

    # We have itemid and lang, render it.
    rootstory, comments = cnt.GetStoryCommentData(itemid=int(itemid), language=currentlang)

    return render_template("storycomments.html",
                           item=rootstory,
                           comments=comments,
                           languagelist=languagelist,
                           currentlang=currentlang)


#    cnt = UHUserController(config)
#    userdata = cnt.get_avatar(uid)



