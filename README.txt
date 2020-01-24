网易云音乐缓存转换器
V0.1a2

免责声明：本程序仅以学习交流为用途，切勿用于商业目的。若因使用本程序造成任何版权纠纷，后果自负。

下载本程序时只需下载CloudmusicCacheHacker.py，Windows用户可额外下载launcher.py
env文件夹是本程序开发者使用的虚拟环境，在其他电脑上应该无法使用

运行指南：
1、在运行本程序之前，需要安装python 3.6+
然后用命令行执行
pip3 install easygui
2、运行本程序时，非Windows用户请用命令行在本程序目录下执行命令
python3 CloudmusicCacheHacker.py
对于Windows用户，也可直接双击launcher.bat来运行
注意launcher.bat要与CloudmusicCacheHacker.py在同一目录下
3、运行程序后，请在弹出的窗口中选择网易云音乐缓存文件夹的位置，程序将自动把缓存转换为MP3格式
本程序暂不支持移动端，手机用户可先将网易云缓存转移到电脑，再使用本程序进行转换
音乐缓存目录通常在netease/cloudmusic/Cache/Music1，缓存文件扩展名为.uc!
为了使程序能够正确获取歌曲信息，请在运行程序时保证网络畅通

已知问题：虽然采用了多线程的算法，但实际运行起来就像单线程一样

更新日志：

2020.1.7	V0.1a2
修复了一个有关网络安全性的漏洞
本次更新后，在获取歌曲信息时，将先检查所获取的数据是否合理，再通过eval函数进行处理