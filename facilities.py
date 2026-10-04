# デモ用の施設データ（施設名・価格・評価はすべて架空）
# member_price / regular_price は1人あたりの福利厚生価格と一般サイト価格（円）
# closed_weekdays は休業曜日（0=月曜 … 6=日曜）
FACILITIES = [
    # 箱根
    {"name": "湯けむりの宿 こもれび亭", "area": "箱根", "category": "宿泊", "member_price": 9800, "regular_price": 21000, "capacity": 6, "rating": 4.3, "coupon": True, "new": False, "closed_weekdays": [], "description": "全室に露天風呂付き。キッズルームあり。"},
    {"name": "芦ノ湖リバーサイドホテル", "area": "箱根", "category": "宿泊", "member_price": 12500, "regular_price": 19800, "capacity": 4, "rating": 4.0, "coupon": False, "new": True, "closed_weekdays": [], "description": "湖を望むレイクビュー客室。"},
    {"name": "箱根そば処 山かげ", "area": "箱根", "category": "食事", "member_price": 1200, "regular_price": 1800, "capacity": 8, "rating": 4.1, "coupon": True, "new": False, "closed_weekdays": [2], "description": "自家製粉の十割そば。個室あり。"},
    {"name": "仙石原アドベンチャーフィールド", "area": "箱根", "category": "レジャー", "member_price": 2500, "regular_price": 4200, "capacity": 10, "rating": 4.4, "coupon": False, "new": False, "closed_weekdays": [1], "description": "アスレチックとジップライン。小学生から利用可。"},
    # 熱海
    {"name": "熱海 潮騒の宿 うみねこ", "area": "熱海", "category": "宿泊", "member_price": 8800, "regular_price": 17600, "capacity": 5, "rating": 4.2, "coupon": True, "new": False, "closed_weekdays": [], "description": "オーシャンビューの貸切風呂。部屋食対応。"},
    {"name": "サンビーチ熱海リゾート", "area": "熱海", "category": "宿泊", "member_price": 14800, "regular_price": 22400, "capacity": 4, "rating": 3.9, "coupon": False, "new": True, "closed_weekdays": [], "description": "屋外プール付きのリゾートホテル。"},
    {"name": "海鮮食堂 いそかぜ", "area": "熱海", "category": "食事", "member_price": 1800, "regular_price": 2600, "capacity": 6, "rating": 4.5, "coupon": True, "new": False, "closed_weekdays": [3], "description": "地魚の海鮮丼が名物。"},
    {"name": "熱海マリンクルーズ", "area": "熱海", "category": "レジャー", "member_price": 1500, "regular_price": 2400, "capacity": 20, "rating": 3.8, "coupon": False, "new": False, "closed_weekdays": [], "description": "初島周辺をめぐる50分の遊覧船。"},
    # 軽井沢
    {"name": "森のコテージ 白樺の丘", "area": "軽井沢", "category": "宿泊", "member_price": 11000, "regular_price": 18500, "capacity": 8, "rating": 4.6, "coupon": True, "new": True, "closed_weekdays": [], "description": "ペット可の一棟貸しコテージ。BBQ設備あり。"},
    {"name": "軽井沢グランフォレストホテル", "area": "軽井沢", "category": "宿泊", "member_price": 16800, "regular_price": 24000, "capacity": 4, "rating": 4.1, "coupon": False, "new": False, "closed_weekdays": [], "description": "森に囲まれたクラシックホテル。"},
    {"name": "高原ベーカリーカフェ こむぎ", "area": "軽井沢", "category": "食事", "member_price": 1100, "regular_price": 1500, "capacity": 4, "rating": 4.0, "coupon": True, "new": False, "closed_weekdays": [1, 2], "description": "焼きたてパンのモーニング。"},
    {"name": "軽井沢サイクリングベース", "area": "軽井沢", "category": "レジャー", "member_price": 1600, "regular_price": 2800, "capacity": 12, "rating": 4.2, "coupon": False, "new": True, "closed_weekdays": [], "description": "電動アシスト自転車のレンタル。子ども用あり。"},
    # 京都
    {"name": "京町家の宿 はなれ月", "area": "京都", "category": "宿泊", "member_price": 13500, "regular_price": 26000, "capacity": 4, "rating": 4.7, "coupon": True, "new": False, "closed_weekdays": [], "description": "一棟貸しの町家。坪庭付き。"},
    {"name": "ホテル鴨川テラス", "area": "京都", "category": "宿泊", "member_price": 10800, "regular_price": 16200, "capacity": 3, "rating": 3.9, "coupon": False, "new": False, "closed_weekdays": [], "description": "鴨川沿いのシティホテル。"},
    {"name": "おばんざい処 こはる", "area": "京都", "category": "食事", "member_price": 2800, "regular_price": 3800, "capacity": 6, "rating": 4.3, "coupon": True, "new": True, "closed_weekdays": [0], "description": "京野菜のおばんざいコース。"},
    {"name": "嵐山きもの散策体験", "area": "京都", "category": "レジャー", "member_price": 3000, "regular_price": 5500, "capacity": 6, "rating": 4.4, "coupon": True, "new": False, "closed_weekdays": [], "description": "着物レンタルと着付け付き。子ども用サイズあり。"},
    # 沖縄
    {"name": "美ら海ビーチヴィラ さんご", "area": "沖縄", "category": "宿泊", "member_price": 15800, "regular_price": 32000, "capacity": 6, "rating": 4.6, "coupon": True, "new": True, "closed_weekdays": [], "description": "プライベートプール付きヴィラ。"},
    {"name": "那覇シーサイドイン", "area": "沖縄", "category": "宿泊", "member_price": 7800, "regular_price": 12400, "capacity": 3, "rating": 3.7, "coupon": False, "new": False, "closed_weekdays": [], "description": "国際通りまで徒歩圏のビジネスホテル。"},
    {"name": "島そば食堂 てぃーだ", "area": "沖縄", "category": "食事", "member_price": 900, "regular_price": 1300, "capacity": 6, "rating": 4.2, "coupon": True, "new": False, "closed_weekdays": [3], "description": "ソーキそばとジューシーのセット。"},
    {"name": "青の洞窟シュノーケルツアー", "area": "沖縄", "category": "レジャー", "member_price": 4500, "regular_price": 7800, "capacity": 8, "rating": 4.8, "coupon": False, "new": False, "closed_weekdays": [], "description": "ガイド付き。6歳から参加可。"},
]
