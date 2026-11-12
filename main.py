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
        self.best_score = 0

    def show_quizzes(self):
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()    
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
game.show_quizzes()