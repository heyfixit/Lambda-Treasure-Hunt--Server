from django.contrib.auth.models import User
from adventure.models import Player, Room, Item, Group
import random

Group.objects.all().delete()
g = Group(name="admin", cooldown=2)
g.save()
g = Group(name="default", cooldown=10)
g.save()

g = Group(name="cs18eu1", cooldown=100)
g.save()


Room.objects.all().delete()

# roomGraph={47: [(3, 11), {'e': 43}], 82: [(4, 6), {'e': 81}], 92: [(4, 7), {'n': 70}], 70: [(4, 8), {'n': 62, 's': 92}], 62: [(4, 9), {'s': 70, 'e': 55}], 90: [(4, 10), {'e': 30}], 43: [(4, 11), {'e': 36, 'w': 47}], 81: [(5, 6), {'e': 77, 'w': 82}], 71: [(5, 7), {'n': 49}], 49: [(5, 8), {'n': 55, 's': 71, 'e': 22}], 55: [(5, 9), {'s': 49, 'w': 62}], 30: [(5, 10), {'e': 17, 'w': 90}], 36: [(5, 11), {'n': 84, 'e': 27, 'w': 43}], 84: [(5, 12), {'s': 36}], 95: [(6, 5), {'n': 77}], 77: [(6, 6), {'s': 95, 'e': 28, 'w': 81}], 44: [(6, 7), {'e': 19}], 22: [(6, 8), {'e': 12, 'w': 49}], 24: [(6, 9), {'e': 8}], 17: [(6, 10), {'n': 27, 'e': 9, 'w': 30}], 27: [(6, 11), {'s': 17, 'w': 36}], 48: [(6, 12), {'e': 35}], 87: [(7, 3), {'e': 65}], 57: [(7, 4), {'e': 51}], 63: [(7, 5), {'n': 28}], 28: [(7, 6), {'n': 19, 's': 63, 'w': 77}], 19: [(7, 7), {'s': 28, 'e': 18, 'w': 44}], 12: [(7, 8), {'e': 6, 'w': 22}], 8: [(7, 9), {'n': 9, 'e': 2, 'w': 24}], 9: [(7, 10), {'n': 20, 's': 8, 'w': 17}], 20: [(7, 11), {'n': 35, 's': 9}], 35: [(7, 12), {'n': 53, 's': 20, 'w': 48}], 53: [(7, 13), {'s': 35}], 65: [(8, 3), {'n': 51, 'w': 87}], 51: [(8, 4), {'n': 42, 's': 65, 'w': 57}], 42: [(8, 5), {'n': 33, 's': 51}], 33: [(8, 6), {'n': 18, 's': 42}], 18: [(8, 7), {'n': 6, 's': 33, 'w': 19}], 6: [(8, 8), {'n': 2, 's': 18, 'w': 12}], 2: [(8, 9), {'n': 7, 's': 6, 'e': 0, 'w': 8}], 7: [(8, 10), {'n': 23, 's': 2}], 23: [(8, 11), {'s': 7}], 41: [(8, 12), {'n': 45, 'e': 31}], 45: [(8, 13), {'s': 41}], 94: [(9, 3), {'n': 73}], 73: [(9, 4), {'n': 32, 's': 94}], 32: [(9, 5), {'n': 13, 's': 73, 'e': 50}], 13: [(9, 6), {'n': 10, 's': 32, 'e': 34}], 10: [(9, 7), {'n': 5, 's': 13}], 5: [(9, 8), {'n': 0, 's': 10, 'e': 11}], 0: [(9, 9), {'n': 1, 's': 5, 'e': 4, 'w': 2}], 1: [(9, 10), {'n': 3, 's': 0, 'e': 14}], 3: [(9, 11), {'s': 1, 'e': 15}], 31: [(9, 12), {'n': 52, 'e': 25, 'w': 41}], 52: [(9, 13), {'n': 67, 's': 31, 'e': 74}], 67: [(9, 14), {'s': 52}], 54: [(10, 4), {'n': 50}], 50: [(10, 5), {'s': 54, 'w': 32}], 34: [(10, 6), {'e': 37, 'w': 13}], 46: [(10, 7), {'n': 11, 'e': 78}], 11: [(10, 8), {'s': 46, 'w': 5}], 4: [(10, 9), {'e': 29, 'w': 0}], 14: [(10, 10), {'e': 21, 'w': 1}], 15: [(10, 11), {'n': 25, 'e': 16, 'w': 3}], 25: [(10, 12), {'s': 15, 'e': 68, 'w': 31}], 74: [(10, 13), {'n': 88, 'w': 52}], 88: [(10, 14), {'s': 74}], 89: [(11, 3), {'n': 66}], 66: [(11, 4), {'n': 58, 's': 89, 'e': 86}], 58: [(11, 5), {'n': 37, 's': 66}], 37: [(11, 6), {'s': 58, 'e': 91, 'w': 34}], 78: [(11, 7), {'w': 46}], 39: [(11, 8), {'n': 29, 'e': 56}], 29: [(11, 9), {'s': 39, 'w': 4}], 21: [(11, 10), {'e': 26, 'w': 14}], 16: [(11, 11), {'e': 69, 'w': 15}], 68: [(11, 12), {'w': 25}], 97: [(12, 3), {'n': 86}], 86: [(12, 4), {'s': 97, 'e': 93, 'w': 66}], 98: [(12, 5), {'n': 91}], 91: [(12, 6), {'s': 98, 'w': 37}], 72: [(12, 7), {'n': 56}], 56: [(12, 8), {'s': 72, 'w': 39}], 40: [(12, 9), {'n': 26, 'e': 59}], 26: [(12, 10), {'s': 40, 'e': 38, 'w': 21}], 69: [(12, 11), {'w': 16}], 93: [(13, 4), {'e': 96, 'w': 86}], 64: [(13, 8), {'n': 59}], 59: [(13, 9), {'s': 64, 'w': 40}], 38: [(13, 10), {'n': 60, 'e': 61, 'w': 26}], 60: [(13, 11), {'n': 80, 's': 38, 'e': 75}], 80: [(13, 12), {'n': 83, 's': 60}], 83: [(13, 13), {'s': 80}], 96: [(14, 4), {'w': 93}], 61: [(14, 10), {'e': 99, 'w': 38}], 75: [(14, 11), {'n': 76, 'e': 79, 'w': 60}], 76: [(14, 12), {'s': 75}], 99: [(15, 10), {'w': 61}], 79: [(15, 11), {'n': 85, 'w': 75}], 85: [(15, 12), {'s': 79}]}


roomGraph = {493: [[50, 54], {'e': 490}], 497: [[50, 55], {'e': 437}], 495: [[50, 58], {'e': 383}], 469: [[50, 71], {'e': 425}], 478: [[51, 53], {'e': 351}], 490: [[51, 54], {'e': 444, 'w': 493}], 437: [[51, 55], {'e': 420, 'w': 497}], 419: [[51, 56], {'e': 276}], 355: [[51, 57], {'e': 235}], 383: [[51, 58], {'e': 330, 'w': 495}], 376: [[51, 59], {'e': 369}], 464: [[51, 60], {'n': 453}], 453: [[51, 61], {'s': 464, 'e': 451}], 394: [[51, 62], {'e': 381}], 448: [[51, 63], {'e': 364}], 499: [[51, 67], {'e': 456}], 450: [[51, 68], {'e': 445}], 474: [[51, 69], {'n': 418}], 418: [[51, 70], {'n': 425, 's': 474, 'e': 415}], 425: [[51, 71], {'s': 418, 'w': 469}], 491: [[52, 52], {'n': 351}], 351: [[52, 53], {'s': 491, 'e': 343, 'w': 478}], 444: [[52, 54], {'n': 420, 'w': 490}], 420: [[52, 55], {'s': 444, 'e': 213, 'w': 437}], 276: [[52, 56], {'e': 197, 'w': 419}], 235: [[52, 57], {'n': 330, 'e': 232, 'w': 355}], 330: [[52, 58], {'n': 369, 's': 235, 'w': 383}], 369: [[52, 59], {'n': 400, 's': 330, 'w': 376}], 400: [[52, 60], {'s': 369}], 451: [[52, 61], {'e': 402, 'w': 453}], 381: [[52, 62], {'n': 364, 'w': 394}], 364: [[52, 63], {'n': 429, 's': 381, 'e': 257, 'w': 448}], 429: [[52, 64], {'s': 364}], 488: [[52, 65], {'n': 412}], 412: [[52, 66], {'s': 488, 'e': 310}], 456: [[52, 67], {'e': 275, 'w': 499}], 445: [[52, 68], {'n': 447, 'e': 339, 'w': 450}], 447: [[52, 69], {'s': 445}], 415: [[52, 70], {'e': 406, 'w': 418}], 454: [[52, 71], {'n': 470, 'e': 423}], 470: [[52, 72], {'s': 454}], 428: [[53, 50], {'e': 391}], 308: [[53, 51], {'e': 274}], 273: [[53, 52], {'n': 343, 'e': 264}], 343: [[53, 53], {'s': 273, 'w': 351}], 238: [[53, 54], {'e': 233}], 213: [[53, 55], {'e': 179, 'w': 420}], 197: [[53, 56], {'n': 232, 'e': 196, 'w': 276}], 232: [[53, 57], {'n': 272, 's': 197, 'w': 235}], 272: [[53, 58], {'n': 295, 's': 232}], 295: [[53, 59], {'s': 272}], 366: [[53, 60], {'e': 335}], 402: [[53, 61], {'e': 176, 'w': 451}], 346: [[53, 62], {'e': 177}], 257: [[53, 63], {'n': 320, 'e': 146, 'w': 364}], 320: [[53, 64], {'n': 348, 's': 257}], 348: [[53, 65], {'s': 320}], 310: [[53, 66], {'e': 259, 'w': 412}], 275: [[53, 67], {'e': 242, 'w': 456}], 339: [[53, 68], {'e': 287, 'w': 445}], 405: [[53, 69], {'n': 406, 'e': 303}], 406: [[53, 70], {'s': 405, 'w': 415}], 423: [[53, 71], {'e': 408, 'w': 454}], 459: [[53, 72], {'e': 458}], 396: [[54, 49], {'n': 391}], 391: [[54, 50], {'s': 396, 'e': 334, 'w': 428}], 274: [[54, 51], {'n': 264, 'w': 308}], 264: [[54, 52], {'n': 236, 's': 274, 'w': 273}], 236: [[54, 53], {'s': 264, 'e': 229}], 233: [[54, 54], {'n': 179, 'w': 238}], 179: [[54, 55], {'s': 233, 'e': 175, 'w': 213}], 196: [[54, 56], {'n': 222, 'e': 159, 'w': 197}], 222: [[54, 57], {'n': 305, 's': 196}], 305: [[54, 58], {'n': 365, 's': 222}], 365: [[54, 59], {'s': 305}], 335: [[54, 60], {'e': 188, 'w': 366}], 176: [[54, 61], {'e': 114, 'w': 402}], 177: [[54, 62], {'n': 146, 'w': 346}], 146: [[54, 63], {'n': 215, 's': 177, 'e': 99, 'w': 257}], 215: [[54, 64], {'n': 246, 's': 146}], 246: [[54, 65], {'s': 215}], 259: [[54, 66], {'n': 242, 'w': 310}], 242: [[54, 67], {'n': 287, 's': 259, 'e': 218, 'w': 275}], 287: [[54, 68], {'s': 242, 'w': 339}], 303: [[54, 69], {'n': 361, 'e': 284, 'w': 405}], 361: [[54, 70], {'n': 408, 's': 303}], 408: [[54, 71], {'n': 458, 's': 361, 'w': 423}], 458: [[54, 72], {'s': 408, 'w': 459}], 482: [[55, 48], {'n': 393}], 393: [[55, 49], {'n': 334, 's': 482}], 334: [[55, 50], {'n': 294, 's': 393, 'e': 341, 'w': 391}]}
roomGraph2 = {294: [[55, 51], {'n': 250, 's': 334}], 250: [[55, 52], {'n': 229, 's': 294, 'e': 289}], 229: [[55, 53], {'n': 183, 's': 250, 'w': 236}], 183: [[55, 54], {'n': 175, 's': 229}], 175: [[55, 55], {'s': 183, 'e': 109, 'w': 179}], 159: [[55, 56], {'e': 142, 'w': 196}], 292: [[55, 57], {'n': 301, 'e': 148}], 301: [[55, 58], {'n': 304, 's': 292}], 304: [[55, 59], {'s': 301}], 188: [[55, 60], {'e': 139, 'w': 335}], 114: [[55, 61], {'n': 113, 'w': 176}], 113: [[55, 62], {'s': 114, 'e': 101}], 99: [[55, 63], {'n': 190, 'e': 91, 'w': 146}], 190: [[55, 64], {'s': 99}], 314: [[55, 65], {'e': 254}], 263: [[55, 66], {'n': 218}], 218: [[55, 67], {'s': 263, 'e': 216, 'w': 242}], 252: [[55, 68], {'n': 284, 'e': 234}], 284: [[55, 69], {'n': 302, 's': 252, 'w': 303}], 302: [[55, 70], {'n': 422, 's': 284}], 422: [[55, 71], {'n': 426, 's': 302}], 426: [[55, 72], {'n': 457, 's': 422}], 457: [[55, 73], {'n': 461, 's': 426}], 461: [[55, 74], {'s': 457}], 492: [[56, 48], {'e': 431}], 449: [[56, 49], {'n': 341}], 341: [[56, 50], {'s': 449, 'w': 334}], 389: [[56, 51], {'e': 300}], 289: [[56, 52], {'w': 250}], 170: [[56, 53], {'e': 129}], 185: [[56, 54], {'n': 109}], 109: [[56, 55], {'s': 185, 'e': 98, 'w': 175}], 142: [[56, 56], {'e': 102, 'w': 159}], 148: [[56, 57], {'e': 136, 'w': 292}], 171: [[56, 58], {'e': 61}], 162: [[56, 59], {'e': 67}], 139: [[56, 60], {'e': 65, 'w': 188}], 161: [[56, 61], {'e': 74}], 101: [[56, 62], {'n': 91, 'w': 113}], 91: [[56, 63], {'n': 180, 's': 101, 'e': 84, 'w': 99}], 180: [[56, 64], {'s': 91}], 254: [[56, 65], {'n': 245, 'w': 314}], 245: [[56, 66], {'s': 254, 'e': 237}], 216: [[56, 67], {'n': 234, 'e': 204, 'w': 218}], 234: [[56, 68], {'n': 368, 's': 216, 'w': 252}], 368: [[56, 69], {'s': 234}], 363: [[56, 70], {'n': 372, 'e': 328}], 372: [[56, 71], {'n': 441, 's': 363}], 441: [[56, 72], {'s': 372}], 431: [[57, 48], {'e': 387, 'w': 492}], 409: [[57, 49], {'e': 317}], 377: [[57, 50], {'n': 300}], 300: [[57, 51], {'n': 226, 's': 377, 'w': 389}], 226: [[57, 52], {'s': 300, 'e': 214}], 129: [[57, 53], {'n': 126, 'e': 194, 'w': 170}], 126: [[57, 54], {'n': 98, 's': 129}], 98: [[57, 55], {'n': 102, 's': 126, 'e': 70, 'w': 109}], 102: [[57, 56], {'s': 98, 'w': 142}], 136: [[57, 57], {'e': 49, 'w': 148}], 61: [[57, 58], {'e': 56, 'w': 171}], 67: [[57, 59], {'e': 16, 'w': 162}], 65: [[57, 60], {'n': 74, 'e': 58, 'w': 139}], 74: [[57, 61], {'n': 87, 's': 65, 'w': 161}], 87: [[57, 62], {'s': 74}], 84: [[57, 63], {'e': 62, 'w': 91}], 82: [[57, 64], {'n': 191, 'e': 64}], 191: [[57, 65], {'s': 82}], 237: [[57, 66], {'e': 125, 'w': 245}], 204: [[57, 67], {'n': 219, 'e': 165, 'w': 216}], 219: [[57, 68], {'s': 204}], 312: [[57, 69], {'n': 328, 'e': 268}], 328: [[57, 70], {'n': 332, 's': 312, 'e': 357, 'w': 363}], 332: [[57, 71], {'n': 350, 's': 328}], 350: [[57, 72], {'n': 436, 's': 332, 'e': 404}], 436: [[57, 73], {'s': 350}], 417: [[58, 47], {'n': 387}], 387: [[58, 48], {'n': 317, 's': 417, 'w': 431}], 317: [[58, 49], {'s': 387, 'e': 281, 'w': 409}], 278: [[58, 50], {'n': 225}], 225: [[58, 51], {'s': 278, 'e': 195}], 214: [[58, 52], {'n': 194, 'w': 226}], 194: [[58, 53], {'s': 214, 'w': 129}], 163: [[58, 54], {'n': 70}], 70: [[58, 55], {'s': 163, 'e': 60, 'w': 98}], 79: [[58, 56], {'n': 49}], 49: [[58, 57], {'s': 79, 'e': 29, 'w': 136}], 56: [[58, 58], {'e': 7, 'w': 61}], 16: [[58, 59], {'n': 58, 'e': 8, 'w': 67}], 58: [[58, 60], {'s': 16, 'w': 65}], 47: [[58, 61], {'n': 71, 'e': 43}], 71: [[58, 62], {'s': 47}]}
roomGraph3 = {62: [[58, 63], {'n': 64, 'e': 46, 'w': 84}], 64: [[58, 64], {'s': 62, 'w': 82}], 110: [[58, 65], {'e': 76}], 125: [[58, 66], {'n': 165, 'e': 83, 'w': 237}], 165: [[58, 67], {'n': 203, 's': 125, 'w': 204}], 203: [[58, 68], {'n': 268, 's': 165, 'e': 299}], 268: [[58, 69], {'s': 203, 'e': 411, 'w': 312}], 357: [[58, 70], {'w': 328}], 374: [[58, 71], {'e': 325}], 404: [[58, 72], {'n': 481, 'w': 350}], 481: [[58, 73], {'s': 404}], 489: [[59, 46], {'n': 487}], 487: [[59, 47], {'n': 318, 's': 489}], 318: [[59, 48], {'n': 281, 's': 487}], 281: [[59, 49], {'n': 228, 's': 318, 'e': 309, 'w': 317}], 228: [[59, 50], {'n': 195, 's': 281}], 195: [[59, 51], {'s': 228, 'e': 138, 'w': 225}], 173: [[59, 52], {'e': 133, 'w': 214}], 202: [[59, 53], {'e': 105}], 149: [[59, 54], {'e': 48}], 60: [[59, 55], {'n': 45, 'w': 70}], 45: [[59, 56], {'n': 29, 's': 60}], 29: [[59, 57], {'s': 45, 'e': 21, 'w': 49}], 7: [[59, 58], {'n': 8, 'e': 6, 'w': 56}], 8: [[59, 59], {'s': 7, 'w': 16}], 1: [[59, 60], {'e': 0}], 43: [[59, 61], {'e': 10, 'w': 47}], 77: [[59, 62], {'e': 19}], 46: [[59, 63], {'e': 20, 'w': 62}], 73: [[59, 64], {'e': 63}], 76: [[59, 65], {'n': 83, 'e': 72, 'w': 110}], 83: [[59, 66], {'s': 76, 'e': 130, 'w': 125}], 208: [[59, 67], {'e': 182}], 299: [[59, 68], {'e': 311, 'w': 203}], 411: [[59, 69], {'w': 268}], 280: [[59, 70], {'n': 325, 'e': 248}], 325: [[59, 71], {'n': 353, 's': 280, 'w': 374}], 353: [[59, 72], {'s': 325}], 378: [[60, 47], {'n': 333}], 333: [[60, 48], {'n': 309, 's': 378}], 309: [[60, 49], {'s': 333, 'e': 326, 'w': 281}], 211: [[60, 50], {'n': 138}], 138: [[60, 51], {'s': 211, 'e': 131, 'w': 195}], 133: [[60, 52], {'e': 117, 'w': 173}], 105: [[60, 53], {'n': 48, 'w': 202}], 48: [[60, 54], {'n': 36, 's': 105, 'w': 149}], 36: [[60, 55], {'s': 48, 'e': 22, 'w': 60}], 25: [[60, 56], {'e': 18}], 21: [[60, 57], {'e': 12, 'w': 29}], 6: [[60, 58], {'n': 2, 'w': 7}], 2: [[60, 59], {'n': 0, 's': 6, 'e': 3}], 0: [[60, 60], {'n': 10, 's': 2, 'e': 4, 'w': 1}], 10: [[60, 61], {'n': 19, 's': 0, 'w': 43}], 19: [[60, 62], {'n': 20, 's': 10, 'w': 77}], 20: [[60, 63], {'n': 63, 's': 19, 'e': 27, 'w': 46}], 63: [[60, 64], {'n': 72, 's': 20, 'w': 73}], 72: [[60, 65], {'s': 63, 'w': 76}], 130: [[60, 66], {'w': 83}], 182: [[60, 67], {'e': 157, 'w': 208}], 311: [[60, 68], {'w': 299}], 290: [[60, 69], {'e': 207}], 248: [[60, 70], {'n': 296, 'e': 231, 'w': 280}], 296: [[60, 71], {'s': 248}], 442: [[60, 72], {'n': 347}], 347: [[60, 73], {'n': 452, 's': 442, 'e': 291}], 452: [[60, 74], {'s': 347}], 432: [[61, 47], {'n': 342}], 342: [[61, 48], {'n': 326, 's': 432}], 326: [[61, 49], {'s': 342, 'w': 309}], 244: [[61, 50], {'e': 239}], 131: [[61, 51], {'n': 117, 'w': 138, 's': 244}], 117: [[61, 52], {'n': 108, 's': 131, 'w': 133, 'e': 166}], 108: [[61, 53], {'n': 78, 's': 117, 'e': 93}], 78: [[61, 54], {'n': 22, 's': 108}], 22: [[61, 55], {'n': 18, 's': 78, 'w': 36}], 18: [[61, 56], {'n': 12, 's': 22, 'w': 25}], 12: [[61, 57], {'n': 9, 's': 18, 'e': 14, 'w': 21}], 9: [[61, 58], {'n': 3, 's': 12, 'e': 11}], 3: [[61, 59], {'s': 9, 'e': 5, 'w': 2}], 4: [[61, 60], {'n': 23, 'e': 13, 'w': 0}], 23: [[61, 61], {'s': 4, 'e': 26}], 28: [[61, 62], {'n': 27}], 27: [[61, 63], {'n': 40, 's': 28, 'e': 30, 'w': 20}], 40: [[61, 64], {'s': 27}], 122: [[61, 65], {'n': 124, 'e': 88}], 124: [[61, 66], {'n': 157, 's': 122}], 157: [[61, 67], {'n': 210, 's': 124, 'w': 182}], 210: [[61, 68], {'s': 157}], 207: [[61, 69], {'n': 231, 'e': 151, 'w': 290}], 231: [[61, 70], {'s': 207, 'w': 248}], 271: [[61, 71], {'n': 337, 'e': 267}]}
roomGraph4 = {337: [[61, 72], {'s': 271}], 291: [[61, 73], {'n': 410, 'e': 286, 'w': 347}], 410: [[61, 74], {'s': 291}], 413: [[62, 48], {'n': 321}], 321: [[62, 49], {'s': 413, 'e': 307}], 239: [[62, 50], {'n': 198, 'w': 244}], 198: [[62, 51], {'n': 166, 's': 239, 'e': 199}], 166: [[62, 52], {'s': 198, 'e': 150}], 93: [[62, 53], {'n': 89}], 89: [[62, 54], {'n': 50, 's': 93}], 50: [[62, 55], {'n': 34, 's': 89}], 34: [[62, 56], {'n': 14, 's': 50, 'e': 35}], 14: [[62, 57], {'s': 34, 'e': 37, 'w': 12}], 11: [[62, 58], {'e': 17, 'w': 9}], 5: [[62, 59], {'w': 3}], 13: [[62, 60], {'e': 15, 'w': 4}], 26: [[62, 61], {'e': 55, 'w': 23}], 31: [[62, 62], {'n': 30, 'e': 33}], 30: [[62, 63], {'s': 31, 'e': 32, 'w': 27}], 41: [[62, 64], {'e': 39}], 88: [[62, 65], {'e': 53, 'w': 122}], 115: [[62, 66], {'n': 116, 'e': 95}], 116: [[62, 67], {'n': 132, 's': 115}], 132: [[62, 68], {'s': 116}], 151: [[62, 69], {'n': 172, 'e': 147, 'w': 207}], 172: [[62, 70], {'n': 267, 's': 151}], 267: [[62, 71], {'n': 285, 's': 172, 'w': 271}], 285: [[62, 72], {'n': 286, 's': 267}], 286: [[62, 73], {'n': 336, 's': 285, 'w': 291}], 336: [[62, 74], {'s': 286}], 480: [[63, 47], {'n': 373}], 373: [[63, 48], {'n': 307, 's': 480}], 307: [[63, 49], {'n': 230, 's': 373, 'e': 371, 'w': 321}], 230: [[63, 50], {'n': 199, 's': 307, 'e': 297}], 199: [[63, 51], {'s': 230, 'w': 198}], 150: [[63, 52], {'n': 135, 'w': 166}], 135: [[63, 53], {'s': 150, 'e': 106}], 68: [[63, 54], {'n': 52, 'e': 100}], 52: [[63, 55], {'n': 35, 's': 68, 'e': 75}], 35: [[63, 56], {'s': 52, 'w': 34}], 37: [[63, 57], {'w': 14}], 17: [[63, 58], {'n': 24, 'e': 42, 'w': 11}], 24: [[63, 59], {'s': 17}], 15: [[63, 60], {'w': 13}], 55: [[63, 61], {'w': 26}], 33: [[63, 62], {'e': 38, 'w': 31}], 32: [[63, 63], {'n': 39, 'e': 54, 'w': 30}], 39: [[63, 64], {'n': 53, 's': 32, 'e': 51, 'w': 41}], 53: [[63, 65], {'n': 95, 's': 39, 'w': 88}], 95: [[63, 66], {'n': 119, 's': 53, 'w': 115}], 119: [[63, 67], {'n': 134, 's': 95}], 134: [[63, 68], {'n': 147, 's': 119, 'e': 144}], 147: [[63, 69], {'n': 200, 's': 134, 'e': 153, 'w': 151}], 200: [[63, 70], {'n': 227, 's': 147, 'e': 206}], 227: [[63, 71], {'n': 269, 's': 200}], 269: [[63, 72], {'n': 319, 's': 227}], 319: [[63, 73], {'n': 359, 's': 269, 'e': 345}], 359: [[63, 74], {'s': 319}], 484: [[64, 47], {'n': 475}], 475: [[64, 48], {'n': 371, 's': 484}], 371: [[64, 49], {'s': 475, 'w': 307}], 297: [[64, 50], {'w': 230}], 367: [[64, 51], {'n': 111}], 111: [[64, 52], {'n': 106, 's': 367, 'e': 158}], 106: [[64, 53], {'n': 100, 's': 111, 'w': 135}], 100: [[64, 54], {'s': 106, 'e': 112, 'w': 68}], 75: [[64, 55], {'e': 85, 'w': 52}], 81: [[64, 56], {'n': 80}], 80: [[64, 57], {'n': 42, 's': 81, 'e': 86}], 42: [[64, 58], {'n': 44, 's': 80, 'e': 118, 'w': 17}], 44: [[64, 59], {'s': 42}], 104: [[64, 60], {'n': 59, 'e': 107}], 59: [[64, 61], {'n': 38, 's': 104, 'e': 92}], 38: [[64, 62], {'s': 59, 'e': 66, 'w': 33}], 54: [[64, 63], {'w': 32}], 51: [[64, 64], {'n': 69, 'e': 57, 'w': 39}], 69: [[64, 65], {'n': 94, 's': 51, 'e': 103}], 94: [[64, 66], {'n': 152, 's': 69}], 152: [[64, 67], {'s': 94}], 144: [[64, 68], {'e': 155, 'w': 134}], 153: [[64, 69], {'e': 329, 'w': 147}], 206: [[64, 70], {'n': 288, 'e': 380, 'w': 200}], 288: [[64, 71], {'s': 206}], 375: [[64, 72], {'n': 345, 'e': 385}], 345: [[64, 73], {'s': 375, 'w': 319}], 434: [[65, 48], {'n': 370}], 370: [[65, 49], {'n': 262, 's': 434, 'e': 407}], 262: [[65, 50], {'n': 167, 's': 370, 'e': 358}], 167: [[65, 51], {'n': 158, 's': 262, 'e': 260}]}
roomGraph5 = {158: [[65, 52], {'s': 167, 'w': 111}], 141: [[65, 53], {'n': 112, 'e': 156}], 112: [[65, 54], {'s': 141, 'e': 140, 'w': 100}], 85: [[65, 55], {'e': 154, 'w': 75}], 96: [[65, 56], {'n': 86, 'e': 97}], 86: [[65, 57], {'s': 96, 'e': 90, 'w': 80}], 118: [[65, 58], {'e': 137, 'w': 42}], 120: [[65, 59], {'n': 107, 'e': 127}], 107: [[65, 60], {'s': 120, 'e': 121, 'w': 104}], 92: [[65, 61], {'w': 59}], 66: [[65, 62], {'n': 169, 'e': 123, 'w': 38}], 169: [[65, 63], {'s': 66, 'e': 186}], 57: [[65, 64], {'e': 145, 'w': 51}], 103: [[65, 65], {'n': 160, 'w': 69}], 160: [[65, 66], {'s': 103}], 187: [[65, 67], {'n': 155}], 155: [[65, 68], {'s': 187, 'e': 316, 'w': 144}], 329: [[65, 69], {'w': 153}], 380: [[65, 70], {'n': 424, 'w': 206}], 424: [[65, 71], {'s': 380, 'e': 473}], 385: [[65, 72], {'w': 375}], 496: [[66, 48], {'n': 407}], 407: [[66, 49], {'s': 496, 'w': 370}], 358: [[66, 50], {'e': 401, 'w': 262}], 260: [[66, 51], {'w': 167}], 168: [[66, 52], {'n': 156, 'e': 340}], 156: [[66, 53], {'s': 168, 'e': 164, 'w': 141}], 140: [[66, 54], {'w': 112}], 154: [[66, 55], {'e': 193, 'w': 85}], 97: [[66, 56], {'e': 181, 'w': 96}], 90: [[66, 57], {'e': 178, 'w': 86}], 137: [[66, 58], {'w': 118}], 127: [[66, 59], {'e': 184, 'w': 120}], 121: [[66, 60], {'n': 128, 'e': 143, 'w': 107}], 128: [[66, 61], {'s': 121, 'e': 189}], 123: [[66, 62], {'w': 66}], 186: [[66, 63], {'e': 205, 'w': 169}], 145: [[66, 64], {'n': 174, 'e': 220, 'w': 57}], 174: [[66, 65], {'n': 192, 's': 145, 'e': 224}], 192: [[66, 66], {'n': 201, 's': 174, 'e': 223}], 201: [[66, 67], {'s': 192}], 316: [[66, 68], {'n': 344, 'w': 155}], 344: [[66, 69], {'n': 392, 's': 316, 'e': 390}], 392: [[66, 70], {'s': 344, 'e': 462}], 473: [[66, 71], {'e': 494, 'w': 424}], 468: [[67, 48], {'n': 463}], 463: [[67, 49], {'s': 468, 'e': 362}], 401: [[67, 50], {'w': 358}], 356: [[67, 51], {'e': 349}], 340: [[67, 52], {'w': 168}], 164: [[67, 53], {'n': 217, 'e': 298, 'w': 156}], 217: [[67, 54], {'s': 164, 'e': 247}], 193: [[67, 55], {'e': 251, 'w': 154}], 181: [[67, 56], {'w': 97}], 178: [[67, 57], {'n': 209, 'e': 243, 'w': 90}], 209: [[67, 58], {'s': 178}], 184: [[67, 59], {'e': 221, 'w': 127}], 143: [[67, 60], {'e': 212, 'w': 121}], 189: [[67, 61], {'e': 255, 'w': 128}], 241: [[67, 62], {'n': 205, 'e': 266}], 205: [[67, 63], {'s': 241, 'e': 479, 'w': 186}], 220: [[67, 64], {'w': 145}], 224: [[67, 65], {'w': 174}], 223: [[67, 66], {'n': 283, 'w': 192}], 283: [[67, 67], {'n': 331, 's': 223, 'e': 313}], 331: [[67, 68], {'s': 283, 'e': 446}], 390: [[67, 69], {'w': 344}], 462: [[67, 70], {'w': 392}], 494: [[67, 71], {'w': 473}], 467: [[68, 47], {'n': 399}], 399: [[68, 48], {'n': 362, 's': 467}], 362: [[68, 49], {'n': 352, 's': 399, 'w': 463}], 352: [[68, 50], {'n': 349, 's': 362, 'e': 485}], 349: [[68, 51], {'n': 324, 's': 352, 'e': 384, 'w': 356}], 324: [[68, 52], {'n': 298, 's': 349, 'e': 354}], 298: [[68, 53], {'s': 324, 'w': 164}], 247: [[68, 54], {'e': 261, 'w': 217}], 251: [[68, 55], {'e': 315, 'w': 193}], 293: [[68, 56], {'n': 243}], 243: [[68, 57], {'s': 293, 'e': 256, 'w': 178}], 253: [[68, 58], {'n': 221, 'e': 258}], 221: [[68, 59], {'s': 253, 'e': 240, 'w': 184}], 212: [[68, 60], {'w': 143}], 255: [[68, 61], {'w': 189}], 266: [[68, 62], {'w': 241}], 479: [[68, 63], {'w': 205}], 313: [[68, 67], {'w': 283}], 446: [[68, 68], {'e': 466, 'w': 331}], 485: [[69, 50], {'w': 352}], 384: [[69, 51], {'w': 349}], 354: [[69, 52], {'w': 324}], 277: [[69, 53], {'n': 261, 'e': 323}], 261: [[69, 54], {'s': 277, 'e': 322, 'w': 247}]}
roomGraph6 = {315: [[69, 55], {'w': 251}], 360: [[69, 56], {'n': 256, 'e': 398}], 256: [[69, 57], {'s': 360, 'e': 327, 'w': 243}], 258: [[69, 58], {'e': 306, 'w': 253}], 240: [[69, 59], {'n': 249, 'e': 386, 'w': 221}], 249: [[69, 60], {'n': 265, 's': 240, 'e': 282}], 265: [[69, 61], {'n': 279, 's': 249, 'e': 270}], 279: [[69, 62], {'s': 265}], 486: [[69, 67], {'n': 466}], 466: [[69, 68], {'s': 486, 'e': 472, 'w': 446}], 323: [[70, 53], {'e': 433, 'w': 277}], 322: [[70, 54], {'n': 382, 'e': 435, 'w': 261}], 382: [[70, 55], {'s': 322, 'e': 388}], 398: [[70, 56], {'e': 438, 'w': 360}], 327: [[70, 57], {'e': 427, 'w': 256}], 306: [[70, 58], {'e': 397, 'w': 258}], 386: [[70, 59], {'e': 414, 'w': 240}], 282: [[70, 60], {'w': 249}], 270: [[70, 61], {'n': 416, 'e': 338, 'w': 265}], 416: [[70, 62], {'s': 270}], 472: [[70, 68], {'w': 466}], 455: [[71, 52], {'n': 433}], 433: [[71, 53], {'s': 455, 'e': 460, 'w': 323}], 435: [[71, 54], {'w': 322}], 388: [[71, 55], {'e': 477, 'w': 382}], 438: [[71, 56], {'e': 465, 'w': 398}], 427: [[71, 57], {'e': 430, 'w': 327}], 397: [[71, 58], {'w': 306}], 414: [[71, 59], {'w': 386}], 379: [[71, 60], {'n': 338, 'e': 395}], 338: [[71, 61], {'s': 379, 'w': 270}], 460: [[72, 53], {'w': 433}], 477: [[72, 55], {'e': 483, 'w': 388}], 465: [[72, 56], {'e': 498, 'w': 438}], 430: [[72, 57], {'n': 443, 'e': 439, 'w': 427}], 443: [[72, 58], {'s': 430, 'e': 471}], 403: [[72, 59], {'n': 395}], 395: [[72, 60], {'s': 403, 'e': 421, 'w': 379}], 476: [[72, 61], {'e': 440}], 483: [[73, 55], {'w': 477}], 498: [[73, 56], {'w': 465}], 439: [[73, 57], {'w': 430}], 471: [[73, 58], {'w': 443}], 421: [[73, 60], {'n': 440, 'w': 395}], 440: [[73, 61], {'s': 421, 'w': 476}]}

for key in roomGraph2:
    roomGraph[key] = roomGraph2[key]

for key in roomGraph3:
    roomGraph[key] = roomGraph3[key]

for key in roomGraph4:
    roomGraph[key] = roomGraph4[key]

for key in roomGraph5:
    roomGraph[key] = roomGraph5[key]

for key in roomGraph6:
    roomGraph[key] = roomGraph6[key]


numRooms = len(roomGraph)
rooms = [None] * numRooms
for i in range(0, numRooms):
    x = roomGraph[i][0][0]
    rooms[i] = Room(title=f"Room {i}", description=f"You are standing in an empty room.", coordinates=f"({roomGraph[i][0][0]},{roomGraph[i][0][1]})",id=i)
    rooms[i].save()


for roomID in roomGraph:
    room = rooms[roomID]
    if 'n' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['n']], 'n')
    if 's' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['s']], 's')
    if 'e' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['e']], 'e')
    if 'w' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['w']], 'w')

players=Player.objects.all()
for p in players:
  p.currentRoom=rooms[0].id
  p.save()



Item.objects.all().delete()

for i in range(0, 500):
  if random.random() > 0.7:
    t = Item(name="tiny treasure",
             description="This is a tiny piece of treasure",
             weight=1,
             aliases="tiny treasure,treasure",
             value=100,
             itemtype="TREASURE",
             attributes='{}',
             room=Room.objects.get(id=i))
    t.save()


