import enum


class TestResult(enum.Enum):
    """ Enum representing the result of running a test case """

    UNRUN = 0
    SUCCESS = 1
    FAILED = 2


SPECIAL_TEST_NAMES = {"all", "unrun", "failed"}


class Test:
    """ Holds data about a specific test.

    :param str name: The name of the test, checks this against the valid test names
    :param function func: The function in the tester bot that makes up this test
    :param bool needs_human: Weather or not this test will require human interaction to complete
    :raises: ValueError
    """

    def __init__(self, name, func, needs_human=False):
        if name in SPECIAL_TEST_NAMES:
            raise ValueError("{} is not a valid test name".format(name))
        self.name = name
        self.func = func
        self.last_run = 0
        self.result = TestResult.UNRUN
        self.needs_human = needs_human


class TestInterface:
    """ All the tests, and some supporting functions. Tests are designed to be run
    by the tester and mixed together in order to actually test the bot.

    .. note::
        In addition to the tests failing due to their own reasons, all tests will also fail if they timeout.
        This period is specified when the bot is run.

    .. note::
        Some functions (``send_message`` and ``edit_message``) are helper functions rather than tests and serve to bring
        some of the functionality of the discord library onto the same level as the tests.

    .. note::
        ``assert_reply_*`` tests will send a message with the passed content, while ``assert_message_*`` tests require a
        ``Message`` to be passed to them. This allows for more flexibility when you need it and an easier
        option when you don't.

    :param discord.Client client: The discord client of the tester.
    :param discord.TextChannel channel: The discord channel in which to run the tests.
    :param discord.Member target: The bot we're testing.
    """

    def __init__(self, client, channel, target):
        self.client = client
        self.channel = channel
        self.target = target
        self.voice_client = None
        self.voice_channel = None

    # Imported Methods
    from ._helpers import send_message, _checkMessage, edit_message
    from ._voice import connect, disconnect
    from ._oddballs import ask_human, ensure_silence
    from ._reaction import assert_reaction_equals
    from ._message import assert_message_equals, assert_message_contains, assert_message_has_image, \
        assert_message_matches
    from ._reply import assert_reply_equals, assert_reply_contains, assert_reply_embed_equals, assert_reply_matches, \
        assert_reply_has_image, get_delayed_reply
    from ._embeds import assert_embed_equals
    from ._wait_for import wait_for_message, wait_for_reaction, wait_for_reply

    edit_message = staticmethod(edit_message)
    assert_message_equals = staticmethod(assert_message_equals)
    assert_message_contains = staticmethod(assert_message_contains)
    assert_message_has_image = staticmethod(assert_message_has_image)
    assert_message_matches = staticmethod(assert_message_matches)
    assert_embed_equals = staticmethod(assert_embed_equals)
