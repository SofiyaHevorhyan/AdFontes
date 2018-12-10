import chartify
import pandas as pd
import numpy as np
from elements.process_file import process


def show(filename):
    system, endpoints, cashes, videos = process(filename)
    data = pd.DataFrame(columns=["endpoint_ID", "video_ID", "time_to_dc"])
    index = 0
    for ep in endpoints:
        for vid in ep.request:
            data.loc[index] = [ep.id, vid[0], vid[1]*ep.dc_latency]
            index += 1

    # Plot the data
    ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
    ch.set_title("Requests time to each video in each endpoint - " + filename)
    ch.set_subtitle("Color grouped by 'video ID'")
    ch.axes.set_xaxis_label("endpoints ID")
    ch.axes.set_yaxis_label("requests time from data centre")
    ch.plot.lollipop(
        data_frame=data,
        categorical_columns=['endpoint_ID', 'video_ID'],
        numeric_column='time_to_dc',
        color_column='video_ID',
        categorical_order_by='labels',
        categorical_order_ascending=True)
    ch.axes.set_xaxis_tick_orientation('vertical')
    ch.show()
    print("Char from file " + filename + " displayed")


for file in ["datasets/example.in", "datasets/me_at_the_zoo.in",
             "datasets/videos_worth_spreading.in",
             "datasets/kittens.in", "datasets/trending_today.in"]:
    show(file)
