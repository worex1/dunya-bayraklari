
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import random

Window.clearcolor = get_color_from_hex("#F2F7FF")

store = JsonStore("oyuncu.json")

COUNTRIES = [
    ("Türkiye", "Ankara"), ("Almanya", "Berlin"),
    ("Fransa", "Paris"), ("İtalya", "Roma"),
    ("İspanya", "Madrid"), ("İngiltere", "Londra"),
    ("Japonya", "Tokyo"), ("Çin", "Pekin"),
    ("Rusya", "Moskova"), ("ABD", "Washington"),
    ("Kanada", "Ottawa"), ("Brezilya", "Brasilia"),
    ("Arjantin", "Buenos Aires"), ("Mısır", "Kahire"),
    ("Yunanistan", "Atina"), ("Portekiz", "Lizbon"),
    ("Hollanda", "Amsterdam"), ("Belçika", "Brüksel"),
    ("İsviçre", "Bern"), ("Avusturya", "Viyana"),
    ("Norveç", "Oslo"), ("İsveç", "Stockholm"),
    ("Finlandiya", "Helsinki"), ("Danimarka", "Kopenhag"),
    ("Polonya", "Varşova"), ("Ukrayna", "Kiev"),
    ("Güney Kore", "Seul"), ("Hindistan", "Yeni Delhi"),
    ("Pakistan", "İslamabad"), ("Avustralya", "Canberra"),
    ("Yeni Zelanda", "Wellington"), ("Meksika", "Meksiko"),
    ("Şili", "Santiago"), ("Kolombiya", "Bogota"),
    ("Kenya", "Nairobi"), ("Nijerya", "Abuja"),
    ("Fas", "Rabat"), ("Suudi Arabistan", "Riyad"),
    ("İran", "Tahran"), ("Irak", "Bağdat")
]

def button(text, callback, color="#4385E8"):
    b = Button(
        text=text,
        size_hint_y=None,
        height=75,
        background_normal="",
        background_color=get_color_from_hex(color),
        color=(1, 1, 1, 1),
        font_size=21
    )
    b.bind(on_release=callback)
    return b

class BaseScreen(Screen):
    def layout(self, title):
        root = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=16
        )
        root.add_widget(Label(
            text=title,
            font_size=26,
            bold=True,
            color=get_color_from_hex("#243B63"),
            size_hint_y=None,
            height=65
        ))
        self.add_widget(root)
        return root

class HomeScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("🌍 DÜNYA BAYRAKLARI")

        username = store.get("player")["name"] if store.exists("player") else "Oyuncu"
        total = store.get("stats")["total"] if store.exists("stats") else 0

        root.add_widget(Label(
            text=f"Merhaba {username}!\nGünlük doğrular: 0   |   Toplam doğrular: {total}",
            color=(0.1, 0.2, 0.4, 1),
            font_size=21,
            size_hint_y=None,
            height=65
        ))

        root.add_widget(button("🎮 OYUNA BAŞLA", lambda x: self.go("levels")))
        root.add_widget(button("🌐 TÜM BAYRAKLAR", lambda x: self.go("game", mode="all")))
        root.add_widget(button("👤 PROFİLİM", lambda x: self.go("profile")))
        root.add_widget(button("🏆 SIRALAMA", lambda x: self.go("ranking")))
        root.add_widget(button("⚙️ AYARLAR", lambda x: self.go("settings")))

    def go(self, screen, **kwargs):
        self.manager.current = screen
        if screen == "game":
            self.manager.get_screen(screen).start(kwargs.get("mode", "all"))

class LevelScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("SEVİYELER")

        for i in range(1, 4):
            root.add_widget(button(
                f"⭐ {i}. SEVİYE - 40 ÜLKE",
                lambda x, n=i: self.open_level(n)
            ))

        root.add_widget(button("⬅ ANA MENÜ", lambda x: self.home()))

    def open_level(self, level):
        self.manager.get_screen("games").level = level
        self.manager.current = "games"

    def home(self):
        self.manager.current = "home"

