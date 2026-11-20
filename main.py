from supabase_config import SUPABASE_URL, SUPABASE_KEY
import requests
import threading
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from datetime import date
import random

Window.clearcolor = get_color_from_hex("#F2F7FF")
store = JsonStore("oyuncu.json")

# ÜLKE - BAŞKENT - BAYRAK
COUNTRIES = [('Türkiye', 'Ankara', '🇹🇷'), ('Almanya', 'Berlin', '🇩🇪'), ('Fransa', 'Paris', '🇫🇷'), ('İtalya', 'Roma', '🇮🇹'), ('İspanya', 'Madrid', '🇪🇸'), ('İngiltere', 'Londra', '🇬🇧'), ('Japonya', 'Tokyo', '🇯🇵'), ('Çin', 'Pekin', '🇨🇳'), ('Rusya', 'Moskova', '🇷🇺'), ('ABD', 'Washington', '🇺🇸'), ('Kanada', 'Ottawa', '🇨🇦'), ('Brezilya', 'Brasilia', '🇧🇷'), ('Arjantin', 'Buenos Aires', '🇦🇷'), ('Mısır', 'Kahire', '🇪🇬'), ('Yunanistan', 'Atina', '🇬🇷'), ('Portekiz', 'Lizbon', '🇵🇹'), ('Hollanda', 'Amsterdam', '🇳🇱'), ('Belçika', 'Brüksel', '🇧🇪'), ('İsviçre', 'Bern', '🇨🇭'), ('Avusturya', 'Viyana', '🇦🇹'), ('Norveç', 'Oslo', '🇳🇴'), ('İsveç', 'Stockholm', '🇸🇪'), ('Finlandiya', 'Helsinki', '🇫🇮'), ('Danimarka', 'Kopenhag', '🇩🇰'), ('Polonya', 'Varşova', '🇵🇱'), ('Ukrayna', 'Kiev', '🇺🇦'), ('Güney Kore', 'Seul', '🇰🇷'), ('Hindistan', 'Yeni Delhi', '🇮🇳'), ('Pakistan', 'İslamabad', '🇵🇰'), ('Avustralya', 'Canberra', '🇦🇺'), ('Yeni Zelanda', 'Wellington', '🇳🇿'), ('Meksika', 'Meksiko', '🇲🇽'), ('Şili', 'Santiago', '🇨🇱'), ('Kolombiya', 'Bogota', '🇨🇴'), ('Kenya', 'Nairobi', '🇰🇪'), ('Nijerya', 'Abuja', '🇳🇬'), ('Fas', 'Rabat', '🇲🇦'), ('Suudi Arabistan', 'Riyad', '🇸🇦'), ('İran', 'Tahran', '🇮🇷'), ('Irak', 'Bağdat', '🇮🇶'), ('İrlanda', 'Dublin', '🇮🇪'), ('İzlanda', 'Reykjavik', '🇮🇸'), ('Tayland', 'Bangkok', '🇹🇭'), ('Vietnam', 'Hanoi', '🇻🇳'), ('Malezya', 'Kuala Lumpur', '🇲🇾'), ('Singapur', 'Singapur', '🇸🇬'), ('Endonezya', 'Cakarta', '🇮🇩'), ('İsrail', 'Kudüs', '🇮🇱'), ('Güney Afrika', 'Pretoria', '🇿🇦'), ('Peru', 'Lima', '🇵🇪'), ('Çekya', 'Prag', '🇨🇿'), ('Slovakya', 'Bratislava', '🇸🇰'), ('Macaristan', 'Budapeşte', '🇭🇺'), ('Romanya', 'Bükreş', '🇷🇴'), ('Bulgaristan', 'Sofya', '🇧🇬'), ('Sırbistan', 'Belgrad', '🇷🇸'), ('Hırvatistan', 'Zagreb', '🇭🇷'), ('Slovenya', 'Ljubljana', '🇸🇮'), ('Estonya', 'Tallinn', '🇪🇪'), ('Letonya', 'Riga', '🇱🇻'), ('Litvanya', 'Vilnius', '🇱🇹'), ('Lüksemburg', 'Lüksemburg', '🇱🇺'), ('Malta', 'Valletta', '🇲🇹'), ('Kıbrıs', 'Lefkoşa', '🇨🇾'), ('Arnavutluk', 'Tiran', '🇦🇱'), ('Karadağ', 'Podgorica', '🇲🇪'), ('Kuzey Makedonya', 'Üsküp', '🇲🇰'), ('Bosna Hersek', 'Saraybosna', '🇧🇦'), ('Moldova', 'Kişinev', '🇲🇩'), ('Belarus', 'Minsk', '🇧🇾'), ('Gürcistan', 'Tiflis', '🇬🇪'), ('Ermenistan', 'Erivan', '🇦🇲'), ('Azerbaycan', 'Bakü', '🇦🇿'), ('Kazakistan', 'Astana', '🇰🇿'), ('Özbekistan', 'Taşkent', '🇺🇿'), ('Türkmenistan', 'Aşkabat', '🇹🇲'), ('Kırgızistan', 'Bişkek', '🇰🇬'), ('Tacikistan', 'Duşanbe', '🇹🇯'), ('Afganistan', 'Kabil', '🇦🇫'), ('Bangladeş', 'Dakka', '🇧🇩'), ('Nepal', 'Katmandu', '🇳🇵'), ('Sri Lanka', 'Sri Jayawardenepura Kotte', '🇱🇰'), ('Myanmar', 'Nepido', '🇲🇲'), ('Kamboçya', 'Phnom Penh', '🇰🇭'), ('Laos', 'Vientiane', '🇱🇦'), ('Filipinler', 'Manila', '🇵🇭'), ('Moğolistan', 'Ulan Batur', '🇲🇳'), ('Ürdün', 'Amman', '🇯🇴'), ('Lübnan', 'Beyrut', '🇱🇧'), ('Kuveyt', 'Kuveyt', '🇰🇼'), ('Katar', 'Doha', '🇶🇦'), ('Bahreyn', 'Manama', '🇧🇭'), ('Umman', 'Maskat', '🇴🇲'), ('Birleşik Arap Emirlikleri', 'Abu Dabi', '🇦🇪'), ('Küba', 'Havana', '🇨🇺'), ('Jamaika', 'Kingston', '🇯🇲'), ('Dominik Cumhuriyeti', 'Santo Domingo', '🇩🇴'), ('Panama', 'Panama', '🇵🇦'), ('Kosta Rika', 'San Jose', '🇨🇷'), ('Paraguay', 'Asuncion', '🇵🇾'), ('Butan', 'Thimphu', '🇧🇹'), ('Maldivler', 'Male', '🇲🇻'), ('Kuzey Kore', 'Pyongyang', '🇰🇵'), ('Suriye', 'Şam', '🇸🇾'), ('Yemen', 'Sana', '🇾🇪'), ('Haiti', 'Port-au-Prince', '🇭🇹'), ('Nikaragua', 'Managua', '🇳🇮'), ('Honduras', 'Tegucigalpa', '🇭🇳'), ('El Salvador', 'San Salvador', '🇸🇻'), ('Guatemala', 'Guatemala', '🇬🇹'), ('Belize', 'Belmopan', '🇧🇿'), ('Ekvador', 'Quito', '🇪🇨'), ('Bolivya', 'Sucre', '🇧🇴'), ('Uruguay', 'Montevideo', '🇺🇾'), ('Venezuela', 'Caracas', '🇻🇪'), ('Guyana', 'Georgetown', '🇬🇾'), ('Surinam', 'Paramaribo', '🇸🇷'), ('Etiyopya', 'Addis Ababa', '🇪🇹'), ('Tanzanya', 'Dodoma', '🇹🇿'), ('Uganda', 'Kampala', '🇺🇬'), ('Gana', 'Akra', '🇬🇭'), ('Senegal', 'Dakar', '🇸🇳'), ('Kamerun', 'Yaounde', '🇨🇲'), ('Angola', 'Luanda', '🇦🇴'), ('Mozambik', 'Maputo', '🇲🇿'), ('Zambiya', 'Lusaka', '🇿🇲'), ('Zimbabve', 'Harare', '🇿🇼'), ('Botsvana', 'Gaborone', '🇧🇼'), ('Namibya', 'Windhoek', '🇳🇦'), ('Madagaskar', 'Antananarivo', '🇲🇬'), ('Ruanda', 'Kigali', '🇷🇼'), ('Burundi', 'Gitega', '🇧🇮'), ('Somali', 'Mogadişu', '🇸🇴'), ('Sudan', 'Hartum', '🇸🇩'), ('Güney Sudan', 'Juba', '🇸🇸'), ('Libya', 'Trablus', '🇱🇾'), ('Tunus', 'Tunus', '🇹🇳'), ('Cezayir', 'Cezayir', '🇩🇿'), ('Mali', 'Bamako', '🇲🇱'), ('Nijer', 'Niamey', '🇳🇪'), ('Çad', 'Encemine', '🇹🇩'), ('Burkina Faso', 'Ouagadougou', '🇧🇫'), ('Fildişi Sahili', 'Yamoussoukro', '🇨🇮'), ('Benin', 'Porto-Novo', '🇧🇯'), ('Togo', 'Lome', '🇹🇬'), ('Gabon', 'Libreville', '🇬🇦'), ('Kongo Cumhuriyeti', 'Brazzaville', '🇨🇬'), ('Demokratik Kongo', 'Kinşasa', '🇨🇩'), ('Orta Afrika Cumhuriyeti', 'Bangui', '🇨🇫'), ('Eritre', 'Asmara', '🇪🇷')]

def save_correct():
    today = str(date.today())
    total = store.get("stats")["total"] if store.exists("stats") else 0
    daily = store.get("daily") if store.exists("daily") else {"date": today, "count": 0}
    if daily["date"] != today:
        daily = {"date": today, "count": 0}
    store.put("stats", total=total + 1)
    store.put("daily", date=today, count=daily["count"] + 1)

def get_total():
    return store.get("stats")["total"] if store.exists("stats") else 0

def get_daily():
    if not store.exists("daily"):
        return 0
    d = store.get("daily")
    return d["count"] if d["date"] == str(date.today()) else 0

def make_button(text, callback, color="#4385E8", height=105, size=30):
    b = Button(
        text=text, size_hint_y=None, height=height,
        background_normal="", background_color=get_color_from_hex(color),
        color=(1,1,1,1), font_size=size, bold=True,
        halign="center", valign="middle",
        text_size=(Window.width * 0.42, None)
    )
    b.bind(on_release=callback)
    return b

def make_label(text, size=34, height=120):
    return Label(
        text=text,
        font_size=size,
        bold=True,
        color=get_color_from_hex("#243B63"),
        halign="center",
        valign="middle",
        text_size=(Window.width - 24, None),
        size_hint_y=None,
        height=height
    )


def make_flag_image(country, height=145):
    import json
    with open("flag_codes.json", "r", encoding="utf-8") as f:
        codes = json.load(f)
    code = codes[country]
    return Image(
        source=f"flags/{code}.png",
        size_hint=(1, None),
        height=height,
        allow_stretch=True,
        keep_ratio=True
    )


