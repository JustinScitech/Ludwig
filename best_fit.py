# # below runs in 1:36

# import cv2
# import matplotlib.pyplot as plt
# import numpy as np

# def fit(img, templates, start_percent, stop_percent, threshold):
#     img_width, img_height = img.shape[::-1]
#     best_location_count = -1
#     best_locations = []
#     best_scale = 1

#     plt.axis([0, 2, 0, 1])
#     plt.show(block=False)

#     x = []
#     y = []
#     for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
#         locations = []
#         location_count = 0
#         for template in templates:
#             template = cv2.resize(template, None,
#                 fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC)
#             result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
#             result = np.where(result >= threshold)
#             location_count += len(result[0])
#             locations += [result]
#         print("scale: {0}, hits: {1}".format(scale, location_count))
#         x.append(location_count)
#         y.append(scale)
#         plt.plot(y, x)
#         plt.pause(0.00001)
#         if (location_count > best_location_count):
#             best_location_count = location_count
#             best_locations = locations
#             best_scale = scale
#             plt.axis([0, 2, 0, best_location_count])
#         elif (location_count < best_location_count):
#             pass
#     plt.close()

#     return best_locations, best_scale




# below runs in 0:37

import cv2
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def process_template(img, template, scale, threshold):
    template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return len(locations[0]), locations

def fit(img, templates, start_percent, stop_percent, threshold):
    img_width, img_height = img.shape[::-1]
    best_location_count = -1
    best_locations = []
    best_scale = 1

    x = []
    y = []
    scales = [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]
    
    for scale in scales:
        location_count = 0
        locations = []
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_template, img, template, scale, threshold) for template in templates]
            for future in futures:
                count, locs = future.result()
                location_count += count
                locations.append(locs)
        
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)
        y.append(scale)
        
        if location_count > best_location_count:
            best_location_count = location_count
            best_locations = locations
            best_scale = scale

    return best_locations, best_scale