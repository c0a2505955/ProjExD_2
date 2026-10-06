import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue／画面外ならFalse
    """

    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を5秒間表示する。
    screen: 画面surface
    None: 戻り値
    """
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(180)

    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_rct = cry_img.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))

    screen.blit(black, (0, 0))
    screen.blit(text, text_rct)
    screen.blit(cry_img, cry_rct)
    pg.display.update()
    time.sleep(5)
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #赤い爆弾

    bb_img.set_colorkey((0, 0, 0))  # 練習2: 黒四隅をなくす
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標乱数
    vx, vy = +5, +5  # 練習2: 爆弾初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # 練習4：kkとbbのrectが重なっていたら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこからしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2: 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2: 爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
