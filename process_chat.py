from json import loads, dumps

from exchange_translation import default as default_func, exchange_type, prompt
from name_exchange import name_exchange
from storage import Keywords, Sessions
from text_util import clean

KEYWORDS = Keywords()
SESSIONS = Sessions()

EXCHANGE_TYPES = {'name': name_exchange}


def process_chat(session, message):
    """Process a chat session based on the session and message.

    :param session: The unique session identifier.
    :param message: The user's message.
    :returns: The next message, if there is an appropriate one, otherwise None.
    """
    curr_exchange, data = SESSIONS.get(session)
    if data is None:
        data = {}
    else:
        data = loads(data)
    if curr_exchange is None:
        curr_exchange = 'start'

    exch_type = exchange_type(curr_exchange)
    try:
        return EXCHANGE_TYPES[exch_type](session, message)
    except KeyError:
        pass

    mapping = KEYWORDS.get_mapping(curr_exchange)
    for mess_word in clean(message).lower().split():
        if mess_word in mapping:
            new_exchange = mapping[mess_word]
            SESSIONS.set(session, new_exchange, )
            return prompt(new_exchange, data)

    # default case
    default = default_func(curr_exchange)
    if default:
        SESSIONS.set(session, default, dumps(data))
        return prompt(default, data)
    else:
        return None
