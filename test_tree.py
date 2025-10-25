import unittest
import tempfile
import os
import io
import sys
from tree import mk, main


class TestPriemkaElki(unittest.TestCase):

    # - тесты функции mk-
    def test1strud(self):
        "Проверка записи штруделя"
        result = mk(4).splitlines()[2:-2]  # только листья
        ats = [line.strip().startswith("@") for line in result if "@" in line]
        # Должно чередоваться True/False
        for i in range(1, len(ats)):
            self.assertNotEqual(ats[i], ats[i - 1])

    def test2str(self):
        "Проверяем структуру одноэтажной елки"
        result = mk(1).strip().splitlines()
        self.assertEqual(result[0].strip(), "W")
        self.assertIn("*", result[1])
        self.assertTrue(result[-1].strip().startswith("TT"))

    def test3number_lines(self):
        "Проверяем соответствие строк и формулы"
        floors = 5
        expected_lines = 1 + (2 * floors - 1) + 2  # W + листья + 2 основания
        result = mk(floors).splitlines()
        self.assertEqual(len(result), expected_lines)

    def test4simm(self):
        "Проверка елки на симметричность"
        result = mk(4).splitlines()
        # проверяем по длинне
        widths = [len(line.rstrip("\n")) for line in result]
        self.assertTrue(all(abs(widths[i] - widths[-1]) < 2 for i in range(len(widths)//2)))

    def test5bad_floor(self):
        "Проверяем выдает ли ошибку, если этажей меньше 1"
        with self.assertRaises(ValueError):
            mk(0)

    def test6stvol(self):
        "Проверка ствола"
        result = mk(3).strip().splitlines()
        trunk1, trunk2 = result[-2:]
        self.assertEqual(trunk1.strip(), trunk2.strip())
        self.assertIn("TTTTT", trunk1)

    def test7lastlevel(self):
        "Проверка основы ствола"
        lines = mk(3).splitlines()
        lengths = [len(l) for l in lines]
        self.assertEqual(max(lengths), len(lines[-3]))  # последняя строка листвы — самая длинная

    def test8new_stroka(self):
        """Результат должен заканчиваться переводом строки"""
        out = mk(2)
        self.assertTrue(out.endswith("\n"))

    # -Тесты основы -
    def test_main_creates_file(self):
        "main() создает файл с елкой"
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        argv = ["3", tmp.name]
        sys_stdout = io.StringIO()
        sys_stderr = io.StringIO()
        sys_stdout_old, sys_stderr_old = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = sys_stdout, sys_stderr
        try:
            main(argv)
        finally:
            sys.stdout, sys.stderr = sys_stdout_old, sys_stderr_old
        # Проверяем, что файл не просто создан, а еще и не пустой
        with open(tmp.name, encoding="utf-8") as f:
            data = f.read()
        os.remove(tmp.name)
        self.assertIn("W", data)
        self.assertIn("*", data)
        self.assertIn("TTTTT", data)

    def test_main_invalid_argument(self):
        "main() с неверным параметром, например не числом , завершается ошибкой"
        argv = ["abc", "output.txt"]
        captured = io.StringIO()
        sys_stdout_old, sys_stderr_old = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = captured, captured
        with self.assertRaises(SystemExit):
            main(argv)
        sys.stdout, sys.stderr = sys_stdout_old, sys_stderr_old

    def test_main_wrong_args_count(self):
        "main() без аргументов должно выводить ошибку"
        captured = io.StringIO()
        sys_stdout_old, sys_stderr_old = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = captured, captured
        with self.assertRaises(SystemExit):
            main([])
        sys.stdout, sys.stderr = sys_stdout_old, sys_stderr_old
        output = captured.getvalue()
        self.assertIn("python tree.py", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)