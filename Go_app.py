import sys
import pygame

# --- მასშტაბები და პარამეტრები ---
BOARD_SIZE = 19
GRID_SIZE = 35
MARGIN = 60

WIDTH = GRID_SIZE * (BOARD_SIZE - 1) + MARGIN * 2
BOARD_HEIGHT = WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + 60  # ქვედა პანელისთვის

# ფერები
BG_COLOR = (220, 179, 92)
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
LINE_COLOR = (40, 30, 10)
TEXT_COLOR = (50, 40, 20)
BUTTON_COLOR = (180, 40, 40)
BUTTON_HOVER = (220, 50, 50)
LAST_MOVE_COLOR = (0, 255, 200)  # მკვეთრი ნეონისფერი ბოლო სვლისთვის


class GoBoard:

    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
        ]
        # ტყვეების (მოკლული ქვების) მთვლელები
        self.captured_by_player = 0
        self.captured_by_ai = 0
        # ბოლო სვლის კოორდინატები
        self.last_move = None

    def draw(self, win, font):
        """ხატავს დაფას, კოორდინატებს და ქვებს"""
        pygame.draw.rect(win, BG_COLOR, (0, 0, WIDTH, BOARD_HEIGHT))

        # ბადის ხატვა
        for i in range(BOARD_SIZE):
            pygame.draw.line(
                win,
                LINE_COLOR,
                (MARGIN, MARGIN + i * GRID_SIZE),
                (WIDTH - MARGIN, MARGIN + i * GRID_SIZE),
                1,
            )
            pygame.draw.line(
                win,
                LINE_COLOR,
                (MARGIN + i * GRID_SIZE, MARGIN),
                (MARGIN + i * GRID_SIZE, BOARD_HEIGHT - MARGIN),
                1,
            )

            # კოორდინატები: ციფრები (1-19)
            num_text = str(19 - i)
            text_surface = font.render(num_text, True, TEXT_COLOR)
            win.blit(text_surface, (MARGIN - 30, MARGIN + i * GRID_SIZE - 10))
            win.blit(
                text_surface, (WIDTH - MARGIN + 15, MARGIN + i * GRID_SIZE - 10)
            )

            # კოორდინატები: ასოები (A-T, I-ს გარეშე)
            let_text = self.letters[i]
            letter_surface = font.render(let_text, True, TEXT_COLOR)
            win.blit(letter_surface, (MARGIN + i * GRID_SIZE - 7, MARGIN - 35))
            win.blit(
                letter_surface,
                (MARGIN + i * GRID_SIZE - 7, BOARD_HEIGHT - MARGIN + 15),
            )

        # ქვების ხატვა
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == 1:
                    pygame.draw.circle(
                        win,
                        BLACK,
                        (MARGIN + c * GRID_SIZE, MARGIN + r * GRID_SIZE),
                        GRID_SIZE // 2 - 2,
                    )
                elif self.grid[r][c] == 2:
                    pygame.draw.circle(
                        win,
                        WHITE,
                        (MARGIN + c * GRID_SIZE, MARGIN + r * GRID_SIZE),
                        GRID_SIZE // 2 - 2,
                    )

        # ბოლო სვლის მონიშვნა პატარა ნეონისფერი წერტილით
        # if self.last_move:
        #     r, c = self.last_move
        #     pygame.draw.circle(
        #         win,
        #         LAST_MOVE_COLOR,
        #         (MARGIN + c * GRID_SIZE, MARGIN + r * GRID_SIZE),
        #         4,
        #     )

    def get_liberties(self, r, c, visited=None):
        if visited is None:
            visited = set()
        color = self.grid[r][c]
        if color == 0:
            return 0
        visited.add((r, c))
        liberties = set()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if self.grid[nr][nc] == 0:
                    liberties.add((nr, nc))
                elif self.grid[nr][nc] == color and (nr, nc) not in visited:
                    liberties.update(self.get_liberties(nr, nc, visited))
        return liberties

    def check_captures(self, opponent_color):
        """ამოწმებს ალყას და ითვლის მოკლულ ქვებს"""
        captured_count = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == opponent_color:
                    visited = set()
                    liberties = self.get_liberties(r, c, visited)
                    if len(liberties) == 0:
                        for pr, pc in visited:
                            self.grid[pr][pc] = 0
                            captured_count += 1

        if opponent_color == 2:
            self.captured_by_player += captured_count
        else:
            self.captured_by_ai += captured_count

    def is_valid_move(self, r, c, color):
        if self.grid[r][c] != 0:
            return False
        self.grid[r][c] = color
        liberties = self.get_liberties(r, c)
        if len(liberties) > 0:
            self.grid[r][c] = 0
            return True
        opp_color = 2 if color == 1 else 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if self.grid[nr][nc] == opp_color:
                    opp_liberties = self.get_liberties(nr, nc)
                    if len(opp_liberties) == 0:
                        self.grid[r][c] = 0
                        return True
        self.grid[r][c] = 0
        return False


