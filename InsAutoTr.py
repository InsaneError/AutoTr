import requests
from telethon import events
from .. import loader, utils

@loader.tds
class InsAutoTr(loader.Module):
    """Автоперевод исходящих сообщений @SheoMod"""
    strings = {'name': 'InsAutoTr'}

    LANGUAGES = {
        "ru": "Русский",
        "en": "English",
        "uk": "Українська",
        "de": "Deutsch",
        "fr": "Français",
        "es": "Español",
        "it": "Italiano",
        "pl": "Polski",
        "tr": "Türkçe",
        "ar": "العربية",
        "zh": "中文",
        "ja": "日本語",
        "ko": "한국어",
        "pt": "Português",
        "hi": "हिन्दी"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.target_lang = self.db.get("InsAutoTr", "lang", "en")
        self.enabled = self.db.get("InsAutoTr", "enabled", False)

        @self.client.on(events.NewMessage(outgoing=True))
        async def handler(event):
            if not self.enabled or not event.message.text:
                return
            text = event.message.text
            if text.startswith('.'):
                return

            try:
                url = "https://translate.googleapis.com/translate_a/single"
                params = {
                    "client": "gtx",
                    "sl": "auto",
                    "tl": self.target_lang,
                    "dt": "t",
                    "q": text
                }
                r = requests.get(url, params=params, timeout=5)
                data = r.json()
                translated = ''.join([part[0] for part in data[0] if part[0]])

                if translated and translated != text:
                    await event.message.edit(translated)
            except:
                pass

    @loader.command()
    async def inst(self, message):
        """[lang] - вкл/выкл автоперевод или сменить язык. Без аргументов - список языков"""
        args = utils.get_args_raw(message)
        
        if args:
            if args in self.LANGUAGES:
                self.target_lang = args
                self.db.set("InsAutoTr", "lang", args)
                self.enabled = True
                self.db.set("InsAutoTr", "enabled", True)
                await utils.answer(message, f"Язык: {self.LANGUAGES[args]}, перевод ON")
            else:
                await utils.answer(message, f"Неверный код языка. Используй .inst для списка")
        else:
            if self.enabled:
                self.enabled = False
                self.db.set("InsAutoTr", "enabled", False)
                await utils.answer(message, f"Автоперевод OFF (был {self.LANGUAGES.get(self.target_lang, self.target_lang)})")
            else:
                lang_list = "\n".join([f"  {code} - {name}" for code, name in self.LANGUAGES.items()])
                await utils.answer(message, f"Доступные языки:\n\n{lang_list}\n\nИспользуй: .inst <код>")
