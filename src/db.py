from pymongo import MongoClient
import os

from dotenv import load_dotenv

'''
사용 패키지 정의
pip install pymongo
'''

# 1) MongoDB 서버 연결 (로컬 MongoDB가 27017 포트에서 실행 중이라 가정)
load_dotenv()
DB_URI = os.environ.get("DB_URI")
client = MongoClient(DB_URI)

# 2) 사용할 데이터베이스 선택 (없으면 자동 생성)
db = client["TokiDB"]

# 현재 로직 개편으로 인해, 아래 3가지 함수는 삭제 예정
# DB 모듈 완성이 늦춰짐(이유는 다른 실행 환경에서의 오류 + 설계 미스)
# 따라서, 먼저 초기에 받은 db를 기반으로 개발을 진행하였음

def get_all_store_info():
    all_stores = list(db.stores.find({}))
    return all_stores
def get_all_menu_info():
    all_menus = list(db.items.find({}))
    return all_menus
def get_all_option_info():
    all_options = list(db.option_groups.find({}))
    return all_options

# id 기반 데이터 조회
def get_store_info_by_id(store_id):
    all_stores = list(db.stores.find({}))
    store_data = all_stores[store_id]
    return store_data
def get_menu_info_by_id(menu_id):
    menu = db.items.find_one({"_id": menu_id})
    return menu
def get_option_info_by_id(option_id):
    option = db.option_groups.find_one({"_id": option_id})
    return option

# 정보가 너무 많으면 프롬프트가 길어져서, 속도가 낮아지므로 최대한 핵심 정보만 요약
# 매장명, 매장 위치, 운영 시간만 포함했습니다.
# json 데이터를 요약해서 prompt에 사용할 수 있도록 전처리 함수
def get_store_summary(store_json: str) -> str:
    '''
    매장 데이터 JSON 문자열을 파싱하여 요약 문자열 생성
    매장명, 위치, 운영시간 정보 포함
    '''

    store = store_json
    result = ""
    name = store.get("name", "")
    address = store.get("address", {}).get("full", "")

    # 현재 operating_hours가 [] 형태로 들어와서 단순하게 get 함수 사용이 불가능함.
    # 그래서, 0번째 요소를 참조해서 사용하였고 DB 구조가 개선되면 이 또한 변경해야함.
    hours = store.get("operating_hours", {})
    open_time = hours[0].get("open", "")
    close_time = hours[0].get("close", "")
    result += f"[매장]\n이름: {name} / 위치: {address}\n운영시간: {open_time} ~ {close_time}\n"

    return result
def get_menu_summary(menu_json: str) -> str:
    '''
    메뉴 데이터 JSON 문자열을 파싱하여 메뉴 목록 요약 생성
    메뉴 ID, 이름(한국어), 가격, 옵션 ID 목록 포함
    '''
    menus = menu_json
    result = "[메뉴]\n"
    for menu in menus:
        id = menu.get("_id", "")
        name = menu.get("name", "")
        price = menu.get("base_price", "")
        option_ids = ", ".join(menu.get("option_group_ids", [])) or "없음"
        result += f"- id: {id} / 이름: {name} / 가격: {price} / 옵션: {option_ids}\n"
    return result
def get_option_summary(option_json: str) -> str:
    '''
    옵션 데이터 JSON 문자열을 파싱하여 옵션 목록 요약 생성
    옵션 ID, 이름, 선택지 라벨과 가격 포함
    '''
    options = option_json
    result = "[옵션]\n"
    for opt in options:
        id = opt.get("_id", "")
        name = opt.get("group_name", "")
        choices = ", ".join([
            f"{choice['label']}({choice['price']:+})"
            for choice in opt.get("choices", [])
        ])
        result += f"- id: {id} / 이름: {name} / 선택지: {choices}\n"
    return result

