import random
from typing import TypedDict, List, Optional

# 札の種別
BRIGHT = "光"
ANIMAL = "タネ"
RIBBON = "タン"
JUNK = "カス"


class Card:
    """花札の1枚を表現するクラス"""

    def __init__(self, id: int, month: int, name: str, type: str, score: int):
        self.id = id  # ユニークID (削除処理に必要)
        self.month = month  # 月
        self.name = name  # 札の名称
        self.type = type  # 札の種別 (光、タネ、タン、カス)
        self.score = score  # 札単体の点数 (今回は未使用だが定義)

    def __repr__(self):
        return f"Card(id={self.id}, month={self.month}, name='{self.name}', type='{self.type}')"

    # Streamlitのセッションステートでオブジェクトを比較できるようにするために必要
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


# ----------------- データ定義 -----------------

# 全48枚の札データ
ALL_CARDS_DATA = [
    # 1月 (松)
    (1, "松に鶴", BRIGHT, 20), (1, "松に赤短", RIBBON, 5), (1, "松にカス", JUNK, 1), (1, "松にカス", JUNK, 1),
    # 2月 (梅)
    (2, "梅に鶯", ANIMAL, 10), (2, "梅に赤短", RIBBON, 5), (2, "梅にカス", JUNK, 1), (2, "梅にカス", JUNK, 1),
    # 3月 (桜)
    (3, "桜に幕", BRIGHT, 20), (3, "桜に赤短", RIBBON, 5), (3, "桜にカス", JUNK, 1), (3, "桜にカス", JUNK, 1),
    # 4月 (藤)
    (4, "藤に不如帰", ANIMAL, 10), (4, "藤に短冊", RIBBON, 5), (4, "藤にカス", JUNK, 1), (4, "藤にカス", JUNK, 1),
    # 5月 (菖蒲)
    (5, "菖蒲に八ツ橋", ANIMAL, 10), (5, "菖蒲に短冊", RIBBON, 5), (5, "菖蒲にカス", JUNK, 1),
    (5, "菖蒲にカス", JUNK, 1),
    # 6月 (牡丹)
    (6, "牡丹に蝶", ANIMAL, 10), (6, "牡丹に青短", RIBBON, 5), (6, "牡丹にカス", JUNK, 1), (6, "牡丹にカス", JUNK, 1),
    # 7月 (萩)
    (7, "萩に猪", ANIMAL, 10), (7, "萩に短冊", RIBBON, 5), (7, "萩にカス", JUNK, 1), (7, "萩にカス", JUNK, 1),
    # 8月 (芒)
    (8, "芒に月", BRIGHT, 20), (8, "芒に雁", ANIMAL, 10), (8, "芒にカス", JUNK, 1), (8, "芒にカス", JUNK, 1),
    # 9月 (菊)
    (9, "菊に盃", ANIMAL, 10), (9, "菊に青短", RIBBON, 5), (9, "菊にカス", JUNK, 1), (9, "菊にカス", JUNK, 1),
    # 10月 (紅葉)
    (10, "紅葉に鹿", ANIMAL, 10), (10, "紅葉に青短", RIBBON, 5), (10, "紅葉にカス", JUNK, 1),
    (10, "紅葉にカス", JUNK, 1),
    # 11月 (柳)
    (11, "柳に小野道風", BRIGHT, 20), (11, "柳にツバメ", ANIMAL, 10), (11, "柳に短冊", RIBBON, 5),
    (11, "柳にカス", JUNK, 1),  # 柳は札の構成が特殊
    # 12月 (桐)
    (12, "桐に鳳凰", BRIGHT, 20), (12, "桐にカス", JUNK, 1), (12, "桐にカス", JUNK, 1), (12, "桐にカス", JUNK, 1),
]


def create_deck() -> List[Card]:
    """全ての札を作成し、シャッフルして山札を返す"""
    deck = []
    card_id_counter = 1
    for month, name, type, score in ALL_CARDS_DATA:
        deck.append(Card(card_id_counter, month, name, type, score))
        card_id_counter += 1
    random.shuffle(deck)
    return deck


# ----------------- ゲーム状態の定義 -----------------

class GameState(TypedDict):
    """ゲーム状態を格納する辞書（Streamlitのセッションステートに格納）"""
    yama_fuda: List[Card]
    field_cards: List[Card]
    player1_hand: List[Card]
    player2_hand: List[Card]
    player1_collected: List[Card]
    player2_collected: List[Card]
    current_turn: int  # 1: プレイヤー, 2: AI


# ----------------- ルール関連 -----------------

class HanafudaRule:
    """花札のルール関連のロジック（簡易版）"""

    @staticmethod
    def calculate_score(collected_cards: List[Card]) -> tuple[int, dict]:
        """獲得札から点数と役を計算する (簡易計算: 札の単体点のみ合計)"""
        total_score = sum(card.score for card in collected_cards)

        # 役のカウント（詳細な役計算は省略し、種類別枚数のみ提供）
        counts = {BRIGHT: 0, ANIMAL: 0, RIBBON: 0, JUNK: 0}
        for card in collected_cards:
            if card.type in counts:
                counts[card.type] += 1

        # カス札10枚以上を5点とする役の簡易適用
        if counts[JUNK] >= 10:
            total_score += 5  # 簡易的な点数加算

        return total_score, counts


def initialize_game() -> GameState:
    """ゲームを初期状態に戻し、札を配る"""
    deck = create_deck()

    # プレイヤーに8枚、AIに8枚、場に8枚配る
    player1_hand = deck[0:8]
    player2_hand = deck[8:16]
    field_cards = deck[16:24]
    yama_fuda = deck[24:]

    # 場札に同じ月が4枚ある場合は配り直しだが、今回は簡易版としてスキップ

    return {
        'yama_fuda': yama_fuda,
        'field_cards': field_cards,
        'player1_hand': player1_hand,
        'player2_hand': player2_hand,
        'player1_collected': [],
        'player2_collected': [],
        'current_turn': 1  # プレイヤーから開始
    }