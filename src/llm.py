from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria
import torch
import time
import re

'''
사용 패키지 정의
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126  <<< 이때, 버전에 따라 마지막 숫자가 달라집니다. 저는 12.9라서 129입니다.
pip install transformers
pip install accelerate
'''

# JSON 균형 체크용 StoppingCriteria
# LLM의 출력 도중 JSON 형식이 완성되면 출력을 중지시키기 위한 클래스
# 중괄호 쌍이 전부 완성되는 순간이 조건
class StopOnJSONBalanced(StoppingCriteria):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.buffer = ""
        self.open_count = 0

    def __call__(self, input_ids, scores, **kwargs):
        last_token_id = input_ids[0, -1].item()
        last_token = self.tokenizer.decode([last_token_id], skip_special_tokens=True)
        self.buffer += last_token

        self.open_count += last_token.count("{")
        self.open_count -= last_token.count("}")

        if self.open_count <= 0 and "{" in self.buffer:
            return True
        return False


class KioskAI:
    '''
     키오스크 AI LLM 클래스
     - OpenAI API 연동 및 대화 히스토리 관리
     - 매장, 메뉴, 옵션 데이터 요약 함수 포함
     - 사용자 입력에 따라 LLM 질의 메시지 생성 및 응답 처리
     '''

    def __init__(self, prompt):
        '''
        초기화
        - 대화 이력 리스트 초기화
        - 모델 초기화, 토크나이저 및 모델 로드
        '''
        self.model_name = "Qwen/Qwen3-4B"

        # 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # 모델 로드
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            offload_folder="offload_dir"
        )
        self.prompt = prompt
        self.conversation_history = self.prompt
        self.stopping_criteria = StopOnJSONBalanced(self.tokenizer)

    # history 초기화 함수
    # 초기에는 prompt만 단일로 존재(대화 내역 X)
    def reset_history(self):
        self.conversation_history = self.prompt

    # llm 출력 후처리
    # 기존의 OpenAI 기준에서 다소 발생하던 출력에서 ```와 같은 문자으의 출력이 발견되어 추가한 함수
    # 다른 모델에서도 발생 가능성이 있으므로 삭제하지 않았음
    def extract_json_from_response(self, md_text):
        '''
        LLM 응답의 마크다운 포맷 내 JSON 코드블럭에서
        JSON 문자열만 추출

        Args:
            md_text (str): 마크다운 형식의 문자열

        Returns:
            str: JSON 문자열 (찾지 못하면 원본 문자열 반환)
        '''
        pattern = r"```json\s*(\{.*?\})\s*```"
        match = re.search(pattern, md_text, re.DOTALL)
        if match:
            return match.group(1)
        return md_text

    def ask(self, user_input):
        '''
        사용자 메시지를 받아 최종 메시지 배열 생성 후
        OpenAI API에 요청하여 응답받고,
        응답 내 JSON 부분을 추출하여 반환

        Args:
            user_input (str): 사용자 입력 텍스트

        Returns:
            str: OpenAI 응답 내 JSON 문자열
        '''

        self.conversation_history += f"\nuser : {user_input}\nassistant :"

        # 입력 토큰화
        inputs = self.tokenizer(self.conversation_history, return_tensors="pt").to(self.model.device)

        # 생성 시작 시간 측정 (디버깅 용도)
        start_time = time.time()

        # 응답 생성
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=500,  # 충분히 늘림
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=[self.stopping_criteria]  # JSON 균형 체크
        )

        # 생성 시간 측정(디버깅 용도)
        elapsed = time.time() - start_time

        # 출력 처리
        input_length = inputs["input_ids"].shape[1]
        generated_ids = outputs[0]
        assistant_response = self.tokenizer.decode(generated_ids[input_length:], skip_special_tokens=True).strip()

        # 사용자에게 출력
        print(f"⏱ 생성 시간: {elapsed:.2f}초")

        # 다음 턴을 위해 히스토리에 추가
        self.conversation_history += f" {assistant_response}"
        return self.extract_json_from_response(assistant_response)

# 모듈 테스트
if __name__ == "__main__":
    prompt = "" # 프롬프트를 작성 후 생성자에 삽입
    llm_model = KioskAI(prompt) # KioskAI 객체 생성
    input_text = input("사용자 : ") # 사용자로부터 텍스트 입력
    result_text = llm_model.ask(input_text) # 입력된 텍스트 기반 추론 생성
    print(result_text) # 추론 결과 출력

