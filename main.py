import re
import time

import dearpygui.dearpygui as dpg
import requests as requests
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'noplaylist': 'True', 'cache': 'remove'}

formats = {}
selected_format = {}
item_list = []
filename = ""
prev_url = ""
illegal_chars_regex = r"[#%&{}\<>*?/\-$!`\"\':@+|=]"


def set_format():
    global formats, selected_format
    index = item_list.index(dpg.get_value("fetched items"))
    print(index)
    selected_format = formats[index]
    print(selected_format)
    # selected_format = formats


def reformat_name(title):
    return re.sub(illegal_chars_regex, '', title)


def download_file(url):
    local_filename = reformat_name(filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
            f.close()
    return local_filename


def download():
    # TODO add filename popup maybe?
    print(selected_format)
    dpg.disable_item("download btn")
    dpg.configure_item("download btn", label="Downloading...")
    try:
        download_file(selected_format['url'])
        dpg.add_text(parent="main window", default_value="Success!", tag="success text")
    except:
        dpg.add_text(parent="main window", default_value="Error!", tag="success text")
    finally:
        time.sleep(2)
        dpg.delete_item("video title")
        dpg.delete_item("fetched items")
        dpg.delete_item("download btn")
        dpg.delete_item("success text")
        item_list.clear()


def fetch_options(sender, app_data):
    global item_list
    global filename
    global selected_format
    global formats
    global prev_url
    request_param = dpg.get_value("url field")
    if prev_url != request_param and dpg.does_alias_exist("fetched items") and dpg.does_alias_exist("download btn"):
        dpg.delete_item("fetched items")
        dpg.delete_item("download btn")
        prev_url = request_param
        item_list.clear()
    if not dpg.does_alias_exist("fetched items") and not dpg.does_alias_exist("download btn"):
        print(f"request param: {request_param}")
        with YoutubeDL(YDL_OPTIONS) as ydl:
            youtube_request = ydl.extract_info(request_param, download=False)
        # print(youtube_request)
        filename = youtube_request['title']
        label = f"Title: {filename}"
        filename += '.' + youtube_request['ext']
        formats = youtube_request['formats']
        selected_format = youtube_request['formats'][0]
        additions = ""
        for value in youtube_request['formats']:
            if value['url']:
                if value['filesize']:
                    fsize = int(value['filesize']) / 1024
                    if fsize > 1024:
                        fsize = str(round(fsize / 1024, 2)) + " mBytes"
                    else:
                        fsize = str(round(fsize, 2)) + " kBytes"
                    if value['asr'] and value['fps']:
                        additions = "(no audio)"
                    else:
                        additions = ""
                    if not value['fps']:
                        append_str = f"audio only ({value['ext']}): {fsize} {additions}"
                    else:
                        append_str = f"{value['format_note']} ({value['ext']}): {fsize} {additions}"
                    item_list.append(append_str)
                else:
                    item_list.append(f"{value['format_note']} ({value['ext']}): Unknown size {additions}")
        
        dpg.add_text(label, parent="main window", tag="video title")
        dpg.add_radio_button(parent="main window", tag="fetched items", items=item_list, label=label,
                             callback=set_format)
        dpg.add_button(parent="main window", label="Download!", tag="download btn", callback=download)
        prev_url = request_param


if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title='YoutubeDL GUI by No4nick', width=600, height=600)

    with dpg.window(width=600, height=600, no_title_bar=True, no_move=True, no_resize=True, tag="main window"):
        dpg.add_text("All downloads go to root where the executable is located")
        dpg.add_input_text(hint="YouTube URL", tag="url field")
        dpg.add_button(label="Fetch", tag="fetch btn")

    with dpg.item_handler_registry(tag="fetch btn handler") as handler:
        dpg.add_item_clicked_handler(callback=fetch_options)

    # bind item handler registry to item
    dpg.bind_item_handler_registry("fetch btn", "fetch btn handler")

    dpg.set_primary_window("main window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
