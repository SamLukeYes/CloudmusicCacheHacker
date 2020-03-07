import os, sys
from time import sleep
from easygui import msgbox, diropenbox
#from progressbar import ProgressBar
from urllib.request import urlopen
#from threading import Thread, RLock

null = None
true = True
false = False
#print_lock = RLock()
#exception_lock = RLock()
#name_lock = RLock()
oops = []
invalid = r'/\:*"<>|?'
finished = 0
bar_value = 0
bar_len = 50
percentage = 0

# def thread_print(*args):
#     print_lock.acquire()
#     print(*args)
#     print_lock.release()

def print_bar(string):
    print(string, end=f'{" "*(bar_len+7-len(string))}\n') #由于存在中文字符，这样仍然不够完美
    #print(string, end=f'{" "*bar_len}\n')
    print(f'|{">"*bar_value}{"="*(bar_len-bar_value)}| {percentage*100:.1f}%', end='\r')

def name_mp3(name):
    #name_lock.acquire() #记得调用这个函数后要释放锁！
    count = 0
    file_name = f'{name}.mp3'
    while os.path.isfile(f'{output_dir}/{file_name}'):
        count += 1
        file_name = f'{name} ({count}).mp3'
    return file_name

def decode(filename):
    global oops
    for i in range(1, len(filename)):
        if not filename[1:i+1].isdigit():
            id = filename[:i]
            break
    #if not id:
    #    return
    try:
        print_bar(f'正在查找ID为{id}的歌曲信息...')
        url = urlopen(f'https://api.imjad.cn/cloudmusic/?type=detail&id={id}')
        raw_data = url.read()
        if not raw_data[0] == '{' and raw_data[-1] == '}':
            raise TypeError
        data = eval(raw_data)
        name = data['songs'][0]['name']
        artist = data['songs'][0]['ar'][0]['name']
        for i in range(len(name)):
            if name[i] in invalid:
                name = name[:i]
                break
        invalid_artist = False
        for i in invalid:
            if i in artist:
                invalid_artist = True
                break
        if invalid_artist:
            output_file = name_mp3(name)
        else:
            output_file = name_mp3(f'{artist} - {name}')
    except:
        output_file = name_mp3(id)
        print_bar(f'找不到ID为{id}的音乐信息，将使用其ID命名...')
    print_bar('正在转码...')
    try:
        with open(f'{input_dir}/{filename}', 'rb') as f:
            btay = bytearray(f.read())
        with open(f'{output_dir}/{output_file}', 'wb') as f:
            for i,j in enumerate(btay):
                btay[i] = j ^ 0xa3
            f.write(bytes(btay))
        #name_lock.release()
        print_bar(f'成功转码MP3文件：{output_file}')
    except:
        #exception_lock.acquire()
        #exceptionbox(f'ID为{id}的缓存转码失败！', '错误')
        #exception_lock.release()
        print_bar(f'ID为{id}的缓存转码失败！')
        return id
    #thread_print(list(threads))

# def run_thread(filename):
#     t = Thread(target=decode, args=[filename])
#     t.run()
#     return t

print('''网易云音乐缓存转换器
V0.1a3

免责声明：本程序仅以学习交流为用途，切勿用于商业目的。若因使用本程序造成任何版权纠纷，后果自负。
''')
sleep(3)
print('请选择网易云音乐缓存所在文件夹...')
sleep(1)
input_dir = diropenbox()
if not input_dir:
    msgbox('您已取消操作','操作取消','确认')
    sys.exit()
output_dir = 'cache2mp3'
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
target_files = []
for i in os.listdir(input_dir):
    if i[-4:] == '.uc!':
        target_files.append(i)
total = len(target_files)
print(f'找到{total}个目标文件。')

sleep(1)

# threads = []

# for i in target_files:
#     threads.append(Thread(target=decode, args=[i]))
#     #print(f'正在准备转码：{i}')
#     threads[-1].run()

#bar = ProgressBar().start()

# threads = map(run_thread, target_files)
# for i in threads:
#     if i.is_alive():
#         i.join()

for i in target_files:
    return_code = decode(i)
    if return_code:
        oops.append(return_code)
    finished += 1
    percentage = finished / total
    bar_value = round(percentage*bar_len)

    #bar.update(int(finished/total)*100)
#bar.finish()
print(' '*(bar_len+7))
if oops:
    print('以下ID的缓存转码失败：')
    for i in oops:
        print(i)
    msgbox(f'部分缓存文件转码失败，转码成功的文件已保存在{output_dir}文件夹内。',
           '转码完成','确认')
else:
    msgbox(f'所有缓存文件转码成功！MP3文件已保存在{output_dir}文件夹内。',
           '转码完成','确认')
