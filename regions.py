from calgen.location_utils import extract_location_info
from calgen.regions import EventRejected

# Philadelphia, PA metro regions, modeled at the county / neighborhood level
# (mirroring dctech.events' multi-region pattern, but for the Pennsylvania side
# of the Delaware Valley). Philadelphia city is its own region; the four
# surrounding Pennsylvania "collar counties" each form a suburban region.
_REGIONS = [
    {'slug': 'philadelphia', 'name': 'Philadelphia'},
    {'slug': 'montgomery-county', 'name': 'Montgomery County'},
    {'slug': 'bucks-county', 'name': 'Bucks County'},
    {'slug': 'chester-county', 'name': 'Chester County'},
    {'slug': 'delaware-county', 'name': 'Delaware County'},
]

# The home state for this site. Anything outside Pennsylvania is rejected.
_HOME_STATE = 'PA'

# Known suburb / borough / township names mapped to their county region slug.
# Keys are lowercased city names as returned by extract_location_info().
# Philadelphia city (and its neighborhoods) falls through to the default slug.
_CITY_TO_REGION = {
    # Philadelphia city + Philadelphia County
    'philadelphia': 'philadelphia',
    'philadelphia county': 'philadelphia',

    # Montgomery County
    'norristown': 'montgomery-county',
    'king of prussia': 'montgomery-county',
    'lansdale': 'montgomery-county',
    'pottstown': 'montgomery-county',
    'abington': 'montgomery-county',
    'cheltenham': 'montgomery-county',
    'plymouth meeting': 'montgomery-county',
    'conshohocken': 'montgomery-county',
    'ambler': 'montgomery-county',
    'lower merion': 'montgomery-county',
    'bala cynwyd': 'montgomery-county',
    'wynnewood': 'montgomery-county',
    'ardmore': 'montgomery-county',
    'narberth': 'montgomery-county',
    'willow grove': 'montgomery-county',
    'horsham': 'montgomery-county',
    'blue bell': 'montgomery-county',
    'jenkintown': 'montgomery-county',
    'glenside': 'montgomery-county',
    'fort washington': 'montgomery-county',
    'collegeville': 'montgomery-county',
    'hatboro': 'montgomery-county',
    'souderton': 'montgomery-county',
    'skippack': 'montgomery-county',
    'montgomery county': 'montgomery-county',

    # Bucks County
    'doylestown': 'bucks-county',
    'levittown': 'bucks-county',
    'bensalem': 'bucks-county',
    'bristol': 'bucks-county',
    'newtown': 'bucks-county',
    'langhorne': 'bucks-county',
    'yardley': 'bucks-county',
    'warminster': 'bucks-county',
    'warrington': 'bucks-county',
    'quakertown': 'bucks-county',
    'perkasie': 'bucks-county',
    'new hope': 'bucks-county',
    'morrisville': 'bucks-county',
    'feasterville': 'bucks-county',
    'richboro': 'bucks-county',
    'chalfont': 'bucks-county',
    'sellersville': 'bucks-county',
    'fairless hills': 'bucks-county',
    'bucks county': 'bucks-county',

    # Chester County
    'west chester': 'chester-county',
    'coatesville': 'chester-county',
    'phoenixville': 'chester-county',
    'downingtown': 'chester-county',
    'exton': 'chester-county',
    'malvern': 'chester-county',
    'kennett square': 'chester-county',
    'oxford': 'chester-county',
    'paoli': 'chester-county',
    'berwyn': 'chester-county',
    'devon': 'chester-county',
    'frazer': 'chester-county',
    'chester springs': 'chester-county',
    'honey brook': 'chester-county',
    'chester county': 'chester-county',

    # Delaware County
    'media': 'delaware-county',
    'chester': 'delaware-county',
    'upper darby': 'delaware-county',
    'lansdowne': 'delaware-county',
    'drexel hill': 'delaware-county',
    'springfield': 'delaware-county',
    'newtown square': 'delaware-county',
    'swarthmore': 'delaware-county',
    'wayne': 'delaware-county',
    'radnor': 'delaware-county',
    'villanova': 'delaware-county',
    'havertown': 'delaware-county',
    'broomall': 'delaware-county',
    'glen mills': 'delaware-county',
    'aston': 'delaware-county',
    'ridley park': 'delaware-county',
    'folsom': 'delaware-county',
    'marcus hook': 'delaware-county',
    'brookhaven': 'delaware-county',
    'chadds ford': 'delaware-county',
    'concordville': 'delaware-county',
    'delaware county': 'delaware-county',
}

# Default region for an in-state (PA) location we don't otherwise recognize.
_DEFAULT_SLUG = 'philadelphia'


def list_regions():
    return _REGIONS


def location_to_region(location_str):
    if not location_str:
        return None

    city_name, state = extract_location_info(location_str)

    # Couldn't determine a state at all -> leave unassigned (don't reject).
    if not state:
        return None

    state_upper = state.upper()
    if state_upper != _HOME_STATE:
        raise EventRejected(
            f"Event is in {state_upper}, outside the Philadelphia, PA metro area"
        )

    if not city_name:
        return _DEFAULT_SLUG

    key = city_name.strip().lower()
    return _CITY_TO_REGION.get(key, _DEFAULT_SLUG)
