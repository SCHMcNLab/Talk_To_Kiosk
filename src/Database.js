const { MongoClient } = require('mongodb');


const uri = "";

const client = new MongoClient(uri);


const stores = [
  //아이디, 성호명, 메뉴들, 카테고리,주소, 여는 시간, 개업일, 포장&배달여부, 화장실여부, 매장 내 좌석, 주차, 와이파이, 결제수단, 할인, 셀프 이용
  {
    _id: "store_sch_coffee",
    name: "순천향커피",
    menu_item_ids: ["item_financier_plain","item_financier_soboru", "item_financier_caramel","item_financier_nunettine","item_canale","item_eggtart", "item_tigre",  "item_pretzel_almond","item_bagel_pizza", "item_americano", "item_latte_strawberry"],
    category: ["카페", "디저트"],
    address: {
      full: "충청남도 아산시 순냥대로 19, 1층",
      postal_code: "A13834"
    },
    phone: "123-333-330",
    operating_hours: [{
      day: "매일",
      open: "09:00",
      close: "20:00",
      break_time: null,
      last_order: "19:30"
    }],
    services: {
      takeout: true,
      delivery: false
    },
    self_service_info: "물과 냅킨, 시럽은 카운터 옆에 준비되어 있습니다.",
    amenities: {
      restroom: {
        available: true,
        details: "가게 내부, 남/녀 공용"
      },
      seating_capacity: 24,
      parking: {
        available: true,
        details: "건물 뒷편 전용 주차장 (3대 가능)"
      },
      wifi: {
        available: true,
        ssid: "sch_coffee_2g",
        password: "없음"
      }
    },
    payment_methods: ["카드", "현금", "아산사랑상품권", "카카오페이"],
    discounts: [{
      name: "텀블러 할인",
      details: "개인 텀블러 이용 시 모든 음료 300원 할인"
    }, {
      name: "오픈 이벤트",
      details: "베이커리 1만원 이상 구매 시 아메리카노 1잔 무료 (~11/30까지)"
    }]
  },
  {
    _id: "store_1year_gukbap",
    name: "1년 전통 국밥",
    menu_item_ids: ["item_gukbap_sundae",  "item_gukbap_naejang",  "item_gukbap_banban", "item_gukbap_makchang","item_plate_sundae","item_plate_naejang", "item_plate_banban","item_pork_cutlet_loin", "item_pork_cutlet_cheese",  "item_jeyuk_deopbap", "item_rice_bowl","item_soup_extra"],
    category: ["일반음식점", "국밥"],
    address: {
      full: "경기도 평택시 신장로 55, 1층",
      postal_code: "ab3921"
    },
    phone: "031-252-1211",
    operating_hours: [{
      day: "매일",
      open: "07:00",
      close: "22:00",
      break_time: null,
      last_order: "21:30"
    }],
    services: {
      takeout: true,
      delivery: false
    },
    self_service_info: "셀프바에서 반찬과 밥을 무료로 리필할 수 있습니다.",
    amenities: {
      restroom: {
        available: true,
        details: "매장 외부, 비밀번호 없음"
      },
      seating_capacity: 44,
      parking: {
        available: true,
        details: "최대 4대 가능"
      },
      wifi: {
        available: false,
        ssid: null,
        password: null
      }
    },
    payment_methods: ["경기페이", "카드", "현금"],
    discounts: [{
      name: "포장 할인",
      details: "포장 주문 시 1,000원 할인"
    }, {
      name: "단체 할인",
      details: "10만원 이상 결제 시 3% 할인"
    }]
  },
  {
    _id: "store_kimbap_script",
    name: "김밥스크립트",
    menu_item_ids: ["item_kimbap_general","item_kimbap_tuna","item_kimbap_pork_cutlet","item_kimbap_custom", "item_pork_cutlet_loin","item_pork_cutlet_cheese", "item_jeyuk_deopbap","item_ramen","item_udon", "item_soda", "item_soju","item_beer"],
    category: ["일반음식점", "분식", "김밥"],
    address: {
      full: "충청남도 아산시 용화로 35, 2층",
      postal_code: "aa3w42"
    },
    phone: "041-000-0000",
    operating_hours: [{
      day: "매일",
      open: "07:30",
      close: "20:00",
      break_time: null,
      last_order: "19:30"
    }],
    services: {
      takeout: true,
      delivery: true
    },
    self_service_info: "반찬코너, 정수기, 물컵이 준비되어 있습니다.",
    amenities: {
      restroom: {
        available: true,
        details: "매장 우측 상가 내에 위치합니다. 비밀번호는 1234 입니다."
      },
      seating_capacity: 32,
      parking: {
        available: true,
        details: "건물 주차장 이용 (승용차 5대)"
      },
      wifi: {
        available: false,
        ssid: null,
        password: null
      }
    },
    payment_methods: ["아산페이", "현금", "신용카드 (롯데카드 제외)"],
    discounts: [{
      name: "무료 배달",
      details: "3만원 이상 구매 시 1km 내 무료 배달"
    }]
  }
];
const items =[

  { "_id": "item_kimbap_general", "name": "제너럴 김밥", "base_price": 2000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_kimbap_tuna", "name": "참치김밥", "base_price": 3500, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_kimbap_pork_cutlet", "name": "돈까스김밥", "base_price": 3500, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_kimbap_custom", "name": "사용자 정의 김밥", "base_price": 3000,  "option_group_ids": ["opt_kimbap_custom_toppings", "opt_side_dish_extra"] },


  { "_id": "item_gukbap_sundae", "name": "순대국밥", "base_price": 9000, "option_group_ids": ["opt_gukbap_style", "opt_side_dish_extra"] },
  { "_id": "item_gukbap_naejang", "name": "내장국밥", "base_price": 9000, "option_group_ids": ["opt_gukbap_style", "opt_side_dish_extra"] },
  { "_id": "item_gukbap_banban", "name": "반반국밥", "base_price": 10000,  "option_group_ids": ["opt_gukbap_style", "opt_side_dish_extra"] },
  { "_id": "item_gukbap_makchang", "name": "막창국밥", "base_price": 12000, "option_group_ids": ["opt_gukbap_style", "opt_side_dish_extra"] },
  
 
  { "_id": "item_plate_sundae", "name": "순대한접시", "base_price": 15000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_plate_naejang", "name": "내장한접시", "base_price": 15000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_plate_banban", "name": "반반한접시", "base_price": 20000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_pork_cutlet_loin", "name": "등심돈까스", "base_price": 8000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_pork_cutlet_cheese", "name": "치즈돈까스", "base_price": 9000, "option_group_ids": ["opt_side_dish_extra"] },
  { "_id": "item_jeyuk_deopbap", "name": "제육덮밥", "base_price": 8000, "option_group_ids": ["opt_dish_size", "opt_side_dish_extra"] },
  
  
  { "_id": "item_ramen", "name": "라면", "base_price": 4000, "option_group_ids": ["opt_ramen_toppings", "opt_side_dish_extra"], "custom_options": [{"option_group_name": "맛 선택", "selection_type": "single", "is_required": true, "choices": [{ "label": "순한라면", "price": 0 }, { "label": "얼큰한라면", "price": 0 }] }] },
  { "_id": "item_udon", "name": "우동", "base_price": 6000, "option_group_ids": ["opt_side_dish_extra"] },
  
 
  { "_id": "item_financier_plain", "name": "플레인 휘낭시에", "base_price": 2500, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_financier_soboru", "name": "소보루 휘낭시에", "base_price": 2700, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_financier_caramel", "name": "솔티캐러멜 휘낭시에", "base_price": 2700, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_financier_nunettine", "name": "누네띠네 휘낭시에", "base_price": 2700, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_canale", "name": "까눌레", "base_price": 3000, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_eggtart", "name": "에그타르트", "base_price": 3500, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_tigre", "name": "티그레", "base_price": 3000, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_pretzel_almond", "name": "아몬드 프레첼", "base_price": 4500, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },
  { "_id": "item_bagel_pizza", "name": "피자 베이글", "base_price": 4900, "option_group_ids": ["opt_bakery_packaging", "opt_bakery_warming"] },


  { "_id": "item_americano", "name": "아메리카노", "base_price": 2000, "option_group_ids": ["opt_cafe_temp", "opt_cafe_size", "opt_cafe_shot", "opt_cafe_syrup"] },
  { "_id": "item_latte_strawberry", "name": "딸기라떼", "base_price": 4000, "option_group_ids": ["opt_cafe_size", "opt_cafe_milk"], "custom_options": [{"option_group_name": "온도 선택", "selection_type": "single", "is_required": true, "choices": [{ "label": "ICE", "price": 0 }] }] },
  { "_id": "item_soda", "name": "음료", "base_price": 2000, "custom_options": [{"option_group_name": "종류 선택", "selection_type": "single", "is_required": true, "choices": [{"label": "콜라", "price": 0}, {"label": "사이다", "price": 0}]}] },
  { "_id": "item_soju", "name": "소주", "base_price": 5000 },
  { "_id": "item_beer", "name": "맥주", "base_price": 4000 },

 
  { "_id": "item_rice_bowl", "name": "공기밥", "base_price": 1000 },
  { "_id": "item_soup_extra", "name": "육수추가", "base_price": 3000 }
];
const option_groups = [
  { "_id": "opt_gukbap_soup", "group_name": "국밥 국물 양 선택", "selection_type": "single", "choices": [{"label": "국물 양 많이", "price": 0}, {"label": "국물 양 보통", "price": 0}, {"label": "국물 양 적게", "price": 0}] },
  { "_id": "opt_gukbap_dadaegi", "group_name": "국밥 다데기", "selection_type": "single", "choices": [{"label": "다데기 같이", "price": 0}, {"label": "다대기 따로", "price": 0}] },
    { "_id": "opt_gukbap_rice", "group_name": "국밥 밥 조리 선택", "selection_type":"single", "choices": [{"label": "밥 따로(공기밥)", "price": 0}, {"label": "밥 같이 끓이기", "price": 0}] },
  { "_id": "opt_ramen_toppings", "group_name": "라면 토핑 추가", "selection_type": "single", "choices": [{"label": "치즈", "price": 200}, {"label": "계란", "price": 500}, {"label": "만두 (3개)", "price": 700}] },
  { "_id": "opt_kimbap_custom_toppings", "group_name": "나만의 김밥 재료 추가", "selection_type": "multiple", "choices": [{"label": "햄 대신 소세지로 변경", "price": 1000}, {"label": "계란 듬뿍 추가", "price": 500}, {"label": "참치 추가", "price": 500}, {"label": "돈까스 한 줄 추가", "price": 500}, {"label": "치즈 추가", "price": 200}, {"label": "떡갈비 추가", "price": 1000}] },
  { "_id": "opt_dish_size", "group_name": "사이즈 선택", "selection_type": "single", "choices": [{"label": "기본", "price": 0}, {"label": "곱배기(대)", "price": 2000}] },
  { "_id": "opt_side_dish_extra", "group_name": "반찬 추가", "selection_type": "multiple", "choices": [{"label": "단무지 추가", "price": 500}, {"label": "김치 추가", "price": 500}] },
  { "_id": "opt_cafe_temp", "group_name": "온도 선택", "selection_type": "single", "is_required": true, "choices": [{"label": "HOT", "price": 0}, {"label": "ICE", "price": 500}] },
  { "_id": "opt_cafe_size", "group_name": "사이즈 변경", "selection_type": "single", "choices": [{"label": "기본 사이즈", "price": 0}, {"label": "사이즈 업", "price": 1000}] },
  { "_id": "opt_cafe_shot", "group_name": "샷 추가", "selection_type": "multiple", "choices": [{"label": "에스프레소 샷 추가", "price": 500}, {"label": "디카페인으로 변경", "price": 700}] },
  { "_id": "opt_cafe_syrup", "group_name": "시럽 추가", "selection_type": "multiple", "choices": [{"label": "바닐라 시럽", "price": 500}, {"label": "헤이즐넛 시럽", "price": 500}] },
  { "_id": "opt_cafe_milk", "group_name": "우유 변경", "selection_type": "single", "choices": [{"label": "일반우유", "price": 0}, {"label": "저지방 우유", "price": 0}, {"label": "두유", "price": 500}, {"label": "오트밀크(귀리)", "price": 700}] },
  { "_id": "opt_bakery_packaging", "group_name": "포장", "selection_type": "single", "choices": [{"label": "개별 비닐 포장", "price": 0}, {"label": "선물용 상자 포장", "price": 1000}] },
  { "_id": "opt_bakery_warming", "group_name": "데우기 서비스", "selection_type": "single", "choices": [{"label": "그대로", "price": 0}, {"label": "따뜻하게 데우기", "price": 0}] }
];

async function run() {
  try {
    await client.connect();
    const database = client.db('TokiDB'); 

 
    
    await database.collection('stores').deleteMany({});
    await database.collection('stores').insertMany(stores);
    console.log('Stores 데이터 삽입 완료');

    await database.collection('option_groups').deleteMany({});
    await database.collection('option_groups').insertMany(option_groups);
    console.log('Option Groups 데이터 삽입 완료');

    await database.collection('items').deleteMany({});
    await database.collection('items').insertMany(items);
    console.log('Items 데이터 삽입 완료');

    console.log('모든 데이터가 성공적으로 삽입되었습니다');
  } finally {
    await client.close();
  }
}
run().catch(console.dir);
