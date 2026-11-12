class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")


quiz = Quiz(
    "고객이 주문한 음료와 다른 음료를 받았다고 하면 어떻게 할까요?",
    [
        "고객에게 그냥 마시라고 한다",
        "주문 내역을 확인하고 잘못 제공했다면 사과 후 다시 만든다",
        "다른 직원의 잘못이라고 말한다",
        "아무 말 없이 음료를 가져간다",
    ],
    2,
)

quiz.display()