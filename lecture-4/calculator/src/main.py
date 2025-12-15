import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.AMBER_100
        self.color = ft.Colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                # 追加: 科学計算行
                ft.Row(
                    controls=[
                        SciButton(text="sin", button_clicked=self.button_clicked),
                        SciButton(text="cos", button_clicked=self.button_clicked),
                        SciButton(text="tan", button_clicked=self.button_clicked),
                        SciButton(text="x^2", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        SciButton(text="√", button_clicked=self.button_clicked),
                        SciButton(text="1/x", button_clicked=self.button_clicked),
                        SciButton(text="x^y", button_clicked=self.button_clicked),
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        # print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand is True:
                # 小数点の重複防止
                if data == ".":
                    self.result.value = "0."
                else:
                    self.result.value = data
                self.new_operand = False
            else:
                # 小数点の重複防止
                if data == "." and "." in self.result.value:
                    pass
                else:
                    self.result.value = self.result.value + data

        # 基本演算子
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(self.operand1, self._to_float(self.result.value), self.operator)
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = 0.0
            else:
                self.operand1 = self._to_float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(self.operand1, self._to_float(self.result.value), self.operator)
            self.reset()

        elif data == "%":
            self.result.value = self._safe_format(self._to_float(self.result.value) / 100.0)
            self.reset()

        elif data == "+/-":
            val = self._to_float(self.result.value)
            if val > 0:
                self.result.value = "-" + str(self._safe_format(val))
            elif val < 0:
                self.result.value = str(self._safe_format(abs(val)))

        # 科学計算
        elif data == "sin":
            val = self._to_float(self.result.value)
            self.result.value = self._safe_format(math.sin(val))
            self.new_operand = True

        elif data == "cos":
            val = self._to_float(self.result.value)
            self.result.value = self._safe_format(math.cos(val))
            self.new_operand = True

        elif data == "tan":
            val = self._to_float(self.result.value)
            # tan の特異点に注意（ラジアンで pi/2 + k*pi）
            try:
                self.result.value = self._safe_format(math.tan(val))
            except Exception:
                self.result.value = "Error"
            self.new_operand = True

        elif data == "x^2":
            val = self._to_float(self.result.value)
            self.result.value = self._safe_format(val * val)
            self.new_operand = True

        elif data == "√":
            val = self._to_float(self.result.value)
            if val < 0:
                self.result.value = "Error"
            else:
                self.result.value = self._safe_format(math.sqrt(val))
            self.new_operand = True

        elif data == "1/x":
            val = self._to_float(self.result.value)
            if val == 0:
                self.result.value = "Error"
            else:
                self.result.value = self._safe_format(1.0 / val)
            self.new_operand = True

        elif data == "x^y":
            # 累乗演算に切り替え（次に入力する値を指数として扱う）
            self.result.value = self.calculate(self.operand1, self._to_float(self.result.value), self.operator)
            # 累乗専用の演算子として "^" を使う
            self.operator = "^"
            if self.result.value == "Error":
                self.operand1 = 0.0
            else:
                self.operand1 = self._to_float(self.result.value)
            self.new_operand = True

        self.update()

    def _to_float(self, s):
        try:
            return float(s)
        except Exception:
            return float("nan")

    def _safe_format(self, num):
        # NaN や Inf の表示対策
        if isinstance(num, float) and (math.isnan(num) or math.isinf(num)):
            return "Error"
        return str(self.format_number(num))

    def format_number(self, num):
        if isinstance(num, str):
            return num
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
        elif operator == "^":
            # 累乗（x^y）
            try:
                return self.format_number(math.pow(operand1, operand2))
            except Exception:
                return "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0.0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator"
    calc = CalculatorApp()
    page.add(calc)


if __name__ == "__main__":
    ft.app(main)