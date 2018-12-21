from numu import app as numu_app
from processing import scan_artist_art, scan_release_art


@numu_app.cli.command()
def check_art():
    """Check for artist and release art."""
    numu_app.logger.info("Checking artist art...")
    scan_artist_art()

    numu_app.logger.info("Checking release art...")
    scan_release_art()

    numu_app.logger.info("Art check finished!")