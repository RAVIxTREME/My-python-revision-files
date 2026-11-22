#basic Mini project
import json
import os
import re
from datetime import datetime

# File paths for saving custom shortcuts and session history
CONFIG_FILE = "custom_emojis.json"
LOG_FILE = "conversion_history.txt"

# A cozy dictionary of standard emoticons paired with their emojis and moods
DEFAULT_EMOJIS = {
    "positive": {
        ":)": "😊", ":-)": "😊", ":D": "😁", ":-D": "😁",
        ";)": "😉", ";-)": "😉", "<3": "❤️", ":P": "😛",
        "XD": "😆", "^^": "☺️", "\\o/": "🙌", "(y)": "👍"
    },
    "negative": {
        ":(": "😒", ":-(": "😒", ":'(": "😢", "D:": "😧",
        ">:(": "😠", ":/": "😕", ":-/": "😕", "T_T": "😭",
        "(n)": "👎", "</3": "💔"
    },
    "neutral": {
        ":o": "😮", ":O": "😲", ":|": "😐", "-_-": "😑",
        "o_O": "🤨", "B)": "😎", "8)": "😎", ":*": "😘"
    }
}

class EmojiStudio:
    def __init__(self):
        print("✨ Warming up Emoji Studio...")
        self.emoji_map = self._load_and_merge_emojis()
        self.session_count = 0

    def _load_and_merge_emojis(self):
        """Flattens default categories and merges any custom emojis saved by the user."""
        flat_map = {}
        for category, emojis in DEFAULT_EMOJIS.items():
            for code, icon in emojis.items():
                flat_map[code] = {"icon": icon, "mood": category}

        # If the user has saved custom emojis before, pull them in
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    custom_emojis = json.load(f)
                    flat_map.update(custom_emojis)
            except json.JSONDecodeError:
                print("⚠️ Warning: custom_emojis.json was corrupted. Starting fresh!")
                
        return flat_map

    def add_custom_emoji(self, shortcut, emoji_char, mood="neutral"):
        """Adds a new shortcut to memory and safely saves it to disk."""
        self.emoji_map[shortcut] = {"icon": emoji_char, "mood": mood}
        
        # Load existing custom file or start fresh
        custom_data = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    custom_data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        custom_data[shortcut] = {"icon": emoji_char, "mood": mood}
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(custom_data, f, ensure_ascii=False, indent=4)
            
        print(f"🎉 Success! '{shortcut}' now turns into {emoji_char} ({mood}).\n")

    def translate_text(self, text):
        """Converts emoticons safely and evaluates the overall mood of the message."""
        # Sort keys by length in reverse (so ':-)' is checked before ':)' to avoid partial bugs)
        sorted_shortcuts = sorted(self.emoji_map.keys(), key=len, reverse=True)
        
        mood_score = 0
        total_converted = 0
        output_text = text

        for code in sorted_shortcuts:
            # Word-boundary check ensures emoticons aren't accidentally replaced inside URLs or words
            pattern = r'(?<!\w)' + re.escape(code) + r'(?!\w)'
            matches = re.findall(pattern, output_text)
            
            if matches:
                info = self.emoji_map[code]
                output_text = re.sub(pattern, info["icon"], output_text)
                count = len(matches)
                total_converted += count
                
                # Adjust sentiment score
                if info["mood"] == "positive":
                    mood_score += count
                elif info["mood"] == "negative":
                    mood_score -= count

        # Decide the vibe based on the math
        if mood_score > 0:
            vibe = "Positive 🌟"
        elif mood_score < 0:
            vibe = "Negative 🌧️"
        else:
            vibe = "Neutral ⚖️"

        self.session_count += total_converted
        self._log_to_history(text, output_text, vibe)
        
        return output_text, vibe, total_converted

    def _log_to_history(self, original, converted, vibe):
        """Saves a quiet history log with timestamps so you can check past chats."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{vibe}] '{original}' ➔ '{converted}'\n")

    def print_cheatsheet(self):
        """Prints a neat and organized list of everything the app can convert."""
        print("\n" + "="*35)
        print("         📖 EMOJI CHEATSHEET        ")
        print("="*35)
        for code, info in self.emoji_map.items():
            print(f"  {code:<6} ➔  {info['icon']}   ({info['mood']})")
        print("="*35 + "\n")


def main():
    studio = EmojiStudio()
    print("\n🚀 Welcome to Emoji Studio! Type your message to translate it.")
    print("💡 Commands you can use anytime:")
    print("   • Type '/list'   to see all shortcuts")
    print("   • Type '/add'    to teach me a new shortcut")
    print("   • Type '/stats'  to see your session count")
    print("   • Type '/exit'   to close the app\n")

    while True:
        try:
            user_input = input("💬 Your message: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            print("⚠️ Please type something first!\n")
            continue

        command = user_input.lower()

        if command == "/exit":
            print(f"\n👋 Hope you had fun! You converted {studio.session_count} emojis this session.")
            break
        elif command == "/list":
            studio.print_cheatsheet()
        elif command == "/stats":
            print(f"\n📊 Session Stat: You've converted {studio.session_count} emojis so far.\n")
        elif command == "/add":
            print("\n➕ Let's add a new custom emoji shortcut:")
            code = input("   1. Enter text shortcut (e.g. :fire:): ").strip()
            icon = input("   2. Paste the emoji symbol (e.g. 🔥): ").strip()
            mood = input("   3. Vibe/Mood [positive / negative / neutral]: ").strip().lower()
            
            if mood not in ["positive", "negative", "neutral"]:
                mood = "neutral"
                print("   (Defaulted mood to 'neutral')")
                
            if code and icon:
                studio.add_custom_emoji(code, icon, mood)
            else:
                print("⚠️ Setup cancelled: Shortcut or emoji couldn't be empty.\n")
        else:
            translated, vibe, count = studio.translate_text(user_input)
            print(f"✨ Output : {translated}")
            print(f"🔮 Vibe   : {vibe} ({count} emoji conversion(s))\n")

if __name__ == "__main__":
    main()