from datetime import datetime, timedelta

from sqlalchemy.sql import func

from backend import musicbrainz
from backend.artists import ArtistProcessing
from backend.releases import ReleaseProcessing
from backend.repo import Repo
from numu import app as numu_app


repo = Repo()
mbz = musicbrainz
artist_processing = ArtistProcessing(repo=repo, mbz=mbz)
release_processing = ReleaseProcessing(repo=repo, mbz=mbz)


def import_user_artist(check_musicbrainz=True, user_id=None):
    date_filter = datetime.now() - timedelta(days=14)
    limit = 1000
    if check_musicbrainz:
        limit = 100

    if user_id:
        artist_imports = repo.get_user_artist_imports(user_id)
    else:
        artist_imports = repo.get_artist_imports(date_filter, limit)

    for artist_import in artist_imports:
        found_artist = None
        numu_app.logger.info(
            "Checking artist import {} - {}".format(
                artist_import.user_id, artist_import.import_name
            )
        )

        numu_app.logger.info("Searching by MBID")
        found_artist = repo.get_artist_by_mbid(artist_import.import_mbid)

        if found_artist is None:
            numu_app.logger.info("Searching by name")
            found_artist = repo.get_artist_by_name(artist_import.import_name)

        if found_artist is None and check_musicbrainz:
            numu_app.logger.info("Searching MusicBrainz")
            found_artist = artist_processing.add_artist(
                name=artist_import.import_name, mbid=artist_import.import_mbid
            )
            if found_artist:
                release_processing.add_releases(found_artist)

        if found_artist is not None:
            numu_app.logger.info("Found artist {}".format(found_artist))
            user_artist = artist_processing.add_user_artist(
                artist_import.user_id, found_artist, artist_import.import_method
            )
            release_processing.update_user_releases(found_artist, user_artist, False)
        else:
            numu_app.logger.info("Did not find artist")
            if check_musicbrainz:
                artist_import.date_checked = func.now()

        repo.save(artist_import)
        repo.commit()
