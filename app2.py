import streamlit as st
from openai import OpenAI
import json

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

# chatGPTにリクエストするためのメソッドを設定。引数には理想の休日プランと重視する観点を指定
def run_gpt(content_text_to_gpt, search_focus_to_gpt):
    request_to_gpt = (
        "あなたは企業の福利厚生サービス（会員制の宿泊・レジャー優待メニュー）に詳しい旅行アドバイザーです。"
        "以下の「理想の休日プラン」に合う宿泊施設・レジャー施設を、福利厚生サービスの施設検索（キーワード検索）で見つけるための検索キーワードを提案してください。\n"
        "- キーワードの個数は固定せず、プランの条件を過不足なくカバーできる最適な数（目安3〜12個）を自分で判断すること。条件が少なければ少なく、多ければ多くてよい。重複・言い換えだけのキーワードで数を水増ししないこと\n"
        "- 福利厚生メニューの施設名・所在地・施設紹介文・設備欄に実際に書かれていそうな語を選ぶこと（例：「箱根」「草津温泉」「旅館」「コテージ」「露天風呂」「貸切風呂」「キッズルーム」「ペット可」「オールインクルーシブ」）\n"
        "- 「癒し」「最高」「おしゃれ」のような抽象的・主観的な語や、「旅行」「宿」のように広すぎる語は避けること\n"
        "- 1つのキーワードは必ず1単語のみとし、スペースや記号で複数の語を組み合わせないこと\n"
        "- 各キーワードを「エリア」「施設タイプ」「設備・サービス」「アクティビティ」のいずれかに分類すること\n"
        "- プランに地域の指定がない場合は、出発地・日数・目的から現実的に行けるエリアを推測して提案すること\n"
        "- キーワードの観点は「" + search_focus_to_gpt + "」の方針で配分すること\n"
        "- 出力は次のJSON形式のみとすること: "
        '{"summary": "施設選びの条件の要約（1文）", "keywords": [{"keyword": "検索キーワード", "category": "分類", "reason": "このキーワードでどんな施設が見つかるか（1文）"}]}\n\n'
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
st.sidebar.write("ゲスト（デモ）")
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
    st.subheader(":material/search: キーワード提案")

    tab_text, tab_condition = st.tabs([":material/chat: 文章で探す", ":material/tune: 条件で探す"])

    with tab_text:
        st.info("休日プランを文章で入力すると、福利厚生サービスの施設検索で使えるキーワードを提案します。")
        content_text_to_gpt = st.text_area(
            "どんな休日にしたいですか",
            placeholder="例：夏休みに家族4人（子ども小学生2人）で、東京から車で行ける温泉旅館に1泊したい。部屋食か個室の食事で、子どもが遊べる施設があると嬉しい。",
        )

    with tab_condition:
        # 選択を外された場合（None）は「バランスよく」として扱う
        search_focus_to_gpt = st.pills(
            "重視する観点",
            options=search_focus_kind_of,
            default=search_focus_kind_of[0],
        ) or search_focus_kind_of[0]

    if st.button("キーワードを提案", type="primary", icon=":material/search:"):
        if not content_text_to_gpt.strip():
            st.warning("「文章で探す」に休日プランを入力してください。")
        else:
            with st.spinner("福利厚生メニューで使える検索キーワードを考えています..."):
                result = run_gpt(content_text_to_gpt, search_focus_to_gpt)

            st.divider()
            st.caption("こう読み取りました。観点を変えるときは「条件で探す」から直せます。")
            st.write(result.get("summary", ""))

            st.markdown("**おすすめの検索キーワード**")
            st.caption("福利厚生サービスの施設検索欄に入力して使ってください。")
            for i, item in enumerate(result.get("keywords", []), start=1):
                st.markdown(f"**{i}. {item.get('keyword', '')}**（{item.get('category', '')}）")
                st.caption(item.get("reason", ""))