class BaseScreen(Screen):
    def layout(self, title):
        root = BoxLayout(
            orientation="vertical",
            size_hint=(0.94, None),
            height=Window.height * 0.92,
            padding=18,
            spacing=16,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        root.add_widget(make_label(title, 34, 75))
        self.add_widget(root)
        return root

class HomeScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("🌍 DÜNYA BAYRAKLARI")
        root.add_widget(Label(text="", size_hint_y=1))
        name = store.get("player")["name"] if store.exists("player") else "Kaşif"
        root.add_widget(make_label(
            f"Merhaba {name}!\nGünlük doğrular: {get_daily()}   |   Toplam: {get_total()}",
            19, 75
        ))
        root.add_widget(make_button("🎮 OYUNA BAŞLA", lambda x: self.go("levels")))
        root.add_widget(make_button("🚩 TÜM BAYRAKLAR", lambda x: self.go("game", "all")))
        root.add_widget(make_button("👤 PROFİLİM", lambda x: self.go("profile")))
        root.add_widget(make_button("🏆 SIRALAMA", lambda x: self.go("ranking")))
        root.add_widget(make_button("⚙️ AYARLAR", lambda x: self.go("settings")))
        root.add_widget(Label(text="", size_hint_y=1))
    def go(self, screen, mode=None):
        if mode:
            self.manager.get_screen("game").start(mode, 0)
        self.manager.current = screen

class LevelScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("⭐ SEVİYELER")
        root.add_widget(Label(text="", size_hint_y=1))
        for i in range(1, 4):
            root.add_widget(make_button(
                f"⭐ {i}. SEVİYE - 50 ÜLKE",
                lambda x, n=i: self.open_level(n)
            ))
        root.add_widget(make_button("⬅ ANA MENÜ", lambda x: self.home()))
        root.add_widget(Label(text="", size_hint_y=1))
    def open_level(self, level):
        self.manager.get_screen("games").level = level
        self.manager.current = "games"
    def home(self):
        self.manager.current = "home"

class GameMenu(BaseScreen):
    level = 1
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout(f"⭐ {self.level}. SEVİYE")
        root.add_widget(Label(text="", size_hint_y=1))
        modes = [
            ("🏙️ BAŞKENTİ BUL", "capital"),
            ("🚩 BAYRAĞI TANI", "flag"),
            ("🧩 BAYRAK EŞLEŞTİR", "match"),
            ("🌍 ÜLKE VE BAŞKENT EŞLEŞTİR", "pair")
        ]
        for title, mode in modes:
            root.add_widget(make_button(
                title, lambda x, m=mode: self.open_game(m), height=75, size=19
            ))
        root.add_widget(make_button("⬅ SEVİYELER", lambda x: self.back()))
        root.add_widget(Label(text="", size_hint_y=1))
    def open_game(self, mode):
        self.manager.get_screen("game").start(mode, self.level)
        self.manager.current = "game"
    def back(self):
        self.manager.current = "levels"

class GameScreen(BaseScreen):
    def start(self, mode, level=0):
        Clock.unschedule(self.tick)
        self.mode = mode
        self.level = level
        if level == 0:
            self.questions = COUNTRIES[:]
        else:
            self.questions = COUNTRIES[(level-1)*50:level*50]
        random.shuffle(self.questions)
        self.index = 0
        self.correct = 0
        self.answer_state = None
        self.answer_locked = False
        self.wrong = 0
        self.hearts = 4
        self.seconds = 120
        self.selected = None
        self.match_pairs = []
        self.matched = []
        self.show_question()
        if mode == "flag":
            Clock.schedule_interval(self.tick, 1)

    def tick(self, dt):
        self.seconds -= 1
        if self.seconds <= 0:
            self.finish()
        elif self.manager and self.manager.current == "game":
            if hasattr(self, "timer_label"):
                self.timer_label.text = f"⏱️ Kalan süre: {self.seconds} saniye"

    def status(self):
        return f"✅ Doğru: {self.correct}     ❌ Yanlış: {self.wrong}     ❤️ Can: {self.hearts}"

    def show_question(self):
        self.clear_widgets()

        root = AnchorLayout(
            anchor_x="center", anchor_y="center"
        )
        panel = BoxLayout(
            orientation="vertical",
            size_hint=(0.96, None),
            height=Window.height * 0.94,
            padding=8,
            spacing=8
        )
        root.add_widget(panel)
        self.add_widget(root)

        panel.add_widget(Label(text="", size_hint_y=1))
        panel.add_widget(make_label("🌍 DÜNYA BAYRAKLARI", 34, 65))
        panel.add_widget(make_label(self.status(), 20, 42))

        if self.mode == "flag":
            self.timer_label = make_label(
                f"⏱️ Kalan süre: {self.seconds} saniye", 22, 42
            )
            panel.add_widget(self.timer_label)

        if self.hearts <= 0 or self.index >= len(self.questions):
            self.finish()
            return

        if self.mode in ("capital", "all"):
            country, capital, flag = self.questions[self.index]
            panel.add_widget(make_label(country, 38, 58))
            panel.add_widget(make_flag_image(country, 155))
            panel.add_widget(make_label(
                "Bu ülkenin başkenti hangisi?", 29, 65
            ))
            choices = [capital] + random.sample(
                [c[1] for c in COUNTRIES if c[1] != capital], 3
            )
            random.shuffle(choices)
            grid = GridLayout(
                cols=2, spacing=10, padding=5,
                size_hint=(1, None), height=190,
                row_force_default=True, row_default_height=88
            )
            for choice in choices:
                grid.add_widget(make_button(
                    choice, lambda x, a=choice: self.answer(a, capital),
                    color=('#2EAD62' if self.answer_state and choice == self.answer_state[1] else '#D94343' if self.answer_state and choice == self.answer_state[0] else '#4385E8'),
                    height=88, size=25
                ))
            panel.add_widget(grid)

        elif self.mode == "flag":
            country, capital, flag = self.questions[self.index]
            panel.add_widget(make_flag_image(country, 190))
            panel.add_widget(make_label(
                "Bu bayrak hangi ülkenin?", 30, 65
            ))
            choices = [country] + random.sample(
                [c[0] for c in COUNTRIES if c[0] != country], 3
            )
            random.shuffle(choices)
            grid = GridLayout(
                cols=2, spacing=10, padding=5,
                size_hint=(1, None), height=190,
                row_force_default=True, row_default_height=88
            )
            for choice in choices:
                grid.add_widget(make_button(
                    choice, lambda x, a=choice: self.answer(a, country),
                    color=('#2EAD62' if self.answer_state and choice == self.answer_state[1] else '#D94343' if self.answer_state and choice == self.answer_state[0] else '#4385E8'),
                    height=88, size=24
                ))
            panel.add_widget(grid)

        elif self.mode in ("match", "pair"):
            if not self.match_pairs:
                self.match_pairs = random.sample(
                    self.questions[self.index:],
                    min(4, len(self.questions)-self.index)
                )
                self.matched = []
                self.selected = None

            title = "Bayrakları ülkelerle eşleştir" if self.mode == "match" else "Ülkeleri başkentleriyle eşleştir"
            panel.add_widget(make_label(title, 25, 55))
            panel.add_widget(make_label(
                "Önce soldan seç, sonra sağdan eşini seç.", 19, 42
            ))

            grid = GridLayout(
                cols=2, spacing=9, padding=5,
                size_hint=(1, None), height=260,
                row_force_default=True, row_default_height=60
            )
            left = [c for c in self.match_pairs if c not in self.matched]
            right = left[:]
            random.shuffle(left)
            random.shuffle(right)

            for i in range(max(len(left), len(right))):
                if i < len(left):
                    c = left[i]
                    txt = c[2] if self.mode == "match" else c[0]
                    grid.add_widget(make_button(
                        txt, lambda x, item=c: self.choose_left(item),
                        color="#8B65C7", height=60, size=20
                    ))
                else:
                    grid.add_widget(Label())
                if i < len(right):
                    c = right[i]
                    txt = c[0] if self.mode == "match" else c[1]
                    grid.add_widget(make_button(
                        txt, lambda x, item=c: self.choose_right(item),
                        color="#E68A43", height=60, size=20
                    ))
                else:
                    grid.add_widget(Label())

            panel.add_widget(grid)
            if self.selected:
                panel.add_widget(make_label(
                    "Seçimin: " + (
                        self.selected[2] if self.mode == "match" else self.selected[0]
                    ), 19, 40
                ))

            panel.add_widget(make_button(
                "🏠 ANA MENÜ", lambda x: self.back_home(),
                color="#60758D", height=58, size=20
            ))

        panel.add_widget(Label(text="", size_hint_y=1))

    def answer(self, choice, correct_answer):
        if self.answer_locked or self.answer_state:
            return
        self.answer_locked = True
        self.answer_state = (choice, correct_answer)
        if choice == correct_answer:
            self.correct += 1
            save_correct()
            self.show_question()
            Clock.schedule_once(self.advance_after_correct, 0.4)
        else:
            self.wrong += 1
            self.hearts -= 1
            self.show_question()
            self.answer_locked = False

    def advance_after_correct(self, dt):
        self.answer_state = None
        self.answer_locked = False
        self.index += 1
        if self.hearts <= 0 or self.index >= len(self.questions):
            self.finish()
        else:
            self.show_question()

    def on_touch_down(self, touch):
        if self.answer_state and self.answer_state[0] != self.answer_state[1]:
            self.answer_state = None
            if self.hearts <= 0:
                self.finish()
            else:
                self.index += 1
                self.show_question()
            return True
        return super().on_touch_down(touch)

    def choose_left(self, item):
        self.selected = item
        self.show_question()

    def choose_right(self, item):
        if not self.selected:
            return
        if item == self.selected:
            self.matched.append(item)
            self.correct += 1
            save_correct()
            self.selected = None
            if len(self.matched) == len(self.match_pairs):
                self.index += len(self.match_pairs)
                self.match_pairs = []
            self.show_question()
        else:
            self.wrong += 1
            self.hearts -= 1
            self.selected = None
            if self.hearts <= 0:
                self.finish()
            else:
                self.show_question()

    def finish(self):
        Clock.unschedule(self.tick)
        self.clear_widgets()
        root = self.layout("🏁 OYUN SONU")
        root.add_widget(make_label(
            f"✅ Doğru cevap: {self.correct}\n❌ Yanlış cevap: {self.wrong}\n❤️ Kalan can: {self.hearts}",
            25, 150
        ))
        if self.hearts > 0 and self.index >= len(self.questions):
            root.add_widget(make_label("⭐ OYUN TAMAMLANDI!", 25, 65))
        root.add_widget(make_button("🔄 TEKRAR OYNA", lambda x: self.start(self.mode, self.level)))
        root.add_widget(make_button("🏠 ANA MENÜ", lambda x: self.back_home()))
    def back_home(self):
        Clock.unschedule(self.tick)
        self.manager.current = "home"

class ProfileScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("👤 PROFİLİM")
        name = store.get("player")["name"] if store.exists("player") else "Kaşif"
        root.add_widget(make_label(
            f"👤 {name}\n\nToplam doğru cevap: {get_total()}\n🏅 Rozetler: Oyun ilerledikçe kazanılacak\n⭐ Unvan: Acemi Kaşif",
            20, 180
        ))
        root.add_widget(make_button("ANA MENÜ", lambda x: self.home()))
    def home(self):
        self.manager.current = "home"

class RankingScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("🏆 GÜNÜN EN İYİLERİ")
        root.add_widget(make_label(
            "Günlük doğru cevap: " + str(get_daily()) +
            "\n\nÇevrimiçi ilk 10 sıralaması için sunucu bağlantısı gerekiyor.",
            20, 150
        ))
        root.add_widget(make_button("ANA MENÜ", lambda x: self.home()))
    def home(self):
        self.manager.current = "home"

class SettingsScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = self.layout("⚙️ AYARLAR")
        root.add_widget(make_label("Görünüm ve ses ayarları sonraki geliştirmede eklenecek.", 19, 100))
        root.add_widget(make_button("ANA MENÜ", lambda x: self.home()))
    def home(self):
        self.manager.current = "home"


class AuthScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()

        center = AnchorLayout(
            anchor_x="center",
            anchor_y="center"
        )

        panel = BoxLayout(
            orientation="vertical",
            size_hint=(0.9, None),
            height=590,
            spacing=14,
            padding=20
        )

        panel.add_widget(make_label(
            "🌍 DÜNYA BAYRAKLARI",
            30, 85
        ))

        self.username = TextInput(
            hint_text="Kullanıcı adı",
            multiline=False,
            size_hint_y=None,
            height=60,
            font_size=22
        )

        self.email = TextInput(
            hint_text="E-posta adresi",
            multiline=False,
            size_hint_y=None,
            height=60,
            font_size=22
        )

        self.password = TextInput(
            hint_text="Şifre",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=60,
            font_size=22
        )

        panel.add_widget(self.username)
        panel.add_widget(self.email)
        panel.add_widget(self.password)

        panel.add_widget(make_button(
            "KAYIT OL", self.signup,
            height=75, size=27
        ))

        panel.add_widget(make_button(
            "GİRİŞ YAP", self.login,
            height=75, size=27
        ))

        self.status = make_label("", 18, 60)
        panel.add_widget(self.status)

        center.add_widget(panel)
        self.add_widget(center)

    def show_message(self, message):
        self.status.text = message

    def signup(self, instance):
        username = self.username.text.strip()
        email = self.email.text.strip()
        password = self.password.text

        if not username or not email or not password:
            self.show_message("Tüm alanları doldur.")
            return

        self.show_message("Kayıt işlemi yapılıyor...")
        threading.Thread(
            target=self.signup_request,
            args=(username, email, password),
            daemon=True
        ).start()

    def signup_request(self, username, email, password):
        try:
            response = requests.post(
                SUPABASE_URL + "/auth/v1/signup",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "email": email,
                    "password": password,
                    "data": {"username": username}
                },
                timeout=20
            )

            if response.status_code >= 400:
                data = response.json()
                message = data.get("msg") or data.get("message") or "Kayıt başarısız."
            else:
                message = "Kayıt başarılı! E-postanı doğrula, sonra giriş yap."

        except Exception as e:
            message = f"Kayıt hatası: {type(e).__name__}: {e}"

        Clock.schedule_once(
            lambda dt: self.show_message(message)
        )

    def login(self, instance):
        email = self.email.text.strip()
        password = self.password.text

        if not email or not password:
            self.show_message("E-posta ve şifreni gir.")
            return

        self.show_message("Giriş yapılıyor...")
        threading.Thread(
            target=self.login_request,
            args=(email, password),
            daemon=True
        ).start()

    def login_request(self, email, password):
        try:
            response = requests.post(
                SUPABASE_URL + "/auth/v1/token?grant_type=password",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "email": email,
                    "password": password
                },
                timeout=20
            )

            data = response.json()

            if response.status_code >= 400:
                message = data.get("msg") or data.get("message") or "Giriş başarısız."
            else:
                user = data.get("user", {})
                username = user.get("user_metadata", {}).get("username")
                username = username or "Kaşif"

                store.put(
                    "auth",
                    access_token=data["access_token"],
                    refresh_token=data["refresh_token"],
                    user_id=user["id"]
                )
                store.put("player", name=username)
                message = "Giriş başarılı!"

                Clock.schedule_once(
                    lambda dt: setattr(self.manager, "current", "home")
                )

        except Exception as e:
            message = f"Hata: {type(e).__name__}: {e}"

        Clock.schedule_once(
            lambda dt: self.show_message(message)
        )