t = Item(name="boots",
         description="These are boots",
         weight=2,
         aliases="boots",
         value=100,
         itemtype="FOOTWEAR",
         attributes='{"SPEED":1}',
         room=Room.objects.get(id=0))
t.save()

t = Item(name="jacket",
         description="This is a jacket",
         weight=2,
         aliases="jacket",
         value=100,
         itemtype="BODYWEAR",
         attributes='{"STRENGTH":1}',
         room=Room.objects.get(id=0))
t.save()


# from django.contrib.auth.models import User
# from adventure.models import Player, Room, Item
# import random

# t=Item.objects.first()
# t.levelUpAndRespawn()



rooms=Room.objects.all()

for room in rooms:
    room.title = "A misty room"
    room.description = "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction."
    room.save()

start=Room.objects.get(id=0)
shop=Room.objects.get(id=1)
name_changer = Room.objects.get(id=467)

start.title = "A brightly lit room"
start.description = "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east."
start.save()

shop.title = "Shop"
shop.description = "You are standing in a small shop. A sign behind the mechanical shopkeeper says 'WILL PAY FOR TREASURE'."
shop.save()

name_changer.title = "Name Changer"
name_changer.description = "You see a man who will change your name."
name_changer.save()




r=Room.objects.get(id=22)
r.title = "The Peak of Mt. Holloway"
r.description = "You are standing at the zenith of Mt. Holloway. You see before you a holy shrine erected in the image of a magnificent winged deity."
r.elevation = 5
r.terrain = "MOUNTAIN"
r.save()

