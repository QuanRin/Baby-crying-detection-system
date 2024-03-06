# config = {
#     "DATA_PATH": "./dataset/src/",
#     "CLASS_NUM": 2,
#     "BOX_NUM_PER_CELL": 2,
#     "STRIDE": 7,
# }

config = dict(
    image_size=(448, 448),
    image_data_csv="./image_data.csv",
    image_data_path="./dataset/src1/",
    audio_data_csv="./audio_data.csv",
    audio_data_path="./dataset/clean/",
    class_num=2,
    box_num=2,
    stride=7,
    audio_data_factor=0.7,
    data_threshold=0.5,
    # audio
    aud_class_num=3
)

yolo3_config = dict(
    image_size=(416, 416),
    image_data_csv="./image_data.csv",
    image_data_path="./dataset/src1/",
    class_num=2,
    stride=[13, 26, 52]
)