class DunyaBayraklariApp(App):
    def build(self):
        if not store.exists("player"):
            store.put("player", name="Kaşif")

        sm = ScreenManager()

        splash = Screen(name="splash")
        splash_layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=20
        )
        splash_layout.add_widget(Label(
            text="🌍 DÜNYA BAYRAKLARI",
            font_size=28,
            bold=True,
            color=get_color_from_hex("#243B63")
        ))
        splash_layout.add_widget(Image(
            source="uygulama_ikonu_kaynak.png",
            size_hint=(1, 0.75),
            allow_stretch=True,
            keep_ratio=True
        ))
        splash.add_widget(splash_layout)
        sm.add_widget(splash)

        sm.add_widget(AuthScreen(name="auth"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LevelScreen(name="levels"))
        sm.add_widget(GameMenu(name="games"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(RankingScreen(name="ranking"))
        sm.add_widget(SettingsScreen(name="settings"))

        sm.current = "splash"
        Clock.schedule_once(lambda dt: self.check_saved_session(sm), 3)
        return sm

    def check_saved_session(self, sm):
        if not store.exists("auth") or not store.get("auth").get("refresh_token"):
            sm.current = "auth"
            return
        threading.Thread(target=self.refresh_session, args=(sm,), daemon=True).start()

    def refresh_session(self, sm):
        try:
            saved = store.get("auth")
            response = requests.post(
                SUPABASE_URL + "/auth/v1/token?grant_type=refresh_token",
                headers={"apikey": SUPABASE_KEY, "Content-Type": "application/json"},
                json={"refresh_token": saved["refresh_token"]},
                timeout=20
            )
            data = response.json()
            if response.status_code >= 400 or not data.get("access_token"):
                raise ValueError("Oturum yenilenemedi")
            user = data.get("user", {})
            store.put("auth", access_token=data["access_token"], refresh_token=data["refresh_token"], user_id=user.get("id", saved.get("user_id")))
            username = user.get("user_metadata", {}).get("username")
            if username:
                store.put("player", name=username)
            Clock.schedule_once(lambda dt: setattr(sm, "current", "home"))
        except Exception:
            store.delete("auth")
            Clock.schedule_once(lambda dt: setattr(sm, "current", "auth"))

if __name__ == "__main__":
    DunyaBayraklariApp().run()