r = Room.objects.get(id=18)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 4
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=78)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 4
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=36)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 4
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=12)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 3
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=25)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 3
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=108)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 3
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=48)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 3
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=60)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 3
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=9)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=14)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=21)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=117)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=93)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=105)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=149)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=45)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=70)
r.title = 'Mt. Holloway'
r.description = 'You are on the side of a steep incline.'
r.elevation = 2
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=3)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=11)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=34)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=37)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=29)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=131)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=133)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=166)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=89)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=202)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=163)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()

r = Room.objects.get(id=98)
r.title = 'Mt. Holloway'
r.description = 'You are at the base of a large, looming mountain.'
r.elevation = 1
r.terrain = 'MOUNTAIN'
r.save()



r=Room.objects.get(id=216)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=234)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=218)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=368)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=252)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=263)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=242)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=284)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=287)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=259)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=275)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=302)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=303)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=339)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=310)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=456)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=422)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=361)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=405)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=445)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=412)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=499)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=426)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=408)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=406)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=447)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=450)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=488)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=457)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=458)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=423)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=415)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'TRAP'
r.save()


r=Room.objects.get(id=461)
r.title = 'An Ancient Shrine'
r.description = 'You are standing before a dark shrine to a fast looking fellow.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=459)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=454)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=418)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=470)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=425)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=474)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()


r=Room.objects.get(id=469)
r.title = 'A Dark Cave'
r.description = 'You are standing in a dark cave.'
r.elevation = 0
r.terrain = 'CAVE'
r.save()




