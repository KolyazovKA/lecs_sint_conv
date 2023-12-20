from analyzator import *
from sint_an import *
from convolution import convolution_tasks, output_results

file_name = "WithoutErrors.txt"


def main():
	reader = Reader(file_name)
	lecs = lecs_analizator(reader)
	sint_analyzator(lecs, reader)
	conv(lecs, reader.lines, lecs.numbs_of_str)

def conv(lecs, lines, numbs):
	if len(lecs.err_message) == 0:
		for i in range(len(lines)):
			for j in range(len(lines[i+1])):
				convolution_tasks(lines[i + 1][j], numbs)
		output_results()

def sint_analyzator(lecs, reader):
	if len(lecs.err_message) == 0:
		print(f"\n\nСинтаксический анализатор")
		for i in range(len(reader.lines)):
			for j in range(len(reader.lines[i + 1])):
				print(f"Исходная строка: {reader.lines[i + 1][j]}")
				a = reader.lines[i + 1][j]
				reader.lines[i + 1][j] = a.replace(" ", "")
				start_str = reader.lines[i + 1][j][:3]
				body = reader.lines[i + 1][j][3:-1]
				body = analis(body, start_str)

				start_str += body
				execute_rule1(start_str)
				print("Список применнных правил")
				for i in list_rules:
					print(i, end="->")
				print('end')
				for i in range(len(list_rules)):
					list_rules.pop(0)


def lecs_analizator(reader):
	print(f"\n\n\t\t\t\t\t\tТаблица лексем")
	lecs = Analyzator(reader.lines)
	return lecs


if __name__ == '__main__':
	main()


