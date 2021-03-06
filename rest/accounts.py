from flask import g, request

import response
from .api_key import require_apikey
from backend import repo
from backend.releases import ReleaseProcessor
from backend.repo import Repo
from backend.user_artists import ImportProcessor
from backend.utils import grab_json
from numu import app as numu_app
from numu import auth

from . import app


@app.route("/user", methods=["POST"])
@require_apikey
def new_user():
    email = request.json.get("email")
    password = request.json.get("password")
    icloud = request.json.get("icloud")
    if (email is None or password is None) and icloud is None:
        return response.error("Proper account credentials were not provided.")

    if icloud and repo.get_user_by_icloud(icloud):
        return response.error("Registration failed.")

    if email and repo.get_user_by_email(email):
        return response.error("Registration failed.")

    user = repo.insert_user(email, icloud, password)
    if user:
        numu_app.logger.info("New user created: {}".format(user.id))
        return response.success("New user created: {}".format(user.id))
    else:
        numu_app.logger.error("New user failed to save.")
        return response.error("An unknown error occurred when creating this account.")


@app.route("/user")
@auth.login_required
@require_apikey
def get_user():
    return response.success(
        {
            "user": {
                "email": g.user.email,
                "icloud": g.user.icloud,
                "filters": g.user.filters,
            }
        }
    )


@app.route("/user/import", methods=["POST"])
@auth.login_required
@require_apikey
def import_artists_endpoint():
    """
    Import artists
    Arguments:
    - artists: [string]
    - import_method: ['apple', 'spotify']
    """
    import_processor = ImportProcessor()
    artists = request.json.get("artists")
    import_method = request.json.get("import_method")
    if not artists or len(artists) == 0:
        return response.error("Missing artists dictionary.")
    if not import_method:
        return response.error("Missing import_method")

    saved_imports = import_processor.save_imports(g.user.id, artists, import_method)

    return response.success({"artists_imported": saved_imports})


@app.route("/user/import/lastfm", methods=["POST"])
@auth.login_required
@require_apikey
def import_lastfm_artists():
    """
    Import artists from Last.FM
    Arguments:
    - username: last.FM username to import artists from
    - period: ['7day', '1month', '3month', '6month', '12month', 'overall']
    - (optional) limit: maximum 500, default 500
    """
    user = g.user
    import_processor = ImportProcessor()
    username = request.json.get("username")
    period = request.json.get("period")
    limit = request.json.get("limit")
    if username is None or period not in [
        "7day",
        "1month",
        "3month",
        "6month",
        "12month",
        "overall",
    ]:
        return response.error("Username empty or period is incorrect.")

    if limit is None or limit > 500:
        limit = 500

    result = import_processor.import_from_lastfm(user.id, username, limit, period)

    return response.success({"artists_imported": result})


@app.route("/user/import/v2", methods=["POST"])
@auth.login_required
@require_apikey
def import_numu_v2():
    """
    Import data from Numu API v2
    Imports:
    - artists
    - listening history
    - filters
    """
    user = g.user
    repo = Repo()
    import_processor = ImportProcessor()
    release_processor = ReleaseProcessor()
    username = user.email if user.email else user.icloud

    result = {}

    data = grab_json(
        "https://www.numutracker.com/v2/json2.php?importv2={}&key={}".format(
            username, numu_app.config.get("NUMU_V2_API_KEY")
        )
    )

    result["raw_data"] = data

    filters = data.get("filters")
    if filters:
        user.album = bool(filters["album"])
        user.ep = bool(filters["ep"])
        user.single = bool(filters["single"])
        user.live = bool(filters["live"])
        user.soundtrack = bool(filters["soundtrack"])
        user.remix = bool(filters["remix"])
        user.other = bool(filters["other"])
        repo.save(user)
        repo.commit()

    artists = data.get("artists")
    if artists:
        imported = import_processor.save_imports(user.id, artists, "v2")
        result["artists_imported"] = imported

    listens = data.get("listens")
    if listens:
        releases_added = 0
        for listen in listens:
            release_mbid = listen.get("mbid")
            release = release_processor.add_release(release_mbid)

            if release:
                user_release, notify = release_processor.add_user_release(
                    release, user_id=user.id
                )
                user_release.listened = True
                user_release.date_listened = listen.get("listen_date")
                repo.save(user_release)
                if notify:
                    releases_added += 1
        repo.commit()

        result["releases_added"] = releases_added

    return response.success(result)
