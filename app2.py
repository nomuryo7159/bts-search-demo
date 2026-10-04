import streamlit as st
from openai import OpenAI
import json
import datetime
from facilities import FACILITIES

st.set_page_config(page_title="福利厚生キーワード提案", page_icon=":material/search:")

api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

# どの観点のキーワードを重視するかの選択肢（福利厚生メニューの施設情報はエリア・施設タイプ・設備で絞り込む）
search_focus_kind_of = [
    "バランスよく",
    "エリア（地域名・温泉地名など）を重視",
    "施設タイプ（旅館・ホテル・コテージなど）を重視",
    "設備・サービス（露天風呂・キッズ対応など）を重視",
]

# 「条件で探す」タブの選択肢（https://bts-demo.streamlit.app/ の項目に合わせる）
area_kind_of = ["すべて", "箱根", "熱海", "軽井沢", "京都", "沖縄"]
category_kind_of = ["すべて", "宿泊", "食事", "レジャー"]
sort_kind_of = ["お得順", "価格が安い順", "評価が高い順"]
weekday_names = ["月", "火", "水", "木", "金", "土", "日"]
category_icons = {"宿泊": ":material/bed:", "食事": ":material/restaurant:", "レジャー": ":material/attractions:"}

# 条件に合う施設を絞り込む。料金は1人あたりなので、予算は人数分の合計で判定する
def search_facilities(area, category, stay_date, people, budget):
    results = []
    for facility in FACILITIES:
        if area != "すべて" and facility["area"] != area:
            continue
        if category != "すべて" and facility["category"] != category:
            continue
        if stay_date.weekday() in facility["closed_weekdays"]:
            continue
        if people > facility["capacity"]:
            continue
        if budget > 0 and facility["member_price"] * people > budget:
            continue
        results.append(facility)
    return results

# 並び順に合わせて施設を並べ替える（評価なしは最後）
def sort_facilities(facilities, sort_by):
    if sort_by == "価格が安い順":
        return sorted(facilities, key=lambda f: f["member_price"])
    if sort_by == "評価が高い順":
        return sorted(facilities, key=lambda f: f["rating"] or 0, reverse=True)
    return sorted(facilities, key=lambda f: f["regular_price"] - f["member_price"], reverse=True)

# chatGPTにリクエストするためのメソッドを設定。引数には理想の休日プランと重視する観点を指定
def run_gpt(content_text_to_gpt, search_focus_to_gpt):
    request_to_gpt = (
        "あなたは企業の福利厚生サービス（会員制の宿泊・レジャー優待メニュー）に詳しい旅行アドバイザーです。"
        "以下の「理想の休日プラン」に合う宿泊施設・レジャー施設を、福利厚生サービスの施設検索（キーワード検索）で見つけるための検索キーワードを提案してください。\n"
        "- キーワードの個数は固定せず、プランの条件を過不足なくカバーできる最適な数（目安3〜12個）を自分で判断すること。条件が少なければ少なく、多ければ多くてよい。重複・言い換えだけのキーワードで数を水増ししないこと\n"
        "- 福利厚生メニューの施設名・所在地・施設紹介文・設備欄に実際に書かれていそうな語を選ぶこと（例：「箱根」「草津温泉」「旅館」「コテージ」「露天風呂」「貸切風呂」「キッズルーム」「ペット可」「オールインクルーシブ」）\n"
        "- 「癒し」「最高」「おしゃれ」のような抽象的・主観的な語や、「旅行」「宿」のように広すぎる語は避けること\n"
        "- 1つのキーワードはスペースや記号で区切らない一続きの語とし、複数の語を組み合わせないこと\n"
        "- 各キーワードを「エリア」「施設タイプ」「設備・サービス」「アクティビティ」「宿泊プラン」のいずれかに分類すること\n"
        "- プランに地域の指定がない場合は、出発地・日数・目的から現実的に行けるエリアを推測して提案すること\n"
        "- プランに宿泊日（時期）・人数（同行者）・予算に関する内容がある場合は、できる限りそれらも反映したキーワードを含めること。"
        "宿泊日・時期なら季節や時期に合う語（例：「紅葉」「花火大会」「海水浴」「年末年始」。「冬」「夏」のような広すぎる語より、「年末年始」「雪見風呂」のような具体的な語を優先すること）、"
        "人数・同行者なら人数や構成に合う語（例：「和洋室」「一棟貸し」「コネクティングルーム」「キッズ」「カップル」）、"
        "予算なら価格帯や泊まり方に合う語（例：「素泊まり」「朝食付き」「露天風呂付き客室」）を選ぶこと。"
        "日付・人数・金額の数字そのものはキーワードにしないこと\n"
        "- 宿泊日・人数・予算を反映したキーワードは、reasonでどの条件を踏まえたかが分かるように書くこと\n"
        "- キーワードの観点は「" + search_focus_to_gpt + "」の方針で配分すること\n"
        "- 出力は次のJSON形式のみとすること: "
        '{"summary": "施設選びの条件の要約（宿泊日・人数・予算の記載があれば含める。1文）", "keywords": [{"keyword": "検索キーワード", "category": "分類", "reason": "このキーワードでどんな施設が見つかるか（1文）"}]}\n\n'
        "理想の休日プラン: " + content_text_to_gpt
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request_to_gpt},
        ],
        response_format={"type": "json_object"},
    )

    # 返って来たレスポンスの内容（JSON文字列）を辞書に変換して返す
    output_content = response.choices[0].message.content.strip()
    return json.loads(output_content)