# db 조회 및 prompt 준비 함수
# 필요한 데이터를 조회 + 요약을 진행 후 이를 prmopt에 적용 및 반환
def prepare_chat_prompt(store_id):
    # 1) 매장 정보 조회
    store_data = get_store_info_by_id(store_id)

    # 2) 메뉴 ID 리스트 추출
    menu_ids = store_data.get("menu_item_ids", [])

    # 3) 메뉴 데이터 한 번에 조회
    menu_data = list(db.items.find({"_id": {"$in": menu_ids}}))

    # 4) 옵션 ID 집합 수집
    option_ids = set()
    for menu in menu_data:
        option_ids.update(menu.get("option_group_ids", []))

    # 5) 옵션 데이터 한 번에 조회
    option_data = []
    if option_ids:
        option_data = list(db.option_groups.find({"_id": {"$in": list(option_ids)}}))

    # 6) 요약 생성
    store_summary = get_store_summary(store_data)
    menu_summary = get_menu_summary(menu_data)
    option_summary = get_option_summary(option_data)

    # 7) 최종 프롬프트 조합
    prompt = f"""당신은 매장 키오스크에 탑재된 AI입니다. 아래 매장, 메뉴, 옵션 정보, 지침과 데이터 및 대화 이력을 참고하여 자연스럽게 응답하세요.

              {store_summary}

                    {menu_summary}

                    {option_summary}

                      [지침]
          - 친절하고 정중한 말투를 사용하세요.
          - 추천 이유와 옵션을 안내하세요.
          - 특수문자는 말하지 마세요.
          - 가격은 '천 원 추가돼요' 식으로 자연스럽게.
          - 정보를 한꺼번에 주지 말고 대화를 이어가세요.
          - 매장, 메뉴, 옵션 정보와 관련되지 않은 질문은 다음 문구로 응답하세요:
            "죄송합니다 고객님.. 주문 외적인 질문은 답변이 불가능합니다..."

            [출력 형식]
          당신의 모든 응답은 다음 JSON 구조로 출력되어야 합니다:

          ```json
          {{
            "Conversation": "<사용자에게 출력할 응답 문장>",
            "FunctionCall": [
              {{
                "Function": "<함수 이름>",  // 필수
                "MenuID": <메뉴 ID>,       // 필요 시
                "Quantity": <수량>,         // 필요 시
                "Option":  {{ ["옵션ID", 선택index], ... }}, // 필요 시
                "NewOption": {{ ["옵션ID", 선택index], ... }} // 필요 시
              }}
            ]
          }}
          function 종류 :
          	start : 대화를 시작했을 경우의 함수
          	ex) user : "안녕하세요~"
          	assistant : {{
          		"Conversation" : "안녕하세요~ 인생치킨에 오신 것을 환영합니다. 무엇을 도와드릴까요?",
          		"FunctionCall" : {{
          			"Function" : "start"
          		}}
          	}}
          	justChat : 액션이 필요하지 않은 대화의 경우의 함수
          	ex) user : "여기에는 무슨 메뉴를 파나요? "
          	assistant : {{
          		"Conversation" : "저희 인생치킨은 인생후라이드, 인생양념, 인생간장 치킨이 있습니다! 무엇을 드릴까요?",
          		"FunctionCall" : {{
          			"Function" : "justChat"
          		}}
          	}}
          	user : "아 그러면 후라이드 치킨으로 주세요~"
          	assistant : {{
          		"Conversation" : "저희 인생 후라이드 치킨은 18000원이며, 옵션으로 순살 혹은 콤보로 변경시 2000원 추가되며, 맵기 조절이 가능합니다. 맵기는 순하게, 보통, 맵게가 있습니다. 어떻게 하시겠습니까?",
          		"FunctionCall" : {{
          			"Function" : "justChat"
          		}}		
          	}}
          	addMenu : 사용자가 메뉴를 추가해달라고 요청했을 경우의 함수
          	ex) user : "아 그러면 순살로 맵게 해서 주세요"
          	assistant : {{
          		"Conversation" : "네, 그러면 인생 후라이드 치킨 순살, 맵게해서 장바구니에 담았습니다. 총 가격은 2만원입니다. 추가로 주문하시겠습니까?",
          		"FunctionCall" : {{
          			"Function" : "addMenu",	
          			"MenuID" : "menu001",
          			"Quantity" : 1,
          			"Option" : [ 
          				{{ 
          					"optionID" : "opt001",
          					"index" : 1 
          				}}, 
          				{{
          					"optionID" : "opt002", 
          					"index" : 2 
          				}}
          			]
          		}}
          	}}
          	changeOption : 추가된 메뉴 내에서 옵션 변경을 요청했을 경우의 함수
          	ex) user: "아, 생각해보니까 제 부모님이 매운 걸 못 드시네요... 그냥 순한 맛으로 해주세요"
          	assistant : {{
          		"Conversation" : "네, 그러면 맵기를 순한 맛으로 변경해드리겠습니다. 추가로 필요하신게 있으신가요?",
          		"FunctionCall" : {{
          			"Function" : "changeOption",
          			"MenuID" : "menu001",
          			"Quantity" : 1,
          			"Option" : [ 
          				{{ 
          					"optionID" : "opt001",
          					"index" : 1 
          				}}, 
          				{{
          					"optionID" : "opt002", 
          					"index" : 2 
          				}}
          			],
          			"NewOption" : [ 
          				{{ 
          					"optionID" : "opt001",
          					"index" : 1 
          				}}, 
          				{{
          					"optionID" : "opt002", 
          					"index" : 0 
          				}}
          			]
          		}}
          	}}
          	deleteMenu : 추가된 메뉴 중 일부를 삭제 요청했을 경우의 함수
          	ex) user : "아~ 진짜 죄송해요. 후라이드 빼주실래요? 고민 좀 더 해볼게요."
          	assistant : {{
          		"Conversation" : "네, 그러면 후라이드 치킨을 제외하겠습니다. 고민 끝나시면 주문 도와드리겠습니다.",
          		"FunctionCall" : {{
          			"Function" : "deleteMenu",	
          			"MenuID" : "menu001",	
          			"Quantity" : 1,
          			"Option" : [ 
          				{{ 
          					"optionID" : "opt001",
          					"index" : 1 
          				}}, 
          				{{
          					"optionID" : "opt002", 
          					"index" : 0 
          				}}
          			]
          		}}
          	}}
          	purchase : 결제를 요청받았을 때의 함수
          	ex) user : "아... 그냥 치킨 안 먹어야겠다. 안녕히 계세요..."
          	assistant : {{
          		"Conversation" : "네, 감사합니다. 안녕히 가세요.",	
          		"FunctionCall" : {{
          			"Function" : "end"
          		}}
          	}}
          	end : 대화가 끝났을 경우의 함수
          	ex) user : "아... 그냥 치킨 안 먹어야겠다. 안녕히 계세요..."
          	assistant : {{
          		"Conversation" : "네, 감사합니다. 안녕히 가세요.",	
          		"FunctionCall" : {{
          			"Function" : "end"
          		}}
          	}}

                      """
    return prompt
