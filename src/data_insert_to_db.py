# mongo_insert.py
from pymongo import MongoClient
import json

# 0 : 카페
# 1 : 국밥
# 2 : 김밥

# 로컬 MongoDB 서버 (기본 포트 27017)
client = MongoClient("mongodb://localhost:27017/")

# DB 선택
db = client["TokiDB"]


#data_list
stores = [
    {
        "_id": "store_sch_coffee",
        "name": "순천향커피",
        "menu_item_ids": [
            "item_financier_plain","item_financier_soboru", "item_financier_caramel",
            "item_financier_nunettine","item_canale","item_eggtart", "item_tigre",
            "item_pretzel_almond","item_bagel_pizza", "item_americano", "item_latte_strawberry"
        ],
        "category": ["카페", "디저트"],
        "address": {
            "full": "충청남도 아산시 순냥대로 19, 1층",
            "postal_code": "A13834"
        },
        "phone": "123-333-330",
        "operating_hours": [
            {
                "day": "매일",
                "open": "09:00",
                "close": "20:00",
                "break_time": None,
                "last_order": "19:30"
            }
        ],
        "services": {
            "takeout": True,
            "delivery": False
        },
        "self_service_info": "물과 냅킨, 시럽은 카운터 옆에 준비되어 있습니다.",
        "amenities": {
            "restroom": {
                "available": True,
                "details": "가게 내부, 남/녀 공용"
            },
            "seating_capacity": 24,
            "parking": {
                "available": True,
                "details": "건물 뒷편 전용 주차장 (3대 가능)"
            },
            "wifi": {
                "available": True,
                "ssid": "sch_coffee_2g",
                "password": "없음"
            }
        },
        "payment_methods": ["카드", "현금", "아산사랑상품권", "카카오페이"],
        "discounts": [
            {
                "name": "텀블러 할인",
                "details": "개인 텀블러 이용 시 모든 음료 300원 할인"
            },
            {
                "name": "오픈 이벤트",
                "details": "베이커리 1만원 이상 구매 시 아메리카노 1잔 무료 (~11/30까지)"
            }
        ]
    },
    {
        "_id": "store_1year_gukbap",
        "name": "1년 전통 국밥",
        "menu_item_ids": [
          "item_gukbap_sundae",
          "item_gukbap_naejang",
          "item_gukbap_banban",
          "item_gukbap_makchang",
          "item_plate_sundae",
          "item_plate_naejang",
          "item_plate_banban"
        ],
        "category": ["일반음식점", "국밥"],
        "address": {
          "full": "경기도 평택시 신장로 55, 1층",
          "postal_code": "ab3921"
        },
        "phone": "031-252-1211",
        "operating_hours": [
          {
            "day": "매일",
            "open": "07:00",
            "close": "22:00",
            "break_time": None,
            "last_order": "21:30"
          }
        ],
        "services": {
          "takeout": True,
          "delivery": False
        },
        "self_service_info": "셀프바에서 반찬과 밥을 무료로 리필할 수 있습니다.",
        "amenities": {
          "restroom": {
            "available": True,
            "details": "매장 외부, 비밀번호 없음"
          },
          "seating_capacity": 44,
          "parking": {
            "available": True,
            "details": "최대 4대 가능"
          },
          "wifi": {
            "available": False,
            "ssid": None,
            "password": None
          }
        },
        "payment_methods": ["경기페이", "카드", "현금"],
        "discounts": [
          {
            "name": "포장 할인",
            "details": "포장 주문 시 1,000원 할인"
          },
          {
            "name": "단체 할인",
            "details": "10만원 이상 결제 시 3% 할인"
          }
        ]
      },
    {
        "_id": "store_kimbap_script",
        "name": "김밥스크립트",
        "menu_item_ids": [
          "item_kimbap_general",
          "item_kimbap_tuna",
          "item_kimbap_pork_cutlet",
          "item_kimbap_custom",
          "item_pork_cutlet_loin",
          "item_pork_cutlet_cheese",
          "item_jeyuk_deopbap",
          "item_ramen",
          "item_udon",
          "item_soda",
          "item_soju",
          "item_beer"
        ],
        "category": ["일반음식점", "분식", "김밥"],
        "address": {
          "full": "충청남도 아산시 용화로 35, 2층",
          "postal_code": "aa3w42"
        },
        "phone": "041-000-0000",
        "operating_hours": [
          {
            "day": "매일",
            "open": "07:30",
            "close": "20:00",
            "break_time": None,
            "last_order": "19:30"
          }
        ],
        "services": {
          "takeout": True,
          "delivery": True
        },
        "self_service_info": "반찬코너, 정수기, 물컵이 준비되어 있습니다.",
        "amenities": {
          "restroom": {
            "available": True,
            "details": "매장 우측 상가 내에 위치합니다. 비밀번호는 1234 입니다."
          },
          "seating_capacity": 32,
          "parking": {
            "available": True,
            "details": "건물 주차장 이용 (승용차 5대)"
          },
          "wifi": {
            "available": False,
            "ssid": None,
            "password": None
          }
        },
    "payment_methods": ["아산페이", "현금", "신용카드 (롯데카드 제외)"],
    "discounts": [
      {
        "name": "무료 배달",
        "details": "3만원 이상 구매 시 1km 내 무료 배달"
      }
    ]
  }
]
items = [
    {"_id": "item_kimbap_general", "name": "제너럴 김밥", "base_price": 2000, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_kimbap_tuna", "name": "참치김밥", "base_price": 3500, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_kimbap_pork_cutlet", "name": "돈까스김밥", "base_price": 3500,
     "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_kimbap_custom", "name": "사용자 정의 김밥", "base_price": 3000,
     "option_group_ids": ["opt_kimbap_topping_sausage", "opt_kimbap_topping_egg", "opt_kimbap_topping_tuna",
                          "opt_kimbap_topping_pork", "opt_kimbap_topping_cheese", "opt_kimbap_topping_ddukgalbi",
                          "opt_side_dish_extra"]},

    {"_id": "item_gukbap_sundae", "name": "순대국밥", "base_price": 9000,
     "option_group_ids": ["opt_gukbap_size", "opt_side_dish_extra"]},
    {"_id": "item_gukbap_naejang", "name": "내장국밥", "base_price": 9000,
     "option_group_ids": ["opt_gukbap_size", "opt_side_dish_extra"]},
    {"_id": "item_gukbap_banban", "name": "반반국밥", "base_price": 10000,
     "option_group_ids": ["opt_gukbap_size", "opt_side_dish_extra"]},
    {"_id": "item_gukbap_makchang", "name": "막창국밥", "base_price": 12000,
     "option_group_ids": ["opt_gukbap_size", "opt_side_dish_extra"]},

    {"_id": "item_plate_sundae", "name": "순대한접시", "base_price": 15000, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_plate_naejang", "name": "내장한접시", "base_price": 15000, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_plate_banban", "name": "반반한접시", "base_price": 20000, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_pork_cutlet_loin", "name": "등심돈까스", "base_price": 8000, "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_pork_cutlet_cheese", "name": "치즈돈까스", "base_price": 9000,
     "option_group_ids": ["opt_side_dish_extra"]},
    {"_id": "item_jeyuk_deopbap", "name": "제육덮밥", "base_price": 8000,
     "option_group_ids": ["opt_dish_size", "opt_side_dish_extra"]},

# 라면 커스텀 옵션 -> 기본 옵션 참조(맵기 조절 옵션 추가)
    {"_id": "item_ramen", "name": "라면", "base_price": 4000,
     "option_group_ids": ["opt_ramen_toppings", "opt_ramen_spicy", "opt_side_dish_extra"]},
    {"_id": "item_udon", "name": "우동", "base_price": 6000, "option_group_ids": ["opt_side_dish_extra"]},

    {"_id": "item_financier_plain", "name": "플레인 휘낭시에", "base_price": 2500,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_financier_soboru", "name": "소보루 휘낭시에", "base_price": 2700,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_financier_caramel", "name": "솔티캐러멜 휘낭시에", "base_price": 2700,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_financier_nunettine", "name": "누네띠네 휘낭시에", "base_price": 2700,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_canale", "name": "까눌레", "base_price": 3000,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_eggtart", "name": "에그타르트", "base_price": 3500,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_tigre", "name": "티그레", "base_price": 3000,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_pretzel_almond", "name": "아몬드 프레첼", "base_price": 4500,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},
    {"_id": "item_bagel_pizza", "name": "피자 베이글", "base_price": 4900,
     "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"]},

    {"_id": "item_americano", "name": "아메리카노", "base_price": 2000,
     "option_group_ids": ["opt_cafe_temp", "opt_cafe_size", "opt_cafe_shot", "opt_cafe_syrup"]},
# 라떼 커스텀 옵션 삭제
    {"_id": "item_latte_strawberry", "name": "딸기라떼", "base_price": 4000,
     "option_group_ids": ["opt_cafe_size", "opt_cafe_milk"]},
# 음료 커스텀 옵션 삭제 + 기본 음료선택 옵션 추가
    {"_id": "item_soda", "name": "음료", "base_price": 2000,  "option_group_ids": ["opt_drink"]},
    {"_id": "item_soju", "name": "소주", "base_price": 5000},
    {"_id": "item_beer", "name": "맥주", "base_price": 4000},

    {"_id": "item_rice_bowl", "name": "공기밥", "base_price": 1000},
    {"_id": "item_soup_extra", "name": "육수추가", "base_price": 3000}
]
option_groups = [

# 기본 옵션 추가, gukbap_soup 이름 size로 변경
  {"_id": "opt_gukbap_size", "group_name": "국밥 국물 양 선택", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0},  {"label": "국물 양 적게", "price": -1000}, {"label": "국물 양 많이", "price": 1000}]},

# 기본 옵션 추가
  {"_id": "opt_gukbap_dadaegi", "group_name": "국밥 다대기 조리 선택", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "다대기 따로 제공", "price": 0}]},

# 기본 옵션 추가
  {"_id": "opt_gukbap_rice", "group_name": "국밥 밥 조리 선택", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "밥 끓여서 제공", "price": 0}]},

# 기본 옵션 추가
  {"_id": "opt_ramen_toppings", "group_name": "라면 토핑 추가", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "치즈", "price": 200}, {"label": "계란", "price": 500}, {"label": "만두 (3개)", "price": 700}]},


{"_id": "opt_kimbap_topping_sausage", "group_name" : "토핑(소세지)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "햄 대신 소세지로 변경", "price": 1000}]},
{"_id": "opt_kimbap_topping_egg", "group_name" : "토핑(계란)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "계란 듬뿍 추가", "price": 500}]},
{"_id": "opt_kimbap_topping_tuna", "group_name" : "토핑(참치)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "참치 추가", "price": 500}]},
{"_id": "opt_kimbap_topping_pork", "group_name" : "토핑(돈까스)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "돈까스 한 줄 추가", "price": 500}]},
{"_id": "opt_kimbap_topping_cheese", "group_name" : "토핑(치즈)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "치즈 추가", "price": 200}]},
{"_id": "opt_kimbap_topping_ddukgalbi", "group_name" : "토핑(떡갈비)", "selection_type": "single",
  "choices": [{"label" : "기본", "price": 0}, {"label": "떡갈비 추가", "price": 1000}]},

  {"_id": "opt_dish_size", "group_name": "사이즈 선택", "selection_type": "single",
   "choices": [{"label": "기본", "price": 0}, {"label": "곱배기(대)", "price": 2000}]},

# 기본 옵션 추가
  {"_id": "opt_side_dish_extra", "group_name": "반찬 추가", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "단무지 추가", "price": 500}, {"label": "김치 추가", "price": 500}]},

  {"_id": "opt_cafe_temp", "group_name": "온도 선택", "selection_type": "single", "is_required": True,
   "choices": [{"label": "HOT", "price": 0}, {"label": "ICE", "price": 500}]},

# 기본 사이즈 제거
  {"_id": "opt_cafe_size", "group_name": "사이즈 변경", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "사이즈 업", "price": 1000}]},

# multiple -> single
  {"_id": "opt_cafe_shot", "group_name": "샷 추가", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "에스프레소 샷 추가", "price": 500}, {"label": "디카페인으로 변경", "price": 700}]},

