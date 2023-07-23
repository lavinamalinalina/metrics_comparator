import sys
import os
def read_file_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def find_missing_metrics(file1_lines, file2_lines):             #функция ищет метрики из первого файла, не совпадающие со вторым
    missing_metrics = []
    missing_metrics.append('         МЕТРИКИ ИЗ ПЕРВОГО ДАШБОРДА, ФОРМУЛА КОТОРЫХ НЕ СОВПАДАЕТ НИ С ОДНОЙ ИЗ ВТОРОГО:')
    missing_metrics.append('\n')
    missing_metrics.append('\n')
    for i in range(0, len(file1_lines)):                        #сравниваем строки с expr в двух файлах
        if '"expr"' in file1_lines[i]:
            if file1_lines[i] not in file2_lines:               #если метрики из первого файла нет во втором, пишем метрику из первого файла 
                missing_metrics.append(f'{file1_lines[i]}')
                for line in file1_lines[i+1:i+12]:              #ищем параметры метрики в большом диапазоне начиная со следующей строки после expr (12 рандомный большой диапазон)
                    if line.lstrip().startswith(("\"refId\"", "\"legendFormat\"", "\"hide\"")):
                        missing_metrics.append(line)
                    if line.lstrip().startswith(("\"expr\"")):   
                        break                                   #выходим из цикла, если дошли до следующей метрики ("expr")                                                 
                missing_metrics.append('\n')
    return missing_metrics
    
def hide_counter(file1_lines, file2_lines):                     #функция считает видимые метрики и подробно записывает скрытые из обоих файлов
   metrics = []         #видимые
   hidden_metrics = []  #скрытые
   
   counter1 = 0         #счётчики видимых метрик
   counter2 = 0
   hidden_metrics.append(f'--- Скрытые метрики из первого дашборда: \n\n')

   for i in range(0, len(file1_lines)):
        if '"expr"' in file1_lines[i]:                                              #если в первом файле строка с expr...
            if not any('"hide": true' in line for line in file1_lines[i:i+4]):      # ...то если в следую щих после неё 4-х нету "hide": true'...
                counter1 += 1                                                       #... то добавить счётчик видимых
            else:
                hidden_metrics.append(f'{file1_lines[i]}')
                for line in file1_lines[i+1:i+12]:                                  #переиспользование цикла выше, можно оптимизировать и вынести его в функцию
                    if line.lstrip().startswith(("\"refId\"", "\"legendFormat\"", "\"hide\"")):
                        hidden_metrics.append(line)
                    if line.lstrip().startswith(("\"expr\"")):   
                        break                                                                                  
                hidden_metrics.append('\n')
   
   metrics.append(f'--- Видимых метрик (hide != true) в первом дашборде: {counter1} --- \n\n')
 
   
   hidden_metrics.append(f'--- Скрытые метрики из второго дашборда: \n\n')
   for i in range(0, len(file2_lines)):
        if '"expr"' in file2_lines[i]: 
            if not any('"hide": true' in line for line in file2_lines[i:i+4]):
                counter2 += 1
            else:
                hidden_metrics.append(f'{file2_lines[i]}')
                for line in file2_lines[i+1:i+12]:                                  #переиспользование х3
                    if line.lstrip().startswith(("\"refId\"", "\"legendFormat\"", "\"hide\"")):
                        hidden_metrics.append(line)
                    if line.lstrip().startswith(("\"expr\"")):   
                        break                                                                                  
                hidden_metrics.append('\n')
   
   metrics.append(f'--- Видимых метрик (hide != true) во втором дашборде: {counter2} ---\n\n\n\n')
   
   
   return metrics, hidden_metrics

def main():
    folder_name = os.path.basename(os.getcwd()) #текущая папка
    file1_path = sys.argv[1]  #ввод имени файла из терминала
    file2_path = sys.argv[2]
    
    file1_lines = read_file_lines(file1_path) 
    file2_lines = read_file_lines(file2_path)
    
    missing_metrics = find_missing_metrics(file1_lines, file2_lines) #получаем из функции метрики, которые отличаются во втором дашборде
    metrics, hidden_metrics = hide_counter(file1_lines, file2_lines) #получаем из функции видимые и скрытые метрики каждого дашборда
    
    with open(f'{folder_name}.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(f"{'='*20} {folder_name} {'='*20}\n\n") #записывает имя текущей папки в начале
        if missing_metrics:
            output_file.writelines(missing_metrics)
        else:
            output_file.write("все метрики первого дашборда есть во втором")
    
        output_file.writelines(metrics)
        output_file.writelines(hidden_metrics)

if __name__ == "__main__":
    main()
