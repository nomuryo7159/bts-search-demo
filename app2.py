import streamlit as st
from openai import OpenAI
import json

# APIキーは .streamlit/secrets.toml の OPENAI_API_KEY から読み込む（Streamlit Community Cloud では Secrets 設定画面の値が使われる）
api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

# どの観点のキーワードを重視するかの選択肢（福利厚生メニューの施設情報はエリア・施設タイプ・設備で絞り込むことが多い）
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

st.title('福利厚生メニューで旅行施設を探す検索キーワード提案アプリ')

content_text_to_gpt = st.sidebar.text_area(
    "理想の休日プランを自由に入力してください！",
    placeholder="例：夏休みに家族4人（子ども小学生2人）で、東京から車で行ける温泉旅館に1泊したい。部屋食か個室の食事で、子どもが遊べる施設があると嬉しい。",
)

search_focus_to_gpt = st.sidebar.selectbox("重視する観点", options=search_focus_kind_of)

if st.sidebar.button("キーワードを提案してもらう"):
    if not content_text_to_gpt.strip():
        st.warning("理想の休日プランを入力してください。")
    else:
        with st.spinner("福利厚生メニューで使える検索キーワードを考えています..."):
            result = run_gpt(content_text_to_gpt, search_focus_to_gpt)

        st.subheader("施設選びの条件")
        st.write(result.get("summary", ""))

        st.subheader("おすすめの検索キーワード")
        st.caption("福利厚生サービスの施設検索欄にコピーして使ってください（右上のアイコンでコピーできます）。")
        for i, item in enumerate(result.get("keywords", []), start=1):
            st.markdown(f"**{i}. {item.get('category', '')}**")
            # st.codeで表示するとワンクリックでコピーできる
            st.code(item.get("keyword", ""), language=None)
            st.caption(item.get("reason", ""))
else:
    st.write("左のサイドバーに理想の休日プランを入力して、ボタンを押してください。")