class GameMenu(BaseScreen):
    level = 1

    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout(f"{self.level}. SEVİYE")

        modes = [
            ("🏙️ BAŞKENTİ BUL", "capital"),
            ("🚩 BAYRAK EŞLEŞTİR", "match"),
            ("⏱️ BAYRAĞI TANI", "timed"),
            ("🌍 ÜLKE VE BAŞKENT EŞLEŞTİR", "pair")
        ]

        for name, mode in modes:
            root.add_widget(button(
                name,
                lambda x, m=mode: self.open_game(m)
            ))

        root.add_widget(button("⬅ SEVİYELER", lambda x: self.back()))

    def open_game(self, mode):
        game = self.manager.get_screen("game")
        game.start(mode)
        self.manager.current = "game"

    def back(self):
        self.manager.current = "levels"

class GameScreen(BaseScreen):
    def start(self, mode):
        self.mode = mode
        self.questions = COUNTRIES.copy()
        random.shuffle(self.questions)
        self.index = 0
        self.correct = 0
        self.wrong = 0
        self.hearts = 4
        self.locked = False
        self.seconds = 120 if mode == "timed" else 0
        self.clear_widgets()
        self.root = self.layout("OYUN")
        self.show_question()

        if mode == "timed":
            Clock.unschedule(self.tick)
            Clock.schedule_interval(self.tick, 1)

    def tick(self, dt):
        if self.seconds <= 0:
            Clock.unschedule(self.tick)
            self.finish()
            return
        self.seconds -= 1
        if hasattr(self, "timer_label"):
            self.timer_label.text = f"⏱️ {self.seconds} saniye"

    def show_question(self):
        self.root.clear_widgets()

        self.root.add_widget(Label(
            text=f"DOĞRULAR: {self.correct}     ❤️ {self.hearts}",
            color=get_color_from_hex("#258B50"),
            font_size=23,
            size_hint_y=None,
            height=45
        ))

        if self.mode == "timed":
            self.timer_label = Label(
                text=f"⏱️ {self.seconds} saniye",
                color=(0.8, 0.2, 0.2, 1),
                size_hint_y=None,
                height=35
            )
            self.root.add_widget(self.timer_label)

        if self.index >= len(self.questions):
            self.finish()
            return

        country, capital = self.questions[self.index]

        if self.mode == "capital":
            self.root.add_widget(Label(
                text=country.upper(),
                font_size=36,
                bold=True,
                color=get_color_from_hex("#2868BD"),
                size_hint_y=None,
                height=110
            ))
            self.root.add_widget(Label(
                text="DOĞRU BAŞKENTİ SEÇ",
                color=(0.1, 0.2, 0.4, 1),
                size_hint_y=None,
                height=40
            ))
            choices = [capital] + random.sample(
                [c for _, c in COUNTRIES if c != capital], 3
            )

        elif self.mode == "pair":
            self.root.add_widget(Label(
                text=country.upper(),
                font_size=36,
                color=get_color_from_hex("#2868BD")
            ))
            self.root.add_widget(Label(
                text="Bu ülkenin başkenti hangisi?",
                color=(0.1, 0.2, 0.4, 1)
            ))
            choices = [capital] + random.sample(
                [c for _, c in COUNTRIES if c != capital], 3
            )

        elif self.mode == "match":
            self.root.add_widget(Label(
                text="ÜLKE VE BAŞKENT EŞLEŞTİR",
                color=(0.1, 0.2, 0.4, 1)
            ))
            self.root.add_widget(Label(
                text=f"{country} ülkesinin başkenti?",
                font_size=22,
                color=get_color_from_hex("#2868BD")
            ))
            choices = [capital] + random.sample(
                [c for _, c in COUNTRIES if c != capital], 3
            )

        else:
            self.root.add_widget(Label(
                text=f"🏳️  {country.upper()}",
                font_size=28,
                color=get_color_from_hex("#2868BD")
            ))
            self.root.add_widget(Label(
                text="Ülkenin başkentini seç!",
                color=(0.1, 0.2, 0.4, 1)
            ))
            choices = [capital] + random.sample(
                [c for _, c in COUNTRIES if c != capital], 3
            )

        random.shuffle(choices)

        for choice in choices:
            self.root.add_widget(button(
                choice,
                lambda x, c=choice: self.answer(c)
            ))

        self.root.add_widget(Label(
            text=f"Soru {self.index + 1} / {len(self.questions)}",
            color=(0.2, 0.2, 0.3, 1),
            size_hint_y=None,
            height=35
        ))

        self.feedback = Label(
            text="",
            size_hint_y=None,
            height=45
        )
        self.root.add_widget(self.feedback)

    def answer(self, choice):
        if self.locked:
            return
        self.locked = True

        correct_answer = self.questions[self.index][1]

        if choice == correct_answer:
            self.correct += 1
            self.feedback.text = "DOĞRU! 🎉"
            self.feedback.color = (0, 0.65, 0.2, 1)
        else:
            self.wrong += 1
            self.hearts -= 1
            self.feedback.text = f"YANLIŞ! Doğru cevap: {correct_answer}"
            self.feedback.color = (0.9, 0.1, 0.1, 1)

        self.save_correct()

        Clock.schedule_once(self.next_question, 1.2)

    def next_question(self, dt):
        if self.hearts <= 0:
            self.finish()
            return

        self.index += 1
        self.locked = False

        if self.mode == "timed" and self.seconds <= 0:
            self.finish()
        else:
            self.show_question()

    def save_correct(self):
        total = store.get("stats")["total"] if store.exists("stats") else 0
        store.put("stats", total=total + 1)

    def finish(self):
        Clock.unschedule(self.tick)
        self.clear_widgets()
        root = self.layout("🏆 OYUN SONUCU")

        root.add_widget(Label(
            text=f"Doğru: {self.correct}\nYanlış: {self.wrong}\nKalan can: {self.hearts}",
            font_size=23,
            color=get_color_from_hex("#243B63")
        ))

        if self.hearts > 0 and self.index >= len(self.questions) - 1:
            root.add_widget(Label(
                text="⭐ OYUN TAMAMLANDI!",
                color=(0.1, 0.6, 0.2, 1),
                font_size=22
            ))

        root.add_widget(button(
            "🔄 TEKRAR OYNA",
            lambda x: self.start(self.mode)
        ))
        root.add_widget(button(
            "ANA MENÜ",
            lambda x: self.back_home()
        ))

    def back_home(self):
        Clock.unschedule(self.tick)
        self.manager.current = "home"

class ProfileScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("👤 PROFİLİM")

        name = store.get("player")["name"] if store.exists("player") else "Oyuncu"
        total = store.get("stats")["total"] if store.exists("stats") else 0

        root.add_widget(Label(
            text=f"👤 {name}\n\nToplam doğru cevap: {total}\n🏅 Rozetler: Henüz kazanılmadı\n⭐ Unvan: Acemi Kaşif",
            color=get_color_from_hex("#243B63"),
            font_size=20
        ))
        root.add_widget(button("ANA MENÜ", lambda x: self.home()))

    def home(self):
        self.manager.current = "home"

class RankingScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("🏆 GÜNÜN EN İYİLERİ")

        root.add_widget(Label(
            text="Günlük ilk 10 sıralaması\n\nÇevrimiçi sıralama için hesap sistemi gerekiyor.",
            color=get_color_from_hex("#243B63"),
            font_size=19
        ))
        root.add_widget(button("ANA MENÜ", lambda x: self.home()))

    def home(self):
        self.manager.current = "home"

class SettingsScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("⚙️ AYARLAR")

        root.add_widget(button(
            "🔊 SES AÇ / KAPAT",
            lambda x: self.message("Ses ayarı sonraki aşamada eklenecek.")
        ))
        root.add_widget(button(
            "🌙 TEMA DEĞİŞTİR",
            lambda x: self.message("Tema ayarı sonraki aşamada eklenecek.")
        ))
        root.add_widget(button("ANA MENÜ", lambda x: self.home()))

    def message(self, msg):
        self.root.add_widget(Label(
            text=msg,
            color=(0.1, 0.2, 0.4, 1)
        ))

    def home(self):
        self.manager.current = "home"

class DunyaBayraklariApp(App):
    def build(self):
        if not store.exists("player"):
            store.put("player", name="Kaşif")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LevelScreen(name="levels"))
        sm.add_widget(GameMenu(name="games"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(RankingScreen(name="ranking"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

if __name__ == "__main__":
    DunyaBayraklariApp().run()

