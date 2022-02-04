import dearpygui.dearpygui as dpg
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'noplaylist': 'True'}


def change_text(sender, app_data):
    request_param = "https://www.youtube.com/watch?v=PyUcdClB5uc"
    with YoutubeDL(YDL_OPTIONS) as ydl:
        youtube_request = ydl.extract_info(request_param, download=False)
    print(youtube_request)
    format_str = ""
    format_str += f"Title: {youtube_request['title']}\n\n"
    count = 0
    for value in youtube_request['formats']:
        count += 1
        if value['filesize']:
            format_str += f"{count}. {value['format_note']} ({value['ext']}): {round(int(value['filesize']) / 1024, 2)} mBytes\n"
        else:
            format_str += f"{value['format_note']} ({value['ext']}): Unknown size\n"
    dpg.set_value("fetched text", f"{format_str}")


if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title='YoutubeDL GUI by No4nick', width=600, height=600, resizable=False)

    with dpg.window(width=600, height=600, no_title_bar=True, no_move=True, no_resize=True):
        dpg.add_text("YoutubeDL_XD!!")
        dpg.add_input_text(label="YouTube URL", hint="YouTube URL")
        dpg.add_button(label="Fetch", tag="fetch btn")
        dpg.add_text(tag="fetched text")

    with dpg.item_handler_registry(tag="widget handler") as handler:
        dpg.add_item_clicked_handler(callback=change_text)

    # bind item handler registry to item
    dpg.bind_item_handler_registry("fetch btn", "widget handler")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
