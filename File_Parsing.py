# Parses the Map file seperate to save room in the Map class ##
import pygame


def map_data(cur_lvl, sub_lvl=None):
    # print(cur_lvl)
    # print(sub_lvl)
    Fp = open("MapAssets\\Level" + str(sub_lvl) + "-" + str(cur_lvl) + ".txt", "r")
    mCur_layer = []
    Header_data = {}
    Map_layers = []
    Tileset_img = None
    Num_tiles_wide = None
    for line in Fp:
        if line[-1] == "\n":
            line = line[0:-1]

        if len(line) >= 2 and line[0] == "[" and line[-1] == "]":
            section = line[1:-1]
            # print("in the '" + section + "' section")

            if section == "layer":
                if len(mCur_layer) > 0:
                    Map_layers.append(mCur_layer)
                    mCur_layer = []

        if (section == "header" or section == "tilesets") and "=" in line:
            elements = line.split("=")
            key = elements[0]
            if key in ("width", "height", "tilewidth", "tileheight"):
                value = int(elements[1])
            else:
                value = elements[1]
            if key == "tileset":
                tileset_parts = value.split(",")
                Tileset_img = pygame.image.load(tileset_parts[0])
                Tile_w = tileset_parts[1]
                tileset_tile_h = tileset_parts[2]
                gap_x = tileset_parts[3]
                gap_y = tileset_parts[4]
                Num_tiles_wide = Tileset_img.get_width() // Header_data["tilewidth"]
            Header_data[key] = value

        elif section == "layer" and line.count(",") >= Header_data["width"] - 1:
            row_data = line.split(",")
            if len(row_data) > Header_data["width"]:
                row_data = row_data[0:-1]
            for i in range(0, len(row_data)):
                row_data[i] = int(row_data[i])
            mCur_layer.append(row_data)

    Fp.close()

    if len(mCur_layer) > 0:
        Map_layers.append(mCur_layer)

    return Header_data, Map_layers, Tileset_img, Num_tiles_wide
