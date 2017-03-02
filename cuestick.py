import math
import pygame
import physics


def set_cue(game_state):
    hit_power = 0.8
    cue_length = 300
    cue_thickness = 3

    def draw_cue(cue_angle, displacement, color):
        # dy/dx = sin(a)/cos(s) = tan(a)
        cos_a = math.cos(math.radians(cue_angle))
        sin_a = math.sin(math.radians(cue_angle))
        x_constant = sin_a * cue_thickness
        y_constant = cos_a * cue_thickness

        points = [
            (ball.x + displacement * cos_a + x_constant,
             ball.y + displacement * sin_a - y_constant),
            (ball.x + displacement * cos_a - x_constant,
             ball.y + displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + displacement * cos_a - x_constant,
             ball.y + cue_length * sin_a + displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + displacement * cos_a + x_constant,
             ball.y + cue_length * sin_a + displacement * sin_a - y_constant)
        ]

        pygame.draw.polygon(game_state.canvas.surface, color, points)

        return points

    def delete_cue(angle, displacement,game_state):
        draw_cue(angle, displacement,
                 game_state.table_color)
        game_state.sides.draw(game_state.canvas.surface)
        game_state.holes.draw(game_state.canvas.surface)
        # game_state.canvas.redraw_balls(game_state)
        # game_state.balls.update()


    def draw_lines(ball, angle, color):
        #draws the aiming dotted lines
        line_dist = 5
        sin_a = math.sin(math.radians(angle))
        cos_a = math.cos(math.radians(angle))
        line_x = ball.x + ball.radius * cos_a * 2
        line_y = ball.y + ball.radius * sin_a * 2
        count = 1
        while (line_x > game_state.table_margin) and (line_x < game_state.canvas.size_x - game_state.table_margin) and \
                (line_y > game_state.table_margin) and (line_y < game_state.canvas.size_y - game_state.table_margin):
            pygame.draw.line(game_state.canvas.surface, color, (line_x, line_y),
                             (line_x + line_dist * cos_a, line_y + line_dist * sin_a))
            line_x += 2 * line_dist * cos_a
            line_y += 2 * line_dist * sin_a
            count += 1

    def get_cue_displacement(mouse_pos, ball, initial_distance):
        displacement = physics.point_distance(mouse_pos, (ball.x, ball.y)) - initial_distance + ball.radius
        if displacement > 0:
            if displacement > 100+ball.radius:
                cue_displacement = 100
            else:
                cue_displacement = displacement
        else:
            cue_displacement = ball.radius

        return cue_displacement

    ball = game_state.zero_ball
    angle = 0
    prev_angle = angle
    rect_pointlist = draw_cue(angle, ball.radius, (100, 100, 100))
    pygame.display.update()

    start_pos = pygame.mouse.get_pos()
    displacement = 0

    done = False
    while not done:
        start_pos = pygame.mouse.get_pos()
        pygame.event.get()
        if pygame.mouse.get_pressed()[0] and physics.is_point_in_rect(rect_pointlist, start_pos):
            done = True
            inital_mouse_dist = physics.point_distance(start_pos, (ball.x, ball.y))
            prev_displacement = ball.radius
            game_state.mark_one_frame()

            # cue was displaced from the cue ball
            while pygame.mouse.get_pressed()[0]:
                pygame.event.get()
                final_pos = pygame.mouse.get_pos()
                dx = ball.x - final_pos[0] - 0.1
                dy = ball.y - final_pos[1] - 0.1

                displacement = get_cue_displacement(final_pos,ball,inital_mouse_dist)

                if dx == 0:
                    # div by zero exception
                    angle = 90
                else:
                    angle = math.degrees(math.atan(dy / dx))
                if dx > 0:
                    angle -= 180
                if not (prev_angle == angle) or not (prev_displacement == displacement):
                    delete_cue( prev_angle, prev_displacement,game_state)
                    draw_lines(ball, prev_angle + 180, game_state.table_color)
                    rect_pointlist = draw_cue(angle, displacement, game_state.cue_color)
                    draw_lines(ball, angle + 180, (255, 255, 255))
                    pygame.display.update()
                    prev_angle = angle
                    prev_displacement = displacement

                game_state.mark_one_frame()

            if (displacement == ball.radius):
                done = False

    draw_lines(ball, prev_angle + 180, game_state.table_color)
    # hitting animation
    prev_n = displacement
    for n in range(int(displacement), ball.radius, -1):
        delete_cue(angle, prev_n,game_state)
        draw_cue(angle, n, game_state.cue_color)
        pygame.display.update()
        prev_n = n
    delete_cue(prev_angle, game_state.ball_size,game_state)

    sin_a = math.sin(math.radians(angle))
    cos_a = math.cos(math.radians(angle))
    ball.add_force(-(displacement * cos_a)*hit_power, -(displacement * sin_a)*hit_power)
