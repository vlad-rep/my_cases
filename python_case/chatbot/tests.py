from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from vk_api.bot_longpoll import VkBotMessageEvent
from chatbot_vk import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1606207068, 'from_id': 90843895, 'id': 150, 'out': 0, 'peer_id': 90843895,
                            'text': 'c', 'conversation_message_id': 122, 'fwd_messages': [],
                            'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
                 'group_id': 200039106}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count  # [obj, obj, ...]
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('chatbot_vk.vk_api.VkApi'):
            with patch('chatbot_vk.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        send_mock = Mock()

        with patch('chatbot_vk.vk_api.VkApi'):
            with patch('chatbot_vk.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(
            message=self.RAW_EVENT['object']['text'],
            random_id=ANY,
            peer_id=self.RAW_EVENT['object']['peer_id'])