# multiple -> single
  {"_id": "opt_cafe_syrup", "group_name": "시럽 추가", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "바닐라 시럽", "price": 500}, {"label": "헤이즐넛 시럽", "price": 500}]},

# 일반 우유 제거
  {"_id": "opt_cafe_milk", "group_name": "우유 변경", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "저지방 우유", "price": 0}, {"label": "두유", "price": 500},
               {"label": "오트밀크(귀리)", "price": 700}]},

  {"_id": "opt_bakery_packaging", "group_name": "포장", "selection_type": "single",
   "choices": [{"label": "개별 비닐 포장", "price": 0}, {"label": "선물용 상자 포장", "price": 1000}]},
# 그대로 제거
  {"_id": "opt_bakery_warming", "group_name": "데우기 서비스", "selection_type": "single",
   "choices": [{"label" : "기본", "price": 0}, {"label": "따뜻하게 데우기", "price": 0}]},

# 라면, 음료 선택 옵션 추가
  { "_id": "opt_ramen_spicy", "group_name": "라면 맵기 조절", "selection_type": "single", "choices": [{"label" : "기본", "price": 0}, {"label": "얼큰한 맛", "price": 0}] },
  { "_id": "opt_drink", "group_name": "음료 선택", "selection_type": "single", "choices": [{"label": "콜라", "price": 0}, {"label": "사이다", "price": 0}] }
]

#insert
# 데이터 삽입 함수로, 로컬 MongoDB을 기준으로 작동되는 함수이다.
# 위에서 저장된 매장 데이터를 DB에 저장
def insert_data():
    # 기존 데이터 삭제
    db["stores"].delete_many({})
    db["items"].delete_many({})
    db["option_groups"].delete_many({})

    # 새 데이터 삽입
    db["stores"].insert_many(stores)
    print("Stores 데이터 삽입 완료")

    db["option_groups"].insert_many(option_groups)
    print("Option Groups 데이터 삽입 완료")

    db["items"].insert_many(items)
    print("Items 데이터 삽입 완료")

    print("모든 데이터가 성공적으로 삽입되었습니다")

#select
def get_all_store_info():
    all_stores = list(db.stores.find({}))
    #return json.dumps(all_stores, ensure_ascii=False, indent=2)
    return all_stores
def get_all_menu_info():
    all_menus = list(db.items.find({}))
    return json.dumps(all_menus, ensure_ascii=False, indent=2)
def get_all_option_info():
    all_options = list(db.option_groups.find({}))
    return json.dumps(all_options, ensure_ascii=False, indent=2)

def get_store_info_by_id(id):
    all_stores = list(db.stores.find({}))
    store_data = all_stores[id]
    return store_data
def get_menu_info_by_id(menu_id):
    menu = db.items.find_one({"_id": menu_id})
    #return json.dumps(menu, ensure_ascii=False, indent=2)
    return menu
def get_option_info_by_id(option_id):
    option = db.option_groups.find_one({"_id": option_id})
    #return json.dumps(option, ensure_ascii=False, indent=2)
    return option

# 조회 테스트용 함수
# 저장된 모든 데이터를 조회 및 출력
def main():
    print(get_all_store_info())
    print(get_all_menu_info())
    print(get_all_option_info())
    None

# 테스트 코드
if __name__ == "__main__":
    #insert_data()      # 데이터 삽입 함수
    main()             # 데이터 조회 함수
    client.close()
