 @echo off
 echo "-----脚本执行开始!-----"
 echo "-----执行中,请耐心等待...-----"
 python bing.py >Log.txt
 echo "----脚本执行成功,请查看脚本所在文件夹中的Log.txt文件!----"
 set /p str=----请按回车键退出!---- &exit