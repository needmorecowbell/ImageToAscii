import cv2
import _thread
import pygame
from time import sleep, time
from pygame.locals import *
import sys


x = 160
sx = 4


#chars = "9685403271 "
chars = "▓@╠■#§=+~/<\"':. "
#chars = "@§#&/|?:-. "
#chars = "@&#$%0§=+~°>^*\"-;:,. "
#chars = "@WMB&$#Q%mO8wZ0UbdahkCzpqXLun?oJYtcvxf1+{}[]~/\|()<>lI^*rji!\"'-;:`,._ "
#chars = ",˙̢;´ˈ˴̈̔̓ʹˇ˗̛͗˜˵̴̃͛¦ȷ˔˟˪̚!jŗɻʲ˭͆͞/\¬÷ƨɟʗˀˤ[~³īŕɀɺ˚˨ͦ͝cyçłƭɂɪʌ˅=sĪţƫǫțʀʔʚͰ7nÿņųƿȜɢɳFpÝĉĳŧơƸȳɑɝʜ̿hÇùėĹŝƆƬǯȽʡ3èûňżƽǵȱɖʊK¢äďĢŏŲƧǂǧȏɎɠͲDĄĠƃƘǎȅȡʬZÜğƀǡȤɯ6mÁĜŪƕǟȃʧNĀŅŹƱȔȻ#½Ö"[::-1]
#chars = "֍ŒǳȬЉœҦÑȒՖŇ͸Ϻ՗׋׵׿܇ܑܛܥܯܹ݃ݍއޑޛޥޯ޹߃ߍåǬЀӐ#ĞǠҜڴĘǍͶѮՔګ¥ŪǨΩщԒՊڲÙƀȭΨЛҞԕٹݺĈƌȗθҧՑڷ§ĝźǥɓΡϩћӋԦձڛݯûƑȱͷКҏԁվلݹôĹƙȽϔ҂ӳդݲòśǝəΎϡќәՀחٻݕuťȯͫϫӟףځے=ĸǫʄͰυяӡ٧ۊvłɔ˅ϲғجۅ~ĵɺ̊ӷؙٱۮ^Ɩʟͨӏمۘ*ɻ̐јه¿˟̾؅ڊʳ֮̃ͬڔˉ͑יٴ´"

pygame.init()
size = x*sx, int(x*sx*0.75)
display = pygame.display.set_mode(size)
content = pygame.Surface(size)
operating = False
ongoing = True
font = pygame.font.SysFont("Arial", sx)
#font.set_bold(True)
fpsa = 0
pygame.scrap.init()

br = (255, 255, 255)
fr = (0, 0, 0)

display.fill(br)

lenc = len(chars)

visload = False
mt = False
aa = False


def displayupdate(*args, **argv):
    global ongoing, operating, content, display, fpsa
    clock = pygame.time.Clock()
    while ongoing:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    copyAscii(gray)
                elif event.key == pygame.K_s:
                    saveAscii(gray)
        if not (visload or operating):
            display.blit(content, (0, 0))
        pygame.display.flip()
    pygame.quit()
        
def copyAscii(pic):
    m = 0
    for y in pic:
        tm = max(y)
        if tm > m:
            m = tm

    fx = 0
    fy = 0

    text = ""
    
    for y in pic:
        for x in y:
            text += chars[int(x/m*(lenc-1))]
        text += "\r"
    print(text)
    pygame.scrap.put (SCRAP_TEXT, bytes(text, "ascii"))
            


def toAscii(pic):
    global operating
    m = 0
    for y in pic:
        tm = max(y)
        if tm > m:
            m = tm

    fx = 0
    fy = 0
    if not visload: content.fill(br)
    
    for y in pic:
        for x in y:
            if visload:
                pygame.draw.rect(display, br, pygame.Rect((fx,fy),(20,20)))
                display.blit(font.render(chars[int(x/m*(lenc-1))], aa, fr), (fx, fy))
            else:
                content.blit(font.render(chars[int(x/m*(lenc-1))], aa, fr), (fx, fy))
            fx += sx
        fy += sx
        fx = 0
    operating = False
            
def saveAscii(pic):
    m = 0
    for y in pic:
        tm = max(y)
        if tm > m:
            m = tm

    fx = 0
    fy = 0

    text = ""
    
    for y in pic:
        for x in y:
            text += chars[int(x/m*(lenc-1))]
        text += "\r"
    with open("image.txt", "w") as file:
        file.write(text+"\n<asciimage.py by Henri Dohmen>")
        file.close()
    print("saved in image.txt")


cap = cv2.VideoCapture(0)
_thread.start_new_thread(displayupdate, (0, ))

while(True):  
    ret, frame = cap.read()

    #colored = cv2.resize(cv2.resize(cv2.cvtColor(frame, 0), (x, int(x*0.75))), (640, 480))
    colored = cv2.cvtColor(frame, 0)

    
    gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (x, int(x*0.75)))

    if not operating:
        operating = True
        if mt:
            _thread.start_new_thread(toAscii, (gray,))
        else:
            toAscii(gray)
        
    
    #gray = cv2.resize(gray, (640, 480), interpolation = cv2.INTER_NEAREST)

    
    cv2.imshow('frame',cv2.resize(gray, (640, 480)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        ongoing = False
        pygame.quit()
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        #_thread.start_new_thread(copyAscii, (gray, ))
        print("copy")
        copyAscii(gray)

cap.release()
cv2.destroyAllWindows()

