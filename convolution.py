from sint_an import IND_AND_CHARS
import re


values = ["11BD", "AA", "2"]
# Значения идентификаторов
vars_and_values = {}
# Список проведенных операций
operations = []
minimaze_operations = {}
deleted_operations = []
# Значения заменяемых идентификаторов и чисел
xs = {}
# Количество операций
step = 0

def find_key_by_value(value):
	for key, val in vars_and_values.items():
		if val == value:
			return key
	return len(operations)-1

def append_in_min_oper(oper, numb1):
	flag = True
	for key, val in vars_and_values.items():
		if val == numb1:
			numb1 = key
			flag = False
			break
	if flag:
		numb1 = len(minimaze_operations)-1
		if minimaze_operations[numb1] in minimaze_operations.keys():
			if numb1 in deleted_operations:
				numb1 = minimaze_operations[numb1]
		else:
			x = 0
			for del_op in deleted_operations:
				if numb1 > del_op:
					x += 1
			numb1 -= x
	for key, val in minimaze_operations.items():
		if f"{oper}: ({numb1})" == val:
			for key1, val1 in minimaze_operations.items():
				if val1 == key:
					return
			minimaze_operations[len(minimaze_operations)] = key
			deleted_operations.append(len(minimaze_operations)-1)
			return
	minimaze_operations[len(minimaze_operations)] = f"{oper}: ({numb1})"

def append_in_min_oper_for_two_numb(oper, numb1, numb2):
	global count_of_deleted_operations
	flag1 = True
	flag2 = True
	for key, val in vars_and_values.items():
		if val == numb1:
			numb1 = key
			flag1 = False
			break
	if flag1:
		numb1 = len(minimaze_operations)-1
		if minimaze_operations[numb1] in minimaze_operations.keys():
			if numb1 in deleted_operations:
				numb1 = minimaze_operations[numb1]
		else:
			x = 0
			for del_op in deleted_operations:
				if numb1 > del_op:
					x += 1
			numb1 -= x

	for key, val in vars_and_values.items():
		if val == numb2:
			numb2 = key
			flag2 = False
			break
	if flag2:
		numb2 = len(minimaze_operations)-1
		if minimaze_operations[numb2] in minimaze_operations.keys():
			if numb2 in deleted_operations:
				numb2 = minimaze_operations[numb2]
		else:
			x = 0
			for del_op in deleted_operations:
				if numb2 > del_op:
					x += 1
			numb2 -= x

	for key, val in minimaze_operations.items():
		if f"{oper}({numb1}, {numb2})" == val:
			minimaze_operations[len(minimaze_operations)] = key
			deleted_operations.append(len(minimaze_operations)-1)
			return
	minimaze_operations[len(minimaze_operations)] = f"{oper}({numb1}, {numb2})"

def execute_rule1(string, start_str):
	vars_and_values[start_str[0]] = xs[string]
	operations.append(f":= ({start_str[0]}, {find_key_by_value(string)})")
	minimaze_operations[len(minimaze_operations)] = f":= ({start_str[0]}, {str(int(find_key_by_value(string) - len(deleted_operations) - 1))})"

def execute_rule2(string, count):
	numb1, numb2 = find_numbs(string)
	string = re.sub(r'X\d+\+X\d+', f'X{count}', string)
	xs[f'X{count}'] = hex_sum(numb1, numb2)
	operation = f"+: ({find_key_by_value(numb1)}, {find_key_by_value(numb2)})"
	operations.append(operation)
	append_in_min_oper_for_two_numb("+: ", numb1, numb2)
	return string

def find_numbs(string):
	numb1 = None
	numb2 = None
	flag = False
	for i in xs.keys():
		if flag:
			if i in string:
				numb2 = xs[i]
		else:
			if i in string:
				numb1 = xs[i]
				flag = True
	return numb1, numb2


def execute_rule4(string, count):
	numb1, numb2 = find_numbs(string)
	string = re.sub(r'X\d+\*X\d+', f'X{count}', string)
	xs[f'X{count}'] = hex_mult(numb1, numb2)
	operations.append(f"*: ({find_key_by_value(numb1)}, {find_key_by_value(numb2)})")
	append_in_min_oper_for_two_numb("*: ", numb1, numb2)
	return string

def find_numb_for_dividion(string):
	s = re.search(r'X\d+/\s*X\d+', string)
	s = s.group(0)
	s = s.split('/')
	numb1 = xs[s[0]]
	numb2 = xs[s[1]]
	return numb1, numb2

def execute_rule5(string, count):
	numb1, numb2 = find_numb_for_dividion(string)
	string = re.sub(r'X\d+/\s*X\d+', f'X{count}', string)
	xs[f'X{count}'] = hex_dividing(numb1, numb2)
	operations.append(f"/: ({find_key_by_value(numb1)}, {find_key_by_value(numb2)})")
	append_in_min_oper_for_two_numb("/: ", numb1, numb2)
	return string

def execute_rule7(string, count):
	numb = None
	for i in xs.keys():
		if i in string:
			numb = xs[i]

	string = re.sub(r'\(X\d+\)', f'X{count}', string)
	xs[f"X{count}"] = numb
	return string

def execute_rule8(string, count):
	numb = ""
	for i in xs.keys():
		if i in string:
			if xs[i][0] != "-":
				numb += xs[i]
			else:
				numb = xs[i][1:]

	string = re.sub(r'-X\d+', f'X{count}', string)
	xs[f"X{count}"] = "-" + numb
	operations.append(f"-: ({find_key_by_value(numb)})")
	append_in_min_oper("-", numb)
	return string

def execute_rule9(string, i, count):
	string = string.replace(i, f"X{count}", 1)
	try:
		xs[f"X{count}"] = vars_and_values[i]
	except:
		xs[f"X{count}"] = i
	return string


def find_and_replace(string, count):
	i = find_var_or_numb(string)
	string = execute_rule9(string, i, count)
	return string


def find_var_or_numb(string: str) -> str:
	for i in vars_and_values.values():
		if i in string:
			return i
	for i in vars_and_values.keys():
		if i in string:
			return i
	result = ""
	for i in values:
		if i in string:
			return i
	return result


def hex_sum(str1, str2):
	num1 = int(str1, 16)
	num2 = int(str2, 16)
	result = num1 + num2
	if result > 0:
		return str(hex(result)[2:]).upper()
	else:
		result = -1 * result
		return "-" + str(hex(result)[2:]).upper()


def hex_mult(str1, str2):
	num1 = int(str1, 16)
	num2 = int(str2, 16)
	result = num1 * num2
	if result > 0:
		return str(hex(result)[2:]).upper()
	else:
		result = -1 * result
		return "-" + str(hex(result)[2:]).upper()


def hex_dividing(str1, str2):
	try:
		result = int(str1, 16) / int(str2, 16)
		return str(hex(int(result))[2:]).upper()
	except ValueError:
		return "Ошибка: неверный формат числа"
	except ZeroDivisionError:
		return "Ошибка: деление на ноль"


def check_sum_of_X(input_string):
	pattern = r'X\d+\+X\d+'
	match = re.search(pattern, input_string)
	return bool(match)


def check_mult_of_X(input_string):
	pattern = r'X\d+\*X\d+'
	match = re.search(pattern, input_string)
	return bool(match)


def check_dividing_of_X(input_string):
	pattern = r'X\d+\/X\d+'
	match = re.search(pattern, input_string)
	return bool(match)


def check_brackets_of_X(input_string):
	pattern = r'\(X\d+\)'
	match = re.search(pattern, input_string)
	return bool(match)


def check_minus_of_X(input_string):
	pattern = r'-X\d+'
	match = re.search(pattern, input_string)
	return bool(match)


def convolution_tasks(string, numbs):
	string = string.replace(" ", "")
	header = string[:3]
	body = string[3:-1]
	var = string[0]

	finish_str = re.compile(r'X\d+')
	if body in numbs:
		vars_and_values[var] = body
		operations.append(f":= ({var},{body})")
		minimaze_operations[len(minimaze_operations)] = f":= ({var},{body})"
	else:
		xs.clear()
		count = 0
		while not finish_str.fullmatch(body):
			count += 1
			if check_minus_of_X(body):
				body = execute_rule8(body, count)
			elif check_mult_of_X(body):
				body = execute_rule4(body, count)
			elif check_dividing_of_X(body):
				body = execute_rule5(body, count)
			elif check_brackets_of_X(body):
				body = execute_rule7(body, count)
			elif check_sum_of_X(body):
				body = execute_rule2(body, count)
			else:
				body = find_and_replace(body, count)
		execute_rule1(body, header)



def output_results():
	# вывод свертки
	print("\nВыполнение свертки")
	for i in range(len(operations)):
		print(f"{i}) {operations[i]}")
	# Вывод значений переменных
	print("\nВывод таблицы Т")
	for i in vars_and_values.keys():
		print(f"{i} = {vars_and_values[i]}")
	# Вывод без лишних операций
	print("\nВыполенение исключения лишних операций")
	x = 0
	for i in minimaze_operations.keys():
		if i in deleted_operations:
			continue
		else:
			print(x, f") {minimaze_operations[i]}")
			x += 1


if __name__ == "__main__":
	values = ["11BD", "AA", "22"]
	convolution_tasks("a := 11BD;", values)
	convolution_tasks("b := 22;", values)
	convolution_tasks("d := - (a / b);", values)
	convolution_tasks("e := - (d + b) + d + b + (a / b);", values)
	convolution_tasks("f := - (a + b);", values)
	convolution_tasks("g := - (a + b);", values)
	convolution_tasks("h := - (a);", values)

	output_results()
