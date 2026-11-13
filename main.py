import json
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self, quizzes):
        self.quizzes = quizzes
        self.best_score = None

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()

    def read_text(self, prompt):
        while True:
            text = input(prompt).strip()

            if text:
                return text

            print("내용을 입력해 주세요.")

    def read_number(self, prompt, minimum, maximum):
        while True:
            text = input(prompt).strip()

            try:
                number = int(text)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue

            if minimum <= number <= maximum:
                return number

            print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()

            answer = self.read_number("정답 입력 (1~4): ", 1, 4)

            if quiz.check_answer(answer):
                print("정답입니다!")
                correct_count += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct_count / len(self.quizzes) * 100)
        print(
            f"\n결과: {len(self.quizzes)}문제 중 "
            f"{correct_count}문제 정답! ({score}점)"
        )

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")

            if not self.save_state():
                print("최고 점수를 파일에 저장하지 못했습니다.")

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")

        question = self.read_text("문제: ")
        choices = []

        for number in range(1, 5):
            choice = self.read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.read_number("정답 번호 (1~4): ", 1, 4)

        quiz = Quiz(question, choices, answer)
        self.quizzes.append(quiz)

        if self.save_state():
            print("퀴즈가 추가되고 저장되었습니다!")
        else:
            print("퀴즈는 추가됐지만 파일 저장에 실패했습니다.")

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    def validate_state(self, data):
        if not isinstance(data, dict):
            raise ValueError("저장 데이터는 딕셔너리여야 합니다.")

        if "quizzes" not in data or "best_score" not in data:
            raise ValueError("필수 저장 항목이 없습니다.")

        if not isinstance(data["quizzes"], list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        for item in data["quizzes"]:
            if not isinstance(item, dict):
                raise ValueError("퀴즈 형식이 올바르지 않습니다.")

            question = item.get("question")
            choices = item.get("choices")
            answer = item.get("answer")

            if not isinstance(question, str) or not question.strip():
                raise ValueError("문제 내용이 비어 있거나 잘못되었습니다.")

            if not isinstance(choices, list) or len(choices) != 4:
                raise ValueError("선택지는 4개여야 합니다.")

            for choice in choices:
                if not isinstance(choice, str) or not choice.strip():
                    raise ValueError("선택지 내용이 잘못되었습니다.")

            if type(answer) is not int or not 1 <= answer <= 4:
                raise ValueError("정답 번호는 1~4의 정수여야 합니다.")

        best_score = data["best_score"]

        if best_score is not None:
            if type(best_score) is not int or not 0 <= best_score <= 100:
                raise ValueError("최고 점수는 0~100의 정수여야 합니다.")

    def load_state(self):
        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.validate_state(data)

            loaded_quizzes = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in data["quizzes"]
            ]

        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")
            return

        except (OSError, ValueError, UnicodeError) as error:
            print(f"저장 데이터를 불러오지 못했습니다: {error}")
            print("기본 퀴즈로 시작합니다.")
            return

        self.quizzes = loaded_quizzes
        self.best_score = data["best_score"]
        print(f"저장 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
        }

        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"데이터를 저장하지 못했습니다: {error}")
            return False

        return True

    def run(self):
        while True:
            print("\n===== 카페 고객 응대 퀴즈 =====")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")

            choice = self.read_number("선택: ", 1, 5)

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("퀴즈 게임을 종료합니다.")
                break


quizzes = [
    Quiz(
        "주문과 다른 음료를 받았다는 고객에게 어떻게 응대할까요?",
        [
            "그냥 마시라고 한다",
            "주문 내역을 확인하고 잘못 제공했다면 사과 후 다시 만든다",
            "고객의 잘못이라고 단정한다",
            "아무 말 없이 음료를 가져간다",
        ],
        2,
    ),
    Quiz(
        "주문이 밀려 음료 준비가 늦어질 때 어떻게 할까요?",
        [
            "기다리는 고객을 무시한다",
            "무조건 곧 나온다고 말한다",
            "예상 대기 시간을 안내하고 양해를 구한다",
            "설명 없이 주문을 취소한다",
        ],
        3,
    ),
    Quiz(
        "고객이 특정 재료의 알레르기 유발 여부를 물으면 어떻게 할까요?",
        [
            "제품 표시와 원재료 정보를 확인하고 불확실한 점도 안내한다",
            "확인하지 않고 괜찮다고 한다",
            "소량이니 안전하다고 한다",
            "맛을 보고 판단하라고 한다",
        ],
        1,
    ),
    Quiz(
        "주문을 정확하게 접수하려면 어떻게 할까요?",
        [
            "고객의 말을 끝까지 듣지 않는다",
            "평소 인기 메뉴로 임의 변경한다",
            "온도와 크기는 확인하지 않는다",
            "메뉴, 수량, 온도와 추가 요청을 다시 확인한다",
        ],
        4,
    ),
    Quiz(
        "고객이 음료 맛에 불만을 말하면 먼저 어떻게 할까요?",
        [
            "다른 고객은 괜찮다고 말한다",
            "말을 끝까지 듣고 불편했던 내용을 확인한다",
            "고객과 논쟁한다",
            "설명 없이 자리를 피한다",
        ],
        2,
    ),
]

game = QuizGame(quizzes)

try:
    game.load_state()
    game.run()
except (KeyboardInterrupt, EOFError):
    print("\n입력이 중단되어 게임을 종료합니다.")
    game.save_state()