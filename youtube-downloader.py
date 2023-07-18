from pathlib import Path
import re, os
from glob import glob

from pytube import YouTube
import urllib.request
import moviepy.editor as mp

import tkinter
from tkinter import Label, Entry, Button, Checkbutton

## https://github.com/Zulko/moviepy/issues/591
#pyinstall audio_fadein 관련 오류
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
#pyinstall video / crop 관련 오류
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize


def downloader():
    audio_dir = './audio/'
    vidoe_dir = './video/'
    url = url_in.get()#input("url : ")
    yt = YouTube(url)

    video = yt.streams.get_highest_resolution()
    #video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last()
    video.download(vidoe_dir)

    translated = re.sub(r'[:?|/"]', '', yt.title)
    thum_dir = './thumbnail/' + translated + '.jpg'
    urllib.request.urlretrieve(yt.thumbnail_url, thum_dir)

    #print(yt.streams.filter(only_audio=True).all())
    if onlyMp4.get() == 0:
        audio = yt.streams.filter(file_extension='mp4').order_by('abr').all()[-1]
        audio.download(audio_dir)

        try:
            vfile = glob('./audio/*.mp4')
            
            for fi in vfile:
                file_name = Path(fi).stem
                clip = mp.VideoFileClip(fi)
                clip.audio.write_audiofile('./audio/' + file_name + '.mp3')
                
                #if fi == vfile[-1]:
                clip.close()
            
            for fi in vfile:
                os.remove(fi)


            done = Label(window, text="all done!")
            done.grid(row=7, column=1)
        except:
            audio_error = Label(window, text="audio download failed", height=10)
            audio_error.grid(row=7, column=1)

    if(yt.length%60 < 10):
        sec = '0' + str(yt.length%60)
    if(yt.length%60 >= 10):
        sec = str(yt.length%60)

    print('download done!')

    print('제목 : ', yt.title)
    print('영상 길이 : ', round(yt.length/60), ':', sec)
    print('게시자 : ', yt.author)
    print('게시일 : ', yt.publish_date)
    print('조회수 : ', yt.views)
    print('키워드 : ', yt.keywords)
    print('썸네일 주소 : ', yt.thumbnail_url)

    print('done!')
    
    vtitle = Label(window, text=yt.title, width=35)
    vlength = Label(window, text=str(round(yt.length/60)) + ':' + sec, width=20)
    vupload = Label(window, text=yt.author, width=20)
    vdate = Label(window, text=str(yt.publish_date), width=20)
    vtitle.grid(row=1, column=1)
    vlength.grid(row=2, column=1)
    vupload.grid(row=3, column=1)
    vdate.grid(row=4, column=1)



window = tkinter.Tk()

window.title('youtube-downloader 2.0.0')
window.geometry('400x400+400+200')
window.resizable(False, False)
window.iconbitmap('./icon.ico')

url_lbl = Label(window, text="url : ", width=10)
url_in = Entry(window, width=35)
btn = Button(window, text="여!", width=10, command=downloader)
onlyMp4 = tkinter.IntVar()
only_mp4 = Checkbutton(window, text='only MP4', variable=onlyMp4)
url_lbl.grid(row=0, column=0)
url_in.grid(row=0, column=1)
btn.grid(row=0, column=2)
only_mp4.grid(row=1, column=2)

lbl1 = Label(window, text='title : ', width=5)
lbl2 = Label(window, text='time : ', width=5)
lbl3 = Label(window, text='channel : ', width=5)
lbl4 = Label(window, text='date : ', width=5)
lbl1.grid(row=1, column=0)
lbl2.grid(row=2, column=0)
lbl3.grid(row=3, column=0)
lbl4.grid(row=4, column=0)

window.mainloop()