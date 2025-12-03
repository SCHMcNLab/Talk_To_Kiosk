class ShoppingList:
    """
    장바구니 내 메뉴 항목들을 관리하는 클래스입니다.
    """

    # 생성자
    # 장바구니 리스트 초기화
    def __init__(self):
        """
        장바구니 초기화 (빈 리스트로 시작)
        """
        self.items = []

    # 장바구니 초기화 함수
    # 장바구니 사용이 끝난 시점(결제 or 그냥 사용 종료)에 호출
    def reset_data(self):
        self.items = []

    # 메뉴 추가 요청 함수 (메뉴 아이디, 수량, 옵션)
    # 이미 같은 옵션의 메뉴가 존재하면 수량만 증가
    # 존재하지 않는다면 장바구니에 추가
    def add(self, menu_id, quantity, option):
        """
        장바구니에 메뉴와 옵션을 추가합니다.
        동일 메뉴 및 옵션이 이미 존재하면 수량을 누적합니다.

        Args:
            menu_id (str): 메뉴 식별자
            quantity (int): 추가할 수량
            option (dict/list): 선택한 옵션 정보
        """
        for item in self.items:
            if item["id"] == menu_id and item["option"] == option:
                item["quantity"] += quantity
                return
        self.items.append({
            "id": menu_id,
            "quantity": quantity,
            "option": option
        })

    # 옵션 변경 요청 함수 (메뉴 아아디, 기존 옵션, 새로운 옵션)
    # 넘겨받은 아이디와 기존 옵션 값에 맞는 메뉴가 존재할 경우, 새 옵션으로 변경
    def change_option(self, menu_id, option, new_option):
        """
        장바구니 내 특정 메뉴 항목의 옵션을 변경합니다.

        Args:
            menu_id (str): 메뉴 식별자
            option (dict/list): 현재 옵션 정보
            new_option (dict/list): 변경할 새로운 옵션 정보
        """
        for item in self.items:
            if item["id"] == menu_id and item["option"] == option:
                item["option"] = new_option
                break

    # 메뉴 삭제 요청 함수 ( 메뉴 아이디, 옵션 )
    # 넘겨받은 아이디와, 옵션 값에 맞는 메뉴가 존재할 경우 장바구니에서 삭제
    def delete(self, menu_id, option):
        """
        특정 메뉴 항목을 장바구니에서 삭제합니다.

        Args:
            menu_id (str): 메뉴 식별자
            option (dict/list): 삭제할 옵션 정보
        """
        self.items = [
            item for item in self.items
            if not (item["id"] == menu_id and item["option"] == option)
        ]

    # 현재 장바구니에 저장된 id 값(리스트)을 반환해주는 함수
    # UI 렌더링 기능 구현 시에 사용될 예정
    def get_items(self):
        """
        장바구니에 담긴 모든 항목을 반환합니다.

        Returns:
            list: 장바구니 항목 리스트
        """
        return self.items

    # 단순하게 저장된 값들을 출력하는 함수(디버깅 목적)
    # 추후에 삭제할 예정
    def print_all_list_info(self):
        """
        장바구니 내 모든 항목을 출력하는 디버그용 함수입니다.
        """
        if not self.items:
            print("장바구니가 비어있습니다.")
        else:
            for item in self.items:
                print(item)
