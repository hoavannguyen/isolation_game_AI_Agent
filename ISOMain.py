import pygame as p
import ISO2Player,ISOAI_Hard,ISOAI_Medium,ISOAI_Easy
WIDTH =920
HEIGHT = 668
MAX_FPS=60
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("ISOLATION GAME")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    home_page = p.transform.scale(p.image.load('Images/home_page.png'), (920,668))
    screen.blit(home_page, p.Rect(0,0, 920, 668))
    running = True
    while running:
        mouse_x, mouse_y = p.mouse.get_pos()  # Lấy tọa độ của chuột

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if 352<mouse_x<579 and 109<mouse_y<189:
                    options = p.transform.scale(p.image.load('Images/game_option.png'), (920, 668))
                    screen.blit(options, p.Rect(0, 0, 920, 668))
                    while running:
                        mouse_x, mouse_y = p.mouse.get_pos()
                        for e in p.event.get():
                            if e.type == p.QUIT:
                                import sys
                                sys.exit('Bye')
                            if e.type == p.MOUSEBUTTONDOWN:
                                if 306 < mouse_x < 612 and 320 < mouse_y <381:
                                    ISOAI_Easy.main()
                                if 306 < mouse_x < 612 and 389 < mouse_y < 449:
                                    ISOAI_Medium.main()
                                if 306 < mouse_x < 612 and 459 < mouse_y < 519:
                                    ISOAI_Hard.main()
                                if 570 < mouse_x < 661 and 87 < mouse_y < 176:
                                    main()
                        clock.tick(MAX_FPS)
                        p.display.flip()
                if 352<mouse_x<579 and 214<mouse_y<291:
                    ISO2Player.main()
                if 735<mouse_x<864 and 605<mouse_y<647:
                    print('About')
        clock.tick(MAX_FPS)
        p.display.flip()
if __name__== "__main__":
    main()