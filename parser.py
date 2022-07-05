import subprocess
import datetime


def report():
    ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True).communicate()[0].split("\n")

    psm = subprocess.Popen(['ps', 'aux', '--sort', 'pmem'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True).communicate()[0].split("\n")

    psc = subprocess.Popen(['ps', 'aux', '--sort', 'pcpu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True).communicate()[0].split("\n")
    resource_list = []
    users_list = []
    mem_size_list = []
    cpu_load_list = []
    mem_list = []
    cpu_list = []
    max_mem_format = 0
    max_cpu_format = 0
    mem_list.append(psm)
    cpu_list.append(psc)
    n = len(ps[0].split()) - 1
    for i in ps[1:-1]:
        resource_list.append(i.split(None, n))
    for i in resource_list:
        users_list.append(i[0])
    for i in resource_list:
        mem_size_list.append(int(i[5]))
    for i in resource_list:
        cpu_load_list.append(float(i[2]))
    for i in mem_list:
        mem_list = (i.pop(int(len(i)) - 2)).split()
        max_mem_format = str((mem_list[3] + '%, ' + mem_list[10])[:27])
    for i in cpu_list:
        cpu_list = (i.pop(int(len(i)) - 2)).split()
        max_cpu_format = str((cpu_list[2] + '%, ' + cpu_list[10])[:27])
    users = list(set(users_list))
    users_dict = dict((x, users_list.count(x)) for x in set(users_list))
    users_format = str(", ".join(users))
    count_format = str(len(ps))
    users_dict_format = str("\n".join("{!r}: {!r}".format(k, v) for k, v in users_dict.items()))
    mem_format = str(round((sum(mem_size_list) / 1024), 1))
    cpu_format = str(round(sum(cpu_load_list), 1))
    report = "Отчёт о состоянии системы: \n"
    report += "Пользователи системы: " + users_format + "\n"
    report += "Процессов запущено: " + count_format + "\n"
    report += "Пользовательских процессов: \n" + users_dict_format + "\n"
    report += "Всего памяти используется: " + mem_format + " mb\n"
    report += "Всего CPU используется: " + cpu_format + "%\n"
    report += "Больше всего памяти использует: " + max_mem_format + "\n"
    report += "Больше всего CPU использует: " + max_cpu_format + "\n"
    return report


def date_format():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y-%H:%M")


def out_to_file():
    with open(f'{date_format()}-scan.txt', 'w+') as file:
        file.write(f'{report()}')


if __name__ == '__main__':
    out_to_file()
