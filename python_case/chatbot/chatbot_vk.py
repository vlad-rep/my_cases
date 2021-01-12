import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import logging

try:
    from settings import TOKEN_VK, GROUP_ID
except ImportError:
    TOKEN = None
    print('Для работы бота необходим токен группы!')
    exit()

group_id = 200039106
log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('chatbot_vk.log', 'w', 'utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s ', datefmt='%Y-%m-%d %H:%M'))
    file_handler.setLevel(logging.INFO)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot:
    """
    Echo bot для vk.com
    Use python 3.7.9
    """

    def __init__(self, GROUP_ID, TOKEN_VK):
        """
        :param group_id_vk: group_id_vk из группы в vk.com
        :param token_vk: секратный токен из группы
        """
        self.group_id = GROUP_ID
        self.token = TOKEN_VK
        self.vk = vk_api.VkApi(token=TOKEN_VK)
        self.long_poller = VkBotLongPoll(self.vk, GROUP_ID)
        self.api = self.vk.get_api()

    def run(self):
        """
        Запускает бота.
        :return:
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """
        Отправляет сообщение назад, если это текст.
        :param event: VkBotMessageEvent object
        :return:
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = f'Я тебя услышал ! \n {event.object.text} \n И как видишь могу отправить тебе тоже самое.'
            log.info(f'Отправляем сообщение --| {event.object.text} |-- назад ...')
            self.api.messages.send(
                message=message,
                random_id=get_random_id(),
                peer_id=event.object.peer_id)
        else:
            log.info('На данный момент мы не можем обрабатывать события подобного типа %s', event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(GROUP_ID, TOKEN_VK)
    bot.run()