def main():
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont("Sylfaen", 16)
    panel_font = pygame.font.SysFont("Sylfaen", 14, bold=True)
    end_font = pygame.font.SysFont("Sylfaen", 32, bold=True)

    win = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Theory: პროფესიონალური გო AI")

    board = GoBoard()
    player_turn = True
    game_over = False
    winner_text = ""

    # ზედიზედ გაცხადებული პასების მთვლელი
    consecutive_passes = 0

    btn_w, btn_h = 120, 36
    btn_x = (WIDTH - btn_w) // 2
    btn_y = BOARD_HEIGHT + 12

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # კლავიატურაზე 'P' ღილაკზე დაჭერა ნიშნავს პასს (Pass)
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_p and player_turn:
                    print("შენ თქვი პასი (Pass) ✋")
                    consecutive_passes += 1
                    player_turn = False  # ჯერი გადადის AI-ზე

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # დანებების ღილაკი
                if (
                    btn_x <= mouse_pos[0] <= btn_x + btn_w
                    and btn_y <= mouse_pos[1] <= btn_y + btn_h
                ):
                    game_over = True
                    winner_text = "შენ დანებდი! AI-მ გაიმარჯვა 🏳️"

                # სვლა დაფაზე
                elif player_turn:
                    c = round((mouse_pos[0] - MARGIN) / GRID_SIZE)
                    r = round((mouse_pos[1] - MARGIN) / GRID_SIZE)

                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                        if board.is_valid_move(r, c, 1):
                            board.grid[r][c] = 1
                            board.last_move = (r, c)
                            board.check_captures(2)
                            consecutive_passes = (
                                0  # ნებისმიერი რეალური სვლა ანულებს პასებს
                            )
                            player_turn = False

        # --- თამაშის ავტომატური დასრულება ზედიზედ 2 პასის დროს ---
        if consecutive_passes >= 2 and not game_over:
            game_over = True
            flat_grid = [cell for row in board.grid for cell in row]
            # ჩინური/არეალური დათვლა: ქვები დაფაზე + მოკლული ტყვეები
            black_final = flat_grid.count(1) + board.captured_by_player
            white_final = flat_grid.count(2) + board.captured_by_ai

            if black_final > white_final:
                winner_text = f"მატჩი დასრულდა პასით! შენ მოიგე ({black_final} VS {white_final})"
            elif white_final > black_final:
                winner_text = f"მატჩი დასრულდა პასით! AI-მ მოიგო ({white_final} VS {black_final})"
            else:
                winner_text = "მატჩი დასრულდა ფრედ!"

        # 1. დაფის დახატვა
        board.draw(win, font)

        # 2. ქვედა პანელი
        pygame.draw.rect(win, (35, 35, 40), (0, BOARD_HEIGHT, WIDTH, 60))

        flat_grid = [cell for row in board.grid for cell in row]
        black_stones = flat_grid.count(1)
        white_stones = flat_grid.count(2)

        # სტატისტიკა და "P - პასი" ინსტრუქცია მწვანე პანელზე
        player_stat = panel_font.render(
            f"შავი (შენ): {black_stones}  [⚔️ ტყვე: {board.captured_by_player}]  |  [P - პასი]",
            True,
            (150, 255, 150),
        )
        ai_stat = panel_font.render(
            f"თეთრი (AI): {white_stones}  [⚔️ ტყვე: {board.captured_by_ai}]",
            True,
            (255, 150, 150),
        )

        win.blit(player_stat, (20, BOARD_HEIGHT + 20))
        win.blit(ai_stat, (WIDTH - ai_stat.get_width() - 20, BOARD_HEIGHT + 20))

        # დანებების ღილაკი
        if not game_over:
            if (
                btn_x <= mouse_pos[0] <= btn_x + btn_w
                and btn_y <= mouse_pos[1] <= btn_y + btn_h
            ):
                pygame.draw.rect(
                    win, BUTTON_HOVER, (btn_x, btn_y, btn_w, btn_h), border_radius=5
                )
            else:
                pygame.draw.rect(
                    win, BUTTON_COLOR, (btn_x, btn_y, btn_w, btn_h), border_radius=5
                )

            btn_text = font.render("დანებება", True, WHITE)
            text_rect = btn_text.get_rect(
                center=(btn_x + btn_w // 2, btn_y + btn_h // 2)
            )
            win.blit(btn_text, text_rect)

        # 3. დასასრულის ფარდა
        if game_over:
            overlay = pygame.Surface((WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            win.blit(overlay, (0, 0))

            text_surf = end_font.render(winner_text, True, WHITE)
            text_rect = text_surf.get_rect(
                center=(WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            win.blit(text_surf, text_rect)

        pygame.display.update()

        # --- AI-ს სვლის / ევრისტიკული პასის ლოგიკა ---
        if not player_turn and not game_over:
            pygame.time.delay(1200)

            best_score = -1000
            best_move = None

            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if board.is_valid_move(r, c, 2):
                        score = 0
                        center = BOARD_SIZE // 2
                        distance = abs(r - center) + abs(c - center)
                        score += (BOARD_SIZE * 2) - distance
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                                if board.grid[nr][nc] == 1:
                                    score += 15
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)

            # ჭკვიანი პასის ზღვარი: თუ დაფა ივსება და აზრიანი სვლა აღარ არსებობს, AI ამბობს პასს
            if best_move and best_score > 5:
                board.grid[best_move[0]][best_move[1]] = 2
                board.last_move = best_move
                board.check_captures(1)
                consecutive_passes = 0  # პასები ნულდება, რადგან რეალური სვლაა
                print("AI-მ გააკეთა სვლა.")
            else:
                consecutive_passes += 1
                print(
                    "AI მიხვდა, რომ სვლას აზრი არ აქვს და გამოაცხადა პასი! ✋"
                )

            player_turn = True
            board.draw(win, font)
            pygame.display.update()


if __name__ == "__main__":
    main()