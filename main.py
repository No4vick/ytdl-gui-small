import dearpygui.dearpygui as dpg
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'noplaylist': 'True'}

formats = {}
selected_format = {}
item_list = []


def set_format():
    global formats, selected_format
    index = item_list.index(dpg.get_value("fetched items"))
    print(index)
    selected_format = formats[index]
    # selected_format = formats


def download():
    print(selected_format)
    ydl_opts = YDL_OPTIONS
    ydl_opts['format_id'] = selected_format['format_id']
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download({dpg.get_value("url field")})
    #TODO REWORK DOWNLOAD!!!
    #TODO add file selector


def fetch_options(sender, app_data):
    request_param = dpg.get_value("url field")
    print(f"request param: {request_param}")
    with YoutubeDL(YDL_OPTIONS) as ydl:
        youtube_request = ydl.extract_info(request_param, download=False)
    # print(youtube_request)
    global item_list
    label = f"Title: {youtube_request['title']}"
    global formats
    formats = youtube_request['formats']
    for value in youtube_request['formats']:
        if value['filesize']:
            item_list.append(
                f"{value['format_note']} ({value['ext']}): {round(int(value['filesize']) / 1024, 2)} mBytes")
        else:
            item_list.append(f"{value['format_note']} ({value['ext']}): Unknown size")
    dpg.add_radio_button(parent="main window", items=item_list, tag="fetched items", label=label, callback=set_format)
    dpg.add_button(parent="main window", label="Download!", tag="download btn", callback=download)
    #TODO Clear radios maybe?


if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title='YoutubeDL GUI by No4nick', width=600, height=600)

    with dpg.window(width=600, height=600, no_title_bar=True, no_move=True, no_resize=True, tag="main window"):
        dpg.add_text("YoutubeDL_XD!!")
        dpg.add_input_text(label="YouTube URL", hint="YouTube URL", tag="url field",
                           default_value="https://www.youtube.com/watch?v=PyUcdClB5uc")
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