# サイドバー（ユーザー名・クーポン使用履歴・ログアウトはデモ用の見た目のみ）
st.sidebar.header(":material/search: 福利厚生キーワード提案")
st.sidebar.write("木下 亮（法務）")
page = st.sidebar.radio(
    "メニュー",
    options=["検索", "クーポン使用履歴"],
    label_visibility="collapsed",
)
if st.sidebar.button("ログアウト", icon=":material/logout:"):
    st.toast("デモ版のためログアウト機能はありません。")

if page == "クーポン使用履歴":
    with st.container(border=True):
        st.subheader(":material/confirmation_number: クーポン使用履歴")
        st.info("この機能はデモ版では準備中です。")
    st.stop()

with st.container(border=True):
    st.subheader(":material/search: 検索")

    tab_text, tab_condition = st.tabs([":material/chat: 文章で探す", ":material/tune: 条件で探す"])

    with tab_text:
        # st.info("休日プランを文章で入力すると、福利厚生サービスの施設検索で使えるキーワードを提案します。")
        content_text_to_gpt = st.text_area(
            "どんな休日にしたいですか",
            placeholder="例：夏休みに家族4人（子ども小学生2人）で、東京から車で行ける温泉旅館に1泊したい。部屋食か個室の食事で、子どもが遊べる施設があると嬉しい。",
        )
        # 選択を外された場合（None）は「バランスよく」として扱う
        search_focus_to_gpt = st.pills(
            "重視する観点",
            options=search_focus_kind_of,
            default=search_focus_kind_of[0],
        ) or search_focus_kind_of[0]

        if st.button("キーワードを提案", type="primary", icon=":material/search:", key="submit_text"):
            if not content_text_to_gpt.strip():
                st.warning("休日プランを入力してください。")
            else:
                with st.spinner("福利厚生メニューで使える検索キーワードを考えています..."):
                    result = run_gpt(content_text_to_gpt, search_focus_to_gpt)

                st.divider()
                st.caption("こう読み取りました。違うときは「条件で探す」から検索してください。")
                st.write(result.get("summary", ""))

                st.markdown("**おすすめの検索キーワード**")
                # st.caption("福利厚生サービスの施設検索欄に入力して使ってください。")
                for item in result.get("keywords", []):
                    st.markdown(
                        f"**{item.get('keyword', '')}**（{item.get('category', '')}）"
                        f"　:gray[{item.get('reason', '')}]"
                    )

    with tab_condition:
        with st.form("condition_form"):
            col_area, col_category = st.columns(2)
            area = col_area.selectbox("エリア", options=area_kind_of)
            category = col_category.selectbox("カテゴリ", options=category_kind_of)

            col_date, col_people, col_budget = st.columns(3)
            stay_date = col_date.date_input(
                "宿泊日",
                value=datetime.date.today() + datetime.timedelta(days=14),
                format="YYYY/MM/DD",
            )
            people = col_people.number_input("人数", min_value=1, value=2, step=1)
            budget = col_budget.number_input("予算（円・0なら上限なし）", min_value=0, value=0, step=1000)

            if st.form_submit_button("検索", type="primary", icon=":material/search:"):
                # 並び替えで画面が再実行されても結果が消えないよう、検索条件を保存しておく
                st.session_state["condition_search"] = (area, category, stay_date, people, budget)

        if "condition_search" in st.session_state:
            area, category, stay_date, people, budget = st.session_state["condition_search"]
            results = search_facilities(area, category, stay_date, people, budget)

            st.divider()
            col_title, col_back = st.columns([3, 1], vertical_alignment="center")
            col_title.subheader(":material/list: 検索結果", anchor=False)
            # 保存した検索条件を消して、検索前の状態に戻す
            col_back.button(
                "トップに戻る",
                icon=":material/home:",
                on_click=lambda: st.session_state.pop("condition_search", None),
                width="stretch",
            )

            col_count, col_sort = st.columns([2, 1], vertical_alignment="center")
            col_count.caption(
                f"{len(results)}件（{stay_date:%Y/%m/%d}（{weekday_names[stay_date.weekday()]}）・{people}人の料金）"
                "　施設データはデモ用の架空のものです。"
            )
            sort_by = col_sort.selectbox("並び順", options=sort_kind_of, label_visibility="collapsed")

            if not results:
                st.info("条件に合う施設が見つかりませんでした。エリアやカテゴリ、予算を変えてお試しください。")

            for facility in sort_facilities(results, sort_by):
                member_total = facility["member_price"] * people
                regular_total = facility["regular_price"] * people
                with st.container(border=True):
                    st.subheader(facility["name"], anchor=False)
                    badges = st.container(horizontal=True)
                    with badges:
                        st.badge(facility["category"], icon=category_icons[facility["category"]], color="violet")
                        st.badge(facility["area"], icon=":material/place:", color="gray")
                        if facility["new"]:
                            st.badge("新着", color="red")
                        if facility["coupon"]:
                            st.badge("クーポンあり", icon=":material/confirmation_number:", color="blue")
                        if facility["rating"]:
                            st.markdown(f"★{facility['rating']:.1f}")
                    st.subheader(f":green[{regular_total - member_total:,}円お得]", anchor=False)
                    st.markdown(f"福利厚生 **{member_total:,}円**　:gray[（一般サイト {regular_total:,}円）]")
                    st.caption(facility["description"])
