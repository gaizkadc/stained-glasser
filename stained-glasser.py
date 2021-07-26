import os
import datetime

import utils
import img_utils
import stained_glass_utils


from dotenv import load_dotenv
load_dotenv()

logger = utils.get_logger()
logger.info(os.getenv('APP_NAME') + ' started')

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

output_folder_path = utils.create_output_folder(logger, today)

vortices = stained_glass_utils.create_vortices(logger)
triangles = []

palette = img_utils.create_palette(logger)
# logger.info(f'palette: {palette}')

for i, vortex in enumerate(vortices):
    logger.info(f'iteration: {i}')
    triangles = stained_glass_utils.get_triangles(logger, vortex, triangles)

    img_utils.draw_triangles(logger, i, triangles, output_folder_path, palette)
