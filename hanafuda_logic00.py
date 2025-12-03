import random
from typing import List, Dict, Tuple

# --- 1. 札の基本定義 ---
BRIGHT = "光"
ANIMAL = "タネ"
RIBBON = "タン"
JUNK = "カス"


class Card:
    """花札の一枚を表現するクラス。"""

    def __init__(self, month: int, type: str, name: str, points: int):
        self.month = month
        self.type = type
        self.name = name
        self.points = points
        self.id = f"{month:02d}_{name}"

    def __repr__(self):
        return f"({self.month}月:{self.type}:{self.name})"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


ALL_CARDS: List[Card] = [
    # 1月：松
    Card(1, BRIGHT, "松に鶴", 20), Card(1, RIBBON, "松に赤短", 5), Card(1, JUNK, "松カスA", 1),
    Card(1, JUNK, "松カスB", 1),
    # 2月：梅
    Card(2, ANIMAL, "梅に鶯", 10), Card(2, RIBBON, "梅に赤短", 5), Card(2, JUNK, "梅カスA", 1),
    Card(2, JUNK, "梅カスB", 1),
    # 3月：桜
    Card(3, BRIGHT, "桜に幕", 20), Card(3, RIBBON, "桜に赤短", 5), Card(3, JUNK, "桜カスA", 1),
    Card(3, JUNK, "桜カスB", 1),
    # 4月：藤
    Card(4, ANIMAL, "藤に不如帰", 10), Card(4, RIBBON, "藤にムラサキ短", 5), Card(4, JUNK, "藤カスA", 1),
    Card(4, JUNK, "藤カスB", 1),
    # 5月：菖蒲
    Card(5, ANIMAL, "菖蒲に八ツ橋", 10), Card(5, RIBBON, "菖蒲にムラサキ短", 5), Card(5, JUNK, "菖蒲カスA", 1),
    Card(5, JUNK, "菖蒲カスB", 1),
    # 6月：牡丹
    Card(6, ANIMAL, "牡丹に蝶", 10), Card(6, RIBBON, "牡丹にムラサキ短", 5), Card(6, JUNK, "牡丹カスA", 1),
    Card(6, JUNK, "牡丹カスB", 1),
    # 7月：萩
    Card(7, ANIMAL, "萩に猪", 10), Card(7, RIBBON, "萩にムラサキ短", 5), Card(7, JUNK, "萩カスA", 1),
    Card(7, JUNK, "萩カスB", 1),
    # 8月：芒
    Card(8, BRIGHT, "芒に月", 20), Card(8, ANIMAL, "芒に雁", 10), Card(8, JUNK, "芒カスA", 1),
    Card(8, JUNK, "芒カスB", 1),
    # 9月：菊
    Card(9, ANIMAL, "菊に盃", 10), Card(9, RIBBON, "菊にムラサキ短", 5), Card(9, JUNK, "菊カスA", 1),
    Card(9, JUNK, "菊カスB", 1),
    # 10月：紅葉
    Card(10, ANIMAL, "紅葉に鹿", 10), Card(10, RIBBON, "紅葉に青短", 5), Card(10, JUNK, "紅葉カスA", 1),
    Card(10, JUNK, "紅葉カスB", 1),
    # 11月：柳
    Card(11, BRIGHT, "柳に小野道風", 20), Card(11, RIBBON, "柳に青短", 5), Card(11, JUNK, "柳カス", 1),
    Card(11, JUNK, "ツル", 1),
    # 12月：桐
    Card(12, BRIGHT, "桐に鳳凰", 20), Card(12, JUNK, "桐カスA", 1), Card(12, JUNK, "桐カスB", 1),
    Card(12, JUNK, "桐カスC", 1),
]


# --- 2. 役の定義と判定ロジック ---
class HanafudaRule:

    @staticmethod
    def get_player_card_ids(cards: List[Card]) -> List[str]:
        return [c.id for c in cards]

    @staticmethod
    def calculate_score(collected_cards: List[Card]) -> Tuple[int, List[str]]:
        # 役の判定ロジックは後ほど実装します
        return (0, ["未実装"])


# --- 3. ゲーム開始時の機能 ---

def initialize_game():
    """ゲーム開始時に札をシャッフルし、手札と場札を配る。"""
    deck = ALL_CARDS[:]
    random.shuffle(deck)

    player1_hand = deck[:8]
    player2_hand = deck[8:16]
    field_cards = deck[16:24]
    yama_fuda = deck[24:]

    return {
        "player1_hand": player1_hand,
        "player2_hand": player2_hand,
        "field_cards": field_cards,
        "yama_fuda": yama_fuda,
        "player1_collected": [],
        "player2_collected": [],
        "current_turn": 1,
        "game_over": False
    }


```eof

---

## 2. 🚨 メインファイル (`hanafuda00.py`) の修正

ファイル名が変わったため、メインファイル
`hanafuda00.py`
の ** インポート文 ** も修正する必要があります。

** 修正前 **

```python
from hanafuda_logic import ALL_CARDS, HanafudaRule, initialize_game, Card