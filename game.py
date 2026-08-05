import pygame
import math
import random
import os
import array

# ==========================================
# 1. CONSTANTS & SYSTEM SETTINGS
# ==========================================
WIDTH, HEIGHT = 900, 750
FPS = 60

# Slick Neon Palette
BG_COLOR = (8, 8, 16)
CYAN = (0, 240, 255)
MAGENTA = (255, 0, 180)
RED = (255, 40, 40)
YELLOW = (255, 200, 0)
GREEN = (40, 255, 100)
ORANGE = (255, 100, 0)
WHITE = (245, 245, 250)
DARK_GRAY = (40, 40, 50)
LIGHT_GRAY = (180, 180, 200)

# ==========================================
# 2. AUDIO SYNTHESIS & SOUND MANAGER
# ==========================================
class SoundManager:
    """Generates 8-bit retro synthesizer sound effects on-the-fly using mono buffers."""
    def __init__(self):
        self.enabled = False
        try:
            # Force mixer settings
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except Exception:
            print("[Warning] Audio hardware not detected. Running game in silent mode.")

        self.sounds = {}
        if self.enabled:
            try:
                self.sounds['laser'] = self._synth_laser()
                self.sounds['enemy_laser'] = self._synth_enemy_laser()
                self.sounds['explosion'] = self._synth_explosion()
                self.sounds['explosion_boss'] = self._synth_explosion_boss()
                self.sounds['hit'] = self._synth_hit()
                self.sounds['powerup'] = self._synth_powerup()
                self.sounds['boss_alarm'] = self._synth_boss_alarm()
                self.sounds['bg_music'] = self._synth_bg_music()
                self.sounds['bg_music'].set_volume(0.22)
                self.sounds['bg_music'].play(loops=-1)
            except Exception as e:
                print(f"[Warning] Failed to synthesize sounds ({e}). Running in silent mode.")
                self.enabled = False

    def _synth_laser(self):
        sr = 22050
        duration = 0.12
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Pitch sweeping down quickly from 1200Hz to 400Hz
            freq = 1200 - 800 * (t / duration)
            val = int(14000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_enemy_laser(self):
        sr = 22050
        duration = 0.15
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Pitch sweep down from 500Hz to 150Hz (sounds deeper/threatening)
            freq = 500 - 350 * (t / duration)
            val = int(10000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_explosion(self):
        sr = 22050
        duration = 0.3
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # White noise combined with low rumbling frequency
            noise = random.uniform(-1.0, 1.0)
            rumble = math.sin(2 * math.pi * 50 * t)
            val = int(18000 * (noise * 0.75 + rumble * 0.25) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_explosion_boss(self):
        sr = 22050
        duration = 0.8
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Deep, crackling boss explosion
            noise = random.uniform(-1.0, 1.0)
            rumble = math.sin(2 * math.pi * (35 + 20 * math.sin(2 * math.pi * 10 * t)) * t)
            val = int(22000 * (noise * 0.5 + rumble * 0.5) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_hit(self):
        sr = 22050
        duration = 0.07
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Short, sharp dissonant square-like wave buzz
            freq = 120
            wave = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
            val = int(20000 * wave * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_powerup(self):
        sr = 22050
        duration = 0.25
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Upward frequency sweep (cyber arpeggio feel)
            freq = 400 + 800 * (t / duration)
            # Add vibrato
            freq += 50 * math.sin(2 * math.pi * 32 * t)
            val = int(12000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_boss_alarm(self):
        sr = 22050
        duration = 0.6
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        for i in range(n):
            t = i / sr
            # Alternating klaxon siren (440Hz -> 330Hz)
            freq = 440 if int(t * 10) % 2 == 0 else 330
            val = int(16000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration))
            buf[i] = val
        return pygame.mixer.Sound(buffer=buf)

    def _synth_bg_music(self):
        mixer_settings = pygame.mixer.get_init()
        sr = mixer_settings[0] if mixer_settings else 22050
        duration = 16.0
        n = int(sr * duration)
        buf = array.array('h', [0] * n)
        
        notes = [130.81, 155.56, 196.00, 233.08, 261.63, 311.13, 392.00, 466.16,
                 466.16, 392.00, 311.13, 261.63, 233.08, 196.00, 155.56, 130.81]
        
        step_duration = 0.25
        
        for i in range(n):
            t = i / sr
            step = int(t / step_duration)
            note_idx = step % len(notes)
            freq = notes[note_idx]
            
            bar = int(t / 4.0) % 4
            if bar == 0:
                pass
            elif bar == 1:
                freq = freq * (207.65 / 196.00)
            elif bar == 2:
                freq = freq * (174.61 / 196.00)
            elif bar == 3:
                freq = freq * (196.00 / 196.00)
                
            t_step = t - (step * step_duration)
            vibrato = 1.0 + 0.015 * math.sin(2 * math.pi * 6 * t)
            phase = 2 * math.pi * freq * vibrato * t_step
            env = math.exp(-6.0 * t_step)
            
            wave = math.sin(phase)
            wave += 0.5 * math.sin(phase * 0.5)
            wave += 0.25 * math.sin(phase * 1.5)
            
            val = int(4500 * wave * env)
            
            bass_freqs = [65.41, 51.91, 43.65, 49.00]
            bass_freq = bass_freqs[bar]
            bass_wave = math.sin(2 * math.pi * bass_freq * t)
            bass_pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t)
            val += int(1500 * bass_wave * bass_pulse)
            
            buf[i] = max(-32768, min(32767, val))
            
        return pygame.mixer.Sound(buffer=buf)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

# Initialize Sound Manager globally
sound_system = SoundManager()

# ==========================================
# 3. VECTOR DRAWING UTILITIES (WITH GLOW)
# ==========================================
def draw_glow_polygon(surface, points, color, glow_color=None, glow_radius=10, thickness=2):
    """Draws a vector polygon with layers of transparent outlines to build a neon glow effect."""
    if glow_color is None:
        glow_color = color

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs) - glow_radius - 5, max(xs) + glow_radius + 5
    min_y, max_y = min(ys) - glow_radius - 5, max(ys) + glow_radius + 5
    w = int(max_x - min_x)
    h = int(max_y - min_y)

    if w <= 0 or h <= 0:
        return

    # Draw glow to standard alpha-compatible surfaces
    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    local_pts = [(p[0] - min_x, p[1] - min_y) for p in points]

    # Layer outlines for glow
    for g in range(glow_radius, 1, -2):
        alpha = int(90 * (1.0 - (g - 1) / glow_radius))
        c = (*glow_color[:3], alpha)
        pygame.draw.polygon(temp_surf, c, local_pts, int(thickness + g))

    # Core high-intensity outline
    pygame.draw.polygon(temp_surf, (*color[:3], 255), local_pts, int(thickness))
    # Bright white center core if color is saturated
    bright_core = (255, 255, 255, 255) if sum(color[:3]) > 200 else color
    pygame.draw.polygon(temp_surf, bright_core, local_pts, 1)

    surface.blit(temp_surf, (min_x, min_y))

def draw_glow_line(surface, start, end, color, glow_radius=8, thickness=2):
    """Draws a neon glowing line segment."""
    min_x = min(start[0], end[0]) - glow_radius - 5
    max_x = max(start[0], end[0]) + glow_radius + 5
    min_y = min(start[1], end[1]) - glow_radius - 5
    max_y = max(start[1], end[1]) + glow_radius + 5
    w = int(max_x - min_x)
    h = int(max_y - min_y)

    if w <= 0 or h <= 0:
        return

    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    l_start = (start[0] - min_x, start[1] - min_y)
    l_end = (end[0] - min_x, end[1] - min_y)

    # Layer outlines
    for g in range(glow_radius, 1, -2):
        alpha = int(100 * (1.0 - (g - 1) / glow_radius))
        c = (*color[:3], alpha)
        pygame.draw.line(temp_surf, c, l_start, l_end, int(thickness + g))

    pygame.draw.line(temp_surf, (255, 255, 255, 255), l_start, l_end, int(thickness))
    surface.blit(temp_surf, (min_x, min_y))

def draw_glow_circle(surface, center, radius, color, glow_radius=10, fill=False, thickness=2):
    """Draws a neon glowing circle."""
    cx, cy = int(center[0]), int(center[1])
    r = int(radius)
    min_x = cx - r - glow_radius - 5
    max_x = cx + r + glow_radius + 5
    min_y = cy - r - glow_radius - 5
    max_y = cy + r + glow_radius + 5
    w = int(max_x - min_x)
    h = int(max_y - min_y)

    if w <= 0 or h <= 0:
        return

    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    local_c = (cx - min_x, cy - min_y)

    # Layered glows
    for g in range(glow_radius, 0, -2):
        alpha = int(100 * (1.0 - g / glow_radius))
        c = (*color[:3], alpha)
        pygame.draw.circle(temp_surf, c, local_c, r + g, int(thickness) if not fill else 0)

    pygame.draw.circle(temp_surf, (*color[:3], 255), local_c, r, int(thickness) if not fill else 0)
    if not fill:
        pygame.draw.circle(temp_surf, (255, 255, 255, 255), local_c, r, 1)

    surface.blit(temp_surf, (min_x, min_y))

def draw_rotated_sprite(surface, image, center, angle_deg):
    """Draws a sprite rotated by angle_deg centered at center."""
    rotated_image = pygame.transform.rotate(image, angle_deg)
    new_rect = rotated_image.get_rect(center=center)
    surface.blit(rotated_image, new_rect.topleft)

# ==========================================
# 4. PARTICLE EFFECTS & ENVIRONMENTAL OBJECTS
# ==========================================
class Star:
    """A scrolling background star for parallax 3D effect."""
    def __init__(self):
        self.reset(True)

    def reset(self, randomize_y=False):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT) if randomize_y else 0
        self.z = random.uniform(1.0, 4.0) # Depth. Larger Z = closer, faster, brighter
        self.speed = (5.0 / self.z) * 1.5

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surface):
        # Scale brightness and size with depth Z
        brightness = int(255 / (self.z * 0.7))
        brightness = max(50, min(255, brightness))
        size = int(3.5 / self.z)
        size = max(1, size)
        color = (brightness, brightness, min(255, int(brightness * 1.15))) # slight blue shift
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)


class Particle:
    """Individual particle used for explosions, engines, and sparks."""
    def __init__(self, x, y, vx, vy, color, size, lifespan, drag=0.98, decay=1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.max_life = lifespan
        self.life = lifespan
        self.size = size
        self.drag = drag
        self.decay = decay

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.drag
        self.vy *= self.drag
        self.life -= self.decay
        return self.life > 0

    def draw(self, surface):
        alpha_ratio = self.life / self.max_life
        alpha = int(255 * alpha_ratio)
        c = (*self.color[:3], alpha)
        sz = int(self.size * alpha_ratio)
        sz = max(1, sz)

        # Draw transparent pixel/circle
        s = pygame.Surface((sz*2, sz*2), pygame.SRCALPHA)
        pygame.draw.circle(s, c, (sz, sz), sz)
        surface.blit(s, (int(self.x - sz), int(self.y - sz)))


class ParticleSystem:
    """Manages spawning, updating, and drawing all active game particles."""
    def __init__(self):
        self.particles = []

    def clear(self):
        self.particles.clear()

    def spawn_explosion(self, x, y, color, count=25, speed=6.0, size=5):
        """Create radial blast particles."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            mag = random.uniform(1.0, speed)
            vx = math.cos(angle) * mag
            vy = math.sin(angle) * mag
            life = random.randint(15, 35)
            self.particles.append(Particle(x, y, vx, vy, color, random.uniform(2, size), life))

    def spawn_engine_trail(self, x, y, vx, vy, color=ORANGE):
        """Flame trails trailing behind vessels."""
        life = random.randint(8, 15)
        size = random.uniform(2, 4)
        # Add random spread to nozzle output
        evx = vx + random.uniform(-0.5, 0.5)
        evy = vy + random.uniform(-0.5, 0.5)
        self.particles.append(Particle(x, y, evx, evy, color, size, life, drag=0.95))

    def spawn_sparks(self, x, y, direction_vector, color=CYAN):
        """Sparks bouncing off shield/armor hit points."""
        for _ in range(5):
            angle = math.atan2(direction_vector[1], direction_vector[0]) + random.uniform(-0.6, 0.6)
            mag = random.uniform(2.0, 5.0)
            vx = math.cos(angle) * mag
            vy = math.sin(angle) * mag
            life = random.randint(10, 20)
            self.particles.append(Particle(x, y, vx, vy, color, random.uniform(1, 2.5), life, drag=0.97))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


# ==========================================
# 5. WEAPONS, ENEMY & PLAYER ENTITIES
# ==========================================
class Laser:
    """Laser bolt fired by Player or Enemies."""
    def __init__(self, x, y, dx, dy, color, is_player_laser, damage=10, width=3):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.is_player = is_player_laser
        self.damage = damage
        self.width = width
        self.length = 18
        self.radius = 4 # collision box radius

    def update(self):
        self.x += self.dx
        self.y += self.dy
        # Out of bounds check
        return -50 < self.x < WIDTH + 50 and -50 < self.y < HEIGHT + 50

    def draw(self, surface):
        end_x = self.x + self.dx * 1.5
        end_y = self.y + self.dy * 1.5
        draw_glow_line(surface, (self.x, self.y), (end_x, end_y), self.color, glow_radius=6, thickness=self.width)


class PowerUp:
    """Floating reward containers that grant weapon boosts or healing."""
    TYPES = ['SHIELD', 'WEAPON', 'REPAIR']
    COLORS = {
        'SHIELD': CYAN,
        'WEAPON': YELLOW,
        'REPAIR': GREEN
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.color = self.COLORS[self.type]
        self.angle = 0.0
        self.radius = 14
        self.vy = 2.0

    def update(self):
        self.y += self.vy
        self.angle += 0.05
        return self.y < HEIGHT + 50

    def draw(self, surface):
        # Draw pulsing outer glow circle
        pulse = 2 * math.sin(self.angle * 3)
        draw_glow_circle(surface, (self.x, self.y), self.radius + pulse, self.color, glow_radius=8, thickness=2)

        # Render geometric inner shape (rotating cross, triangle, or square)
        r = self.radius - 6
        points = []
        if self.type == 'SHIELD':
            # Diamond
            points = [
                (self.x, self.y - r),
                (self.x + r, self.y),
                (self.x, self.y + r),
                (self.x - r, self.y)
            ]
        elif self.type == 'WEAPON':
            # Triangle pointing up
            points = [
                (self.x, self.y - r),
                (self.x + r * 0.86, self.y + r * 0.5),
                (self.x - r * 0.86, self.y + r * 0.5)
            ]
        elif self.type == 'REPAIR':
            # Cross shape points
            w = r * 0.4
            points = [
                (self.x - w, self.y - r), (self.x + w, self.y - r),
                (self.x + w, self.y - w), (self.x + r, self.y - w),
                (self.x + r, self.y + w), (self.x + w, self.y + w),
                (self.x + w, self.y + r), (self.x - w, self.y - r + r*2),
                (self.x - w, self.y + w), (self.x - r, self.y + w),
                (self.x - r, self.y - w), (self.x - w, self.y - w)
            ]

        if points:
            # Rotate points slightly for dynamic aesthetic
            rotated = []
            for px, py in points:
                # shift to origin
                tx = px - self.x
                ty = py - self.y
                # rotate
                rx = tx * math.cos(self.angle) - ty * math.sin(self.angle)
                ry = tx * math.sin(self.angle) + ty * math.cos(self.angle)
                rotated.append((rx + self.x, ry + self.y))

            pygame.draw.polygon(surface, WHITE, rotated, 1)


class Player:
    """The player spaceship, holding scores, life states, weapons, and dynamics."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.vx = 0.0
        self.vy = 0.0
        self.accel = 0.7
        self.max_speed = 6.5
        self.friction = 0.90
        
        self.health = 100
        self.max_health = 100
        self.shield = 50
        self.max_shield = 100
        
        self.weapon_level = 1
        self.shoot_cooldown = 0
        self.shoot_delay = 14  # frames (approx 0.23 seconds)

        self.invincibility_time = 0
        self.angle_tilt = 0.0  # visual banking angle
        self.radius = 20       # collision box radius

    def get_hit(self, damage, particles):
        if self.invincibility_time > 0:
            return False

        # Shield absorbs damage first
        if self.shield > 0:
            self.shield -= damage
            sound_system.play('hit')
            if self.shield < 0:
                self.health += self.shield  # subtract overflow from health
                self.shield = 0
            # blue sparks for shield hits
            particles.spawn_sparks(self.x, self.y, (0, -1), CYAN)
        else:
            self.health -= damage
            sound_system.play('hit')
            # red sparks for hull damage
            particles.spawn_sparks(self.x, self.y, (0, -1), RED)

        self.invincibility_time = 45  # Invincible for 0.75 seconds
        return True

    def upgrade_weapon(self):
        if self.weapon_level < 4:
            self.weapon_level += 1
            return True
        return False

    def recharge_shield(self, amount):
        old = self.shield
        self.shield = min(self.max_shield, self.shield + amount)
        return self.shield > old

    def repair_hull(self, amount):
        old = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health > old

    def update(self, keys, lasers, particles):
        # 1. Handle Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincibility_time > 0:
            self.invincibility_time -= 1

        # 2. Movement Inputs (Forces)
        ax = 0.0
        ay = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax = -self.accel
            self.angle_tilt = min(0.35, self.angle_tilt + 0.04) # bank left
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax = self.accel
            self.angle_tilt = max(-0.35, self.angle_tilt - 0.04) # bank right
        else:
            self.angle_tilt *= 0.85 # slowly return to center

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ay = -self.accel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ay = self.accel

        # 3. Physics Integration
        self.vx += ax
        self.vy += ay

        # Speed Limiting
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed

        # Inertia friction
        self.vx *= self.friction
        self.vy *= self.friction

        # Move ship
        self.x += self.vx
        self.y += self.vy

        # Limit movement to screen boundary
        self.x = max(25, min(WIDTH - 25, self.x))
        self.y = max(25, min(HEIGHT - 25, self.y))

        # 4. Engine trail particles
        if abs(self.vx) > 0.5 or abs(self.vy) > 0.5 or random.random() < 0.3:
            # Spawn thrust particles pointing opposite to flight
            back_x = self.x - math.sin(self.angle_tilt) * 10
            back_y = self.y + 15
            particles.spawn_engine_trail(back_x, back_y, -self.vx * 0.3, 3.0 + random.uniform(0.5, 1.5))

        # 5. Weapon Shooting
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.fire_weapon(lasers)

    def fire_weapon(self, lasers):
        self.shoot_cooldown = self.shoot_delay
        sound_system.play('laser')

        # Weapon tiers
        if self.weapon_level == 1:
            # Single central laser
            lasers.append(Laser(self.x, self.y - 15, 0, -11, CYAN, is_player_laser=True, damage=12, width=3))
        elif self.weapon_level == 2:
            # Double parallel lasers
            lasers.append(Laser(self.x - 10, self.y - 8, 0, -11, CYAN, is_player_laser=True, damage=10, width=2.5))
            lasers.append(Laser(self.x + 10, self.y - 8, 0, -11, CYAN, is_player_laser=True, damage=10, width=2.5))
        elif self.weapon_level == 3:
            # Spread shot (3 rays)
            lasers.append(Laser(self.x, self.y - 15, 0, -12, CYAN, is_player_laser=True, damage=10, width=2.5))
            lasers.append(Laser(self.x - 5, self.y - 10, -2.5, -11.5, CYAN, is_player_laser=True, damage=8, width=2))
            lasers.append(Laser(self.x + 5, self.y - 10, 2.5, -11.5, CYAN, is_player_laser=True, damage=8, width=2))
        else:
            # Super Weapon: Double Parallel + Left/Right angles
            lasers.append(Laser(self.x - 8, self.y - 15, 0, -12, CYAN, is_player_laser=True, damage=10, width=2.5))
            lasers.append(Laser(self.x + 8, self.y - 15, 0, -12, CYAN, is_player_laser=True, damage=10, width=2.5))
            lasers.append(Laser(self.x - 12, self.y - 5, -4.0, -10.5, CYAN, is_player_laser=True, damage=8, width=2))
            lasers.append(Laser(self.x + 12, self.y - 5, 4.0, -10.5, CYAN, is_player_laser=True, damage=8, width=2))

    def draw(self, surface, sprites=None):
        # Apply blinking if invincible
        if self.invincibility_time > 0 and (self.invincibility_time // 4) % 2 == 0:
            return

        cos_a = math.cos(self.angle_tilt)
        sin_a = math.sin(self.angle_tilt)

        if sprites and 'player' in sprites:
            draw_rotated_sprite(surface, sprites['player'], (int(self.x), int(self.y)), -math.degrees(self.angle_tilt))
        else:
            # Build rotated coordinates for ship polygon based on banking angle_tilt
            base_points = [
                (0, -20),   # Nose
                (-16, 15),  # Left wing
                (-6, 8),    # Inner left
                (6, 8),     # Inner right
                (16, 15)    # Right wing
            ]

            rotated_pts = []
            for px, py in base_points:
                # Rotate point and shift to self.x, self.y
                rx = px * cos_a - py * sin_a + self.x
                ry = px * sin_a + py * cos_a + self.y
                rotated_pts.append((rx, ry))

            # Draw Player Neon Ship
            draw_glow_polygon(surface, rotated_pts, CYAN, glow_radius=10, thickness=2)

        # Draw engine core glow (circle behind thrusters)
        thruster_pos = (
            int(self.x + sin_a * 15),
            int(self.y + cos_a * 15)
        )
        draw_glow_circle(surface, thruster_pos, 5 + random.randint(0, 3), ORANGE, glow_radius=8, fill=True)

        # Draw active shield ring
        if self.shield > 0:
            # Shield grows slightly with higher values, pulses over time
            pulse = 1.5 * math.sin(pygame.time.get_ticks() * 0.01)
            shield_radius = self.radius + 12 + pulse
            alpha = int(70 + 30 * (self.shield / self.max_shield))
            # Blit cyan shield outline with glow
            draw_glow_circle(surface, (self.x, self.y), shield_radius, CYAN, glow_radius=12, thickness=2)


# ==========================================
# 6. ENEMY FLEET CLASSES
# ==========================================
class Enemy:
    """Base class for all enemy targets."""
    def __init__(self, x, y, hp, speed, color, points):
        self.x = x
        self.y = y
        self.health = hp
        self.max_health = hp
        self.speed = speed
        self.color = color
        self.points = points
        self.shoot_cooldown = random.randint(30, 90)
        self.radius = 15
        self.anim_timer = random.uniform(0.0, 10.0)

    def get_hit(self, damage, particles):
        self.health -= damage
        sound_system.play('hit')
        particles.spawn_sparks(self.x, self.y, (0, 1), self.color)
        return self.health <= 0

    def update(self, player, lasers, particles):
        self.y += self.speed
        self.anim_timer += 0.05
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Bounds check
        return self.y < HEIGHT + 50

    def draw(self, surface, sprites=None, player=None):
        pass


class ScoutEnemy(Enemy):
    """Fires no shots but flies fast in a wavy horizontal trajectory."""
    def __init__(self):
        super().__init__(
            x=random.randint(100, WIDTH - 100),
            y=-50,
            hp=10,
            speed=2.4,
            color=MAGENTA,
            points=100
        )
        self.radius = 11
        self.wave_width = random.uniform(4.0, 7.0)
        self.wave_freq = random.uniform(0.04, 0.07)
        self.start_x = self.x

    def update(self, player, lasers, particles):
        # Horizontal movement based on sine wave
        self.x = self.start_x + math.sin(self.y * self.wave_freq) * (self.wave_width * 15)
        # Gentle rotation angle for drawing
        self.angle = math.cos(self.y * self.wave_freq) * 0.4
        
        # Engine trails
        if random.random() < 0.2:
            particles.spawn_engine_trail(self.x, self.y - 10, 0, -2.0, MAGENTA)

        return super().update(player, lasers, particles)

    def draw(self, surface, sprites=None, player=None):
        if sprites and 'scout' in sprites:
            draw_rotated_sprite(surface, sprites['scout'], (int(self.x), int(self.y)), 180 - math.degrees(self.angle))
        else:
            base_points = [
                (0, 14),   # Nose
                (-12, -8), # Left Wing
                (-3, -2),  # Mid Left
                (0, -8),   # Back Core
                (3, -2),   # Mid Right
                (12, -8)   # Right Wing
            ]
            
            rotated = []
            cos_a = math.cos(self.angle)
            sin_a = math.sin(self.angle)
            for px, py in base_points:
                rx = px * cos_a - py * sin_a + self.x
                ry = px * sin_a + py * cos_a + self.y
                rotated.append((rx, ry))

            draw_glow_polygon(surface, rotated, self.color, glow_radius=8)


class StrikerEnemy(Enemy):
    """Aggressive drone that tracks and shoots single direct lasers."""
    def __init__(self):
        super().__init__(
            x=random.randint(80, WIDTH - 80),
            y=-50,
            hp=18,
            speed=1.6,
            color=RED,
            points=200
        )
        self.radius = 14
        self.shoot_delay = random.randint(70, 110)
        self.shoot_cooldown = random.randint(20, 60)

    def update(self, player, lasers, particles):
        # AI: Move down but slide slightly towards player horizontal position
        dx = player.x - self.x
        if abs(dx) > 10:
            self.x += (dx / abs(dx)) * 0.8

        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            sound_system.play('enemy_laser')
            
            # Fire laser towards player direction (aimed slightly)
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                vx = (dx / dist) * 7.5
                vy = (dy / dist) * 7.5
                lasers.append(Laser(self.x, self.y + 12, vx, vy, RED, is_player_laser=False, damage=15, width=2.5))

        if random.random() < 0.25:
            particles.spawn_engine_trail(self.x, self.y - 12, 0, -1.5, RED)

        return super().update(player, lasers, particles)

    def draw(self, surface, sprites=None, player=None):
        if sprites and 'striker' in sprites:
            angle_deg = 180
            if player:
                dx = player.x - self.x
                dy = player.y - self.y
                angle_rad = math.atan2(dy, dx)
                # Convert to degrees, subtract 90 because sprite standard is pointing UP
                angle_deg = -math.degrees(angle_rad) - 90
            draw_rotated_sprite(surface, sprites['striker'], (int(self.x), int(self.y)), angle_deg)
        else:
            points = [
                (0, 16),    # Nose
                (-12, 4),   # Left edge
                (-8, -12),  # Left tail
                (0, -4),    # Center base
                (8, -12),   # Right tail
                (12, 4)     # Right edge
            ]
            translated = [(px + self.x, py + self.y) for px, py in points]
            draw_glow_polygon(surface, translated, self.color, glow_radius=9)


class CruiserEnemy(Enemy):
    """Slow tanky flagship that shoots a heavy triple-laser spread."""
    def __init__(self):
        super().__init__(
            x=random.randint(120, WIDTH - 120),
            y=-70,
            hp=35,
            speed=0.8,
            color=YELLOW,
            points=400
        )
        self.radius = 28
        self.shoot_delay = 140
        self.shoot_cooldown = random.randint(40, 80)

    def update(self, player, lasers, particles):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            sound_system.play('enemy_laser')
            
            # Fire heavy 3-laser spread straight down
            lasers.append(Laser(self.x, self.y + 22, 0, 5.5, YELLOW, is_player_laser=False, damage=20, width=4.0))
            lasers.append(Laser(self.x - 15, self.y + 15, -1.5, 5.0, YELLOW, is_player_laser=False, damage=15, width=3.0))
            lasers.append(Laser(self.x + 15, self.y + 15, 1.5, 5.0, YELLOW, is_player_laser=False, damage=15, width=3.0))

        # Twin engine exhaust trails
        if random.random() < 0.4:
            particles.spawn_engine_trail(self.x - 12, self.y - 20, 0, -1.0, YELLOW)
            particles.spawn_engine_trail(self.x + 12, self.y - 20, 0, -1.0, YELLOW)

        return super().update(player, lasers, particles)

    def draw(self, surface, sprites=None, player=None):
        if sprites and 'cruiser' in sprites:
            draw_rotated_sprite(surface, sprites['cruiser'], (int(self.x), int(self.y)), 180)
        else:
            # Heavy Cruiser polygon layout
            points = [
                (0, 26),     # Front main cannon
                (-18, 12),   # Front Left
                (-26, -10),  # Heavy Left shield wing
                (-12, -22),  # Rear Left stabilizer
                (0, -14),    # Engine intake center
                (12, -22),   # Rear Right stabilizer
                (26, -10),   # Heavy Right shield wing
                (18, 12)     # Front Right
            ]
            translated = [(px + self.x, py + self.y) for px, py in points]
            draw_glow_polygon(surface, translated, self.color, glow_radius=14, thickness=3)


class BossEnemy(Enemy):
    """Three-phase dreadnought boss. Health bar display & high-damage attacks."""
    def __init__(self):
        super().__init__(
            x=WIDTH // 2,
            y=-150,
            hp=600,
            speed=0.4,
            color=RED,
            points=3000
        )
        self.radius = 70
        self.target_y = 120
        self.horizontal_dir = 1
        self.phase = 1
        self.phase_timer = 0
        self.alarm_timer = 0
        sound_system.play('boss_alarm')

    def get_hit(self, damage, particles):
        dead = super().get_hit(damage, particles)
        
        # Calculate phase thresholds
        health_pct = self.health / self.max_health
        if health_pct < 0.35 and self.phase < 3:
            self.phase = 3
            self.color = MAGENTA
            sound_system.play('boss_alarm')
        elif health_pct < 0.70 and self.phase < 2:
            self.phase = 2
            self.color = ORANGE
            sound_system.play('boss_alarm')
            
        return dead

    def update(self, player, lasers, particles):
        self.phase_timer += 1
        self.anim_timer += 0.03
        
        # Phase alarms
        self.alarm_timer += 1
        if self.alarm_timer % 120 == 0 and self.health > 0:
            sound_system.play('boss_alarm')

        # 1. Entrance movement
        if self.y < self.target_y:
            self.y += 1.0
        else:
            # Horizontal side-to-side hovering
            self.x += self.horizontal_dir * self.speed
            if self.x > WIDTH - 180:
                self.horizontal_dir = -1
            elif self.x < 180:
                self.horizontal_dir = 1

        # 2. Phase-Based Attack Behaviors
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            self._execute_attack(player, lasers)

        # 3. Engine smoke systems
        if random.random() < 0.6:
            particles.spawn_engine_trail(self.x - 45, self.y - 40, 0, -1.0, self.color)
            particles.spawn_engine_trail(self.x, self.y - 45, 0, -1.0, self.color)
            particles.spawn_engine_trail(self.x + 45, self.y - 40, 0, -1.0, self.color)

        return self.health > 0 # Never despawns off bounds

    def _execute_attack(self, player, lasers):
        if self.phase == 1:
            self.shoot_cooldown = 45
            sound_system.play('enemy_laser')
            # 5-laser spread downward
            for angle in [-2.0, -1.0, 0, 1.0, 2.0]:
                lasers.append(Laser(self.x + angle*10, self.y + 35, angle, 6.0, RED, is_player_laser=False, damage=12, width=3))
        
        elif self.phase == 2:
            self.shoot_cooldown = 20
            sound_system.play('enemy_laser')
            # Rapid spray sweeping left to right
            sweep_angle = 3.5 * math.sin(self.phase_timer * 0.15)
            lasers.append(Laser(self.x, self.y + 35, sweep_angle, 6.5, ORANGE, is_player_laser=False, damage=14, width=3))
            lasers.append(Laser(self.x - 30, self.y + 20, sweep_angle - 0.5, 6.0, ORANGE, is_player_laser=False, damage=10, width=2.5))
            lasers.append(Laser(self.x + 30, self.y + 20, sweep_angle + 0.5, 6.0, ORANGE, is_player_laser=False, damage=10, width=2.5))

        elif self.phase == 3:
            self.shoot_cooldown = 60
            sound_system.play('enemy_laser')
            # Mega radial nova spray (12 directions)
            for i in range(12):
                ang = (i / 12) * 2 * math.pi
                vx = math.cos(ang) * 5.0
                vy = math.sin(ang) * 5.0
                lasers.append(Laser(self.x, self.y, vx, vy, MAGENTA, is_player_laser=False, damage=15, width=3))
            
            # Additional heavy targeted laser
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                vx = (dx / dist) * 8.5
                vy = (dy / dist) * 8.5
                lasers.append(Laser(self.x, self.y + 30, vx, vy, WHITE, is_player_laser=False, damage=25, width=4.5))

    def draw(self, surface, sprites=None, player=None):
        if sprites and 'boss' in sprites:
            rocking = 12 * math.sin(self.anim_timer)
            draw_rotated_sprite(surface, sprites['boss'], (int(self.x), int(self.y)), 180 + rocking)
        else:
            # Boss Fortress Polygon
            points = [
                (0, 50),      # Main center blaster spike
                (-25, 30),    # Left inner armor
                (-55, 30),    # Left hangerbay bay
                (-75, -5),    # Left heavy wing generator
                (-50, -40),   # Left rear stabilizer
                (0, -30),     # Rear main engine block
                (50, -40),    # Right rear stabilizer
                (75, -5),     # Right heavy wing generator
                (55, 30),     # Right hangerbay bay
                (25, 30)      # Right inner armor
            ]
            
            translated = [(px + self.x, py + self.y) for px, py in points]
            draw_glow_polygon(surface, translated, self.color, glow_radius=18, thickness=3)

            # Draw glowing cores (engine/reactors) on top
            core_pos_left = (int(self.x - 30), int(self.y - 10))
            core_pos_right = (int(self.x + 30), int(self.y - 10))
            core_pulse = 2 * math.sin(self.anim_timer * 10)
            
            draw_glow_circle(surface, core_pos_left, 8 + core_pulse, self.color, glow_radius=10, fill=True)
            draw_glow_circle(surface, core_pos_right, 8 + core_pulse, self.color, glow_radius=10, fill=True)


# ==========================================
# 7. INTERACTIVE HEADS UP DISPLAY (HUD)
# ==========================================
class FloatingText:
    """Drifting texts notifying points scored or weapon level upgrades."""
    def __init__(self, x, y, text, color=WHITE, size=20, duration=45):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.max_life = duration
        self.life = duration
        self.font = pygame.font.SysFont("Courier New", size, bold=True)

    def update(self):
        self.y -= 1.2  # drift up
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha_ratio = self.life / self.max_life
        alpha = int(255 * alpha_ratio)
        
        # Render text surface
        text_surf = self.font.render(self.text, True, self.color)
        
        # Apply alpha blending transparency safely
        alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, alpha))
        text_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Center blit position
        pos = (int(self.x - text_surf.get_width() // 2), int(self.y - text_surf.get_height() // 2))
        surface.blit(text_surf, pos)


# ==========================================
# 8. CORE GAME ENGINE COORDINATOR
# ==========================================
class GameEngine:
    """Manages the full state machine, events, physics loops, and blits."""
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_GAMEOVER = 2
    STATE_SETTINGS = 3
    STATE_PAUSED = 4

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CYBER-SHOOTER 2088")
        self.clock = pygame.time.Clock()
        self.state = self.STATE_MENU

        # Fonts
        self.title_font = pygame.font.SysFont("Courier New", 54, bold=True)
        self.header_font = pygame.font.SysFont("Courier New", 32, bold=True)
        self.body_font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.hud_font = pygame.font.SysFont("Courier New", 18, bold=True)

        # Highscore loading
        self.highscore_file = "highscore.txt"
        self.highscore = self.load_highscore()

        # Engine Components Setup
        self.stars = [Star() for _ in range(70)]
        self.particles = ParticleSystem()
        
        # Playable states variables
        self.player = Player()
        self.lasers = []
        self.enemies = []
        self.powerups = []
        self.floaters = []
        
        self.score = 0
        self.level = 1
        
        # Screen Shake configs
        self.shake_intensity = 0.0
        self.shake_decay = 0.90

        # Spawning timers
        self.enemy_spawn_timer = 0
        self.boss_spawned = False
        self.game_time = 0

        # Assets & Scrolling Background
        self.sprites = {}
        self.bg_scroll_y = 0.0
        self.load_sprites()

    def load_sprites(self):
        sizes = {
            'player': (64, 64),
            'scout': (36, 36),
            'striker': (42, 42),
            'cruiser': (80, 80),
            'boss': (220, 220)
        }
        for name, size in sizes.items():
            path = f"{name}.png"
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    scaled_img = pygame.transform.scale(img, size)
                    self.sprites[name] = scaled_img
                except Exception as e:
                    print(f"Error loading/scaling sprite {name}: {e}")
                    
        # Load background
        bg_path = "background.jpg"
        if os.path.exists(bg_path):
            try:
                img = pygame.image.load(bg_path).convert()
                self.sprites['background'] = pygame.transform.scale(img, (WIDTH, HEIGHT))
            except Exception as e:
                print(f"Error loading background: {e}")

    def load_highscore(self):
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, 'r') as f:
                    return int(f.read().strip())
            except Exception:
                return 0
        return 0

    def save_highscore(self):
        try:
            with open(self.highscore_file, 'w') as f:
                f.write(str(self.highscore))
        except Exception:
            pass

    def start_new_game(self):
        self.player.reset()
        self.lasers.clear()
        self.enemies.clear()
        self.powerups.clear()
        self.floaters.clear()
        self.particles.clear()
        self.score = 0
        self.level = 1
        self.boss_spawned = False
        self.enemy_spawn_timer = 0
        self.game_time = 0
        self.shake_intensity = 0.0
        self.state = self.STATE_PLAYING

    def trigger_screen_shake(self, intensity):
        self.shake_intensity = max(self.shake_intensity, intensity)

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        
        # Difficulty scaling base curves
        spawn_rate = max(40, 110 - (self.level * 12)) # lower is faster spawns
        
        # Don't spawn normal minion fleets if Boss is alive
        boss_alive = any(isinstance(e, BossEnemy) for e in self.enemies)
        if boss_alive:
            # Boss summons scouts and strikers occasionally
            if self.enemy_spawn_timer % 180 == 0:
                self.enemies.append(ScoutEnemy())
                self.enemies.append(StrikerEnemy())
            return

        # Spawns boss dreadnought at 3000 points
        if self.score >= 3000 and not self.boss_spawned:
            self.boss_spawned = True
            self.enemies.append(BossEnemy())
            self.floaters.append(FloatingText(WIDTH//2, HEIGHT//3, "BOSS WARNING!", RED, size=38, duration=150))
            self.trigger_screen_shake(15)
            return

        # Regular spawning cycle
        if self.enemy_spawn_timer >= spawn_rate:
            self.enemy_spawn_timer = 0
            
            # Level 1: Scouts only
            # Level 2+: Strikers introduced
            # Level 4+: Heavy Cruisers introduced
            spawn_pool = [ScoutEnemy]
            if self.level >= 2:
                spawn_pool.append(StrikerEnemy)
            if self.level >= 3:
                spawn_pool.append(CruiserEnemy)
                
            enemy_class = random.choice(spawn_pool)
            self.enemies.append(enemy_class())

    def update_physics(self):
        self.game_time += 1
        
        # 1. Update Starfield
        for star in self.stars:
            star.update()

        # 2. Spawn enemies
        self.spawn_enemies()

        # 3. Update active entities
        self.particles.update()
        
        # Update Player controls & physics
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.lasers, self.particles)

        # Update Projectiles
        self.lasers = [l for l in self.lasers if l.update()]

        # Update Enemy Positions
        self.enemies = [e for e in self.enemies if e.update(self.player, self.lasers, self.particles)]

        # Update Powerups
        self.powerups = [p for p in self.powerups if p.update()]

        # Update HUD floaters
        self.floaters = [f for f in self.floaters if f.update()]

        # 4. Handle Level progression (every 1000 points unlocks new level difficulty)
        new_level = 1 + (self.score // 1200)
        if new_level != self.level:
            self.level = new_level
            self.floaters.append(FloatingText(WIDTH//2, HEIGHT//2, f"LEVEL {self.level} ARCHIVED!", YELLOW, size=32, duration=100))
            sound_system.play('powerup')

        # 5. Collision Checks
        self.process_collisions()

        # 6. Screen shake decay
        if self.shake_intensity > 0.1:
            self.shake_intensity *= self.shake_decay
        else:
            self.shake_intensity = 0.0

        # Check death trigger
        if self.player.health <= 0:
            sound_system.play('explosion_boss')
            self.particles.spawn_explosion(self.player.x, self.player.y, CYAN, count=70, speed=10.0, size=8)
            self.state = self.STATE_GAMEOVER
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

    def process_collisions(self):
        # A. Lasers hitting targets
        for laser in list(self.lasers):
            if laser.is_player:
                # Player laser hits Enemy
                for enemy in list(self.enemies):
                    dist = math.hypot(laser.x - enemy.x, laser.y - enemy.y)
                    if dist < enemy.radius + laser.radius:
                        # Laser impact spark spray
                        self.particles.spawn_sparks(laser.x, laser.y, (0, -1), laser.color)
                        
                        # Apply damage to enemy
                        is_dead = enemy.get_hit(laser.damage, self.particles)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            
                        if is_dead:
                            sound_system.play('explosion')
                            self.particles.spawn_explosion(enemy.x, enemy.y, enemy.color, count=30, speed=5.5)
                            self.score += enemy.points
                            self.floaters.append(FloatingText(enemy.x, enemy.y, f"+{enemy.points}", enemy.color, size=16))
                            self.trigger_screen_shake(4)
                            
                            # Reward roll: 15% chance of spawning power-up upon minion death
                            if not isinstance(enemy, BossEnemy):
                                if random.random() < 0.16:
                                    self.powerups.append(PowerUp(enemy.x, enemy.y))
                            else:
                                # Boss death spawns multi-upgrades and wins the game!
                                self.trigger_screen_shake(25)
                                self.particles.spawn_explosion(enemy.x, enemy.y, WHITE, count=150, speed=12.0, size=10)
                                sound_system.play('explosion_boss')
                                for _ in range(3):
                                    self.powerups.append(PowerUp(enemy.x + random.randint(-40, 40), enemy.y))
                                self.enemies.remove(enemy)
                                self.floaters.append(FloatingText(WIDTH//2, HEIGHT//2, "DREADNOUGHT SLAIN! +5000", CYAN, size=36, duration=150))
                                self.score += 5000
                        break
            else:
                # Enemy laser hits Player
                dist = math.hypot(laser.x - self.player.x, laser.y - self.player.y)
                # Player shield/hitbox check
                shield_rad = self.player.radius + 12 if self.player.shield > 0 else self.player.radius
                if dist < shield_rad + laser.radius:
                    if self.player.get_hit(laser.damage, self.particles):
                        self.trigger_screen_shake(8)
                    if laser in self.lasers:
                        self.lasers.remove(laser)

        # B. Direct Ship-to-Ship body collisions
        for enemy in list(self.enemies):
            dist = math.hypot(self.player.x - enemy.x, self.player.y - enemy.y)
            shield_rad = self.player.radius + 12 if self.player.shield > 0 else self.player.radius
            if dist < shield_rad + enemy.radius:
                # Massive damage to player (ramming check)
                damage_amt = 40 if isinstance(enemy, CruiserEnemy) else 25
                if not isinstance(enemy, BossEnemy):
                    if self.player.get_hit(damage_amt, self.particles):
                        self.trigger_screen_shake(12)
                    sound_system.play('explosion')
                    self.particles.spawn_explosion(enemy.x, enemy.y, enemy.color, count=30, speed=6.0)
                    self.enemies.remove(enemy)
                else:
                    # Rammimg boss causes immediate shield drain
                    if self.player.get_hit(50, self.particles):
                        self.trigger_screen_shake(15)

        # C. Player collects Powerups
        for pu in list(self.powerups):
            dist = math.hypot(self.player.x - pu.x, self.player.y - pu.y)
            if dist < self.player.radius + pu.radius:
                sound_system.play('powerup')
                self.powerups.remove(pu)
                
                if pu.type == 'SHIELD':
                    recharged = self.player.recharge_shield(35)
                    self.floaters.append(FloatingText(self.player.x, self.player.y - 20, "SHIELD CHARGED", CYAN, size=18))
                elif pu.type == 'WEAPON':
                    upgraded = self.player.upgrade_weapon()
                    txt = f"WEAPON LVL {self.player.weapon_level}!" if upgraded else "WEAPON MAX LEVEL!"
                    self.floaters.append(FloatingText(self.player.x, self.player.y - 20, txt, YELLOW, size=18))
                elif pu.type == 'REPAIR':
                    repaired = self.player.repair_hull(25)
                    self.floaters.append(FloatingText(self.player.x, self.player.y - 20, "HEALTH REPAIRED", GREEN, size=18))
                
                # Neon absorption fireworks
                self.particles.spawn_explosion(pu.x, pu.y, pu.color, count=15, speed=3.0, size=3)

    # ==========================================
    # 9. GRAPHICS RENDERING & LAYOUTS
    # ==========================================
    def draw_hud(self):
        # 1. Health Integrity Bar (Neon Green)
        hud_y = HEIGHT - 40
        pygame.draw.rect(self.screen, DARK_GRAY, (40, hud_y, 160, 16), border_radius=4)
        hp_width = int(160 * (self.player.health / self.player.max_health))
        if hp_width > 0:
            pygame.draw.rect(self.screen, GREEN, (40, hud_y, hp_width, 16), border_radius=4)
        # Outline
        pygame.draw.rect(self.screen, WHITE, (40, hud_y, 160, 16), 1, border_radius=4)
        hp_label = self.hud_font.render("HEALTH", True, GREEN)
        self.screen.blit(hp_label, (40, hud_y - 22))

        # 2. Energy Shield Bar (Neon Cyan)
        pygame.draw.rect(self.screen, DARK_GRAY, (220, hud_y, 160, 16), border_radius=4)
        sh_width = int(160 * (self.player.shield / self.player.max_shield))
        if sh_width > 0:
            pygame.draw.rect(self.screen, CYAN, (220, hud_y, sh_width, 16), border_radius=4)
        pygame.draw.rect(self.screen, WHITE, (220, hud_y, 160, 16), 1, border_radius=4)
        sh_label = self.hud_font.render("SHIELD", True, CYAN)
        self.screen.blit(sh_label, (220, hud_y - 22))

        # 3. Numeric Score & HighScore
        score_lbl = self.hud_font.render(f"SCORE: {self.score:05d}", True, WHITE)
        self.screen.blit(score_lbl, (WIDTH - 180, 25))
        
        hi_lbl = self.hud_font.render(f"HI-SCORE: {self.highscore:05d}", True, LIGHT_GRAY)
        self.screen.blit(hi_lbl, (WIDTH - 220, 50))
        
        lvl_lbl = self.hud_font.render(f"SECTOR: {self.level:02d}", True, YELLOW)
        self.screen.blit(lvl_lbl, (40, 25))

        # 4. Boss Health Bar (top overlay if active)
        for enemy in self.enemies:
            if isinstance(enemy, BossEnemy):
                bar_w = 500
                bar_h = 14
                bx = (WIDTH - bar_w) // 2
                by = 40
                
                # Draw Boss frame
                pygame.draw.rect(self.screen, DARK_GRAY, (bx, by, bar_w, bar_h), border_radius=3)
                boss_hp_pct = max(0, enemy.health / enemy.max_health)
                boss_w = int(bar_w * boss_hp_pct)
                if boss_w > 0:
                    pygame.draw.rect(self.screen, enemy.color, (bx, by, boss_w, bar_h), border_radius=3)
                pygame.draw.rect(self.screen, WHITE, (bx, by, bar_w, bar_h), 1, border_radius=3)
                
                boss_lbl = self.hud_font.render("DREADNOUGHT FLAGSHIP CLASS", True, enemy.color)
                self.screen.blit(boss_lbl, (bx, by - 22))

    def draw_menu(self):
        # Pulsing text colors
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
        title_color = (int(0 + 50 * pulse), int(220 + 35 * pulse), 255)
        
        # Title rendering
        title_surf = self.title_font.render("CYBER-SHOOTER 2088", True, title_color)
        t_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
        self.screen.blit(title_surf, t_rect)

        # Spaceship graphic decoration (Sprite with slow float & rock animation)
        if 'player' in self.sprites:
            scaled_player = pygame.transform.scale(self.sprites['player'], (120, 120))
            hover_offset = 6 * math.sin(pygame.time.get_ticks() * 0.003)
            center_pos = (WIDTH//2, HEIGHT//3 + 120 + int(hover_offset))
            rocking_angle = 8 * math.sin(pygame.time.get_ticks() * 0.002)
            draw_rotated_sprite(self.screen, scaled_player, center_pos, rocking_angle)
        else:
            ship_points = [
                (WIDTH//2, HEIGHT//3 + 80),
                (WIDTH//2 - 25, HEIGHT//3 + 140),
                (WIDTH//2, HEIGHT//3 + 125),
                (WIDTH//2 + 25, HEIGHT//3 + 140)
            ]
            draw_glow_polygon(self.screen, ship_points, CYAN, glow_radius=12, thickness=2)

        # Menu options
        opt_start = self.header_font.render("PRESS [ENTER] TO INITIATE", True, WHITE)
        self.screen.blit(opt_start, opt_start.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))
        
        opt_set = self.body_font.render("[C] VIEW CONTROLS & SETTINGS", True, LIGHT_GRAY)
        self.screen.blit(opt_set, opt_set.get_rect(center=(WIDTH//2, HEIGHT//2 + 130)))
        
        opt_exit = self.body_font.render("[ESCAPE] POWER OFF SYSTEM", True, RED)
        self.screen.blit(opt_exit, opt_exit.get_rect(center=(WIDTH//2, HEIGHT//2 + 170)))

        # Subtitle copyright
        copy_lbl = self.hud_font.render("POWERED BY PROGRAMMATIC GLOW & PYGAME", True, DARK_GRAY)
        self.screen.blit(copy_lbl, copy_lbl.get_rect(center=(WIDTH//2, HEIGHT - 50)))

    def draw_settings(self):
        # Settings Header
        title_surf = self.header_font.render("SECTOR CONTROLS & MANUALS", True, YELLOW)
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, HEIGHT//4)))

        # Control mapping descriptions
        controls = [
            ("FLIGHT ACCELERATION", "W / A / S / D  (or ARROW KEYS)"),
            ("NEON BEAM CANNON", "SPACEBAR (HOLD TO ENGAGE)"),
            ("SYSTEM REBOOT (PAUSE)", "P KEY"),
            ("ABORT MISSION (EXIT)", "ESCAPE KEY"),
            ("WEAPON UPGRADES", "WEAPON TIER 1 -> 4 (COINS DROP)"),
            ("SHIELD MATRIX", "ABSORBS IMPACT DAMAGE (SHIELD REPAIR)"),
            ("AUDIO FEEDBACK", f"SOUND HARDWARE ENGAGED: {str(sound_system.enabled).upper()}")
        ]

        start_y = HEIGHT//3 + 10
        for desc, key in controls:
            desc_surf = self.body_font.render(desc, True, LIGHT_GRAY)
            key_surf = self.body_font.render(key, True, CYAN)
            self.screen.blit(desc_surf, (WIDTH//4 - 40, start_y))
            self.screen.blit(key_surf, (WIDTH//2 + 70, start_y))
            start_y += 38

        back_lbl = self.header_font.render("PRESS [ENTER] TO RETURN TO DOCK", True, WHITE)
        self.screen.blit(back_lbl, back_lbl.get_rect(center=(WIDTH//2, HEIGHT - 100)))

    def draw_gameover(self):
        # Flash overlay
        self.screen.fill((25, 5, 5), special_flags=pygame.BLEND_RGB_ADD)
        
        go_surf = self.title_font.render("SYSTEM CRITICAL: DEFEAT", True, RED)
        self.screen.blit(go_surf, go_surf.get_rect(center=(WIDTH//2, HEIGHT//3)))

        # Stats summaries
        stats_score = self.header_font.render(f"FINAL SCORE: {self.score}", True, WHITE)
        self.screen.blit(stats_score, stats_score.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))

        if self.score >= self.highscore and self.score > 0:
            hi_congrats = self.body_font.render("NEW HIGH RECORD SET!", GREEN)
            self.screen.blit(hi_congrats, hi_congrats.get_rect(center=(WIDTH//2, HEIGHT//2 + 25)))

        retry_lbl = self.header_font.render("PRESS [ENTER] TO RESPAWN", True, CYAN)
        self.screen.blit(retry_lbl, retry_lbl.get_rect(center=(WIDTH//2, HEIGHT//2 + 90)))

        quit_lbl = self.body_font.render("PRESS [ESCAPE] TO TERMINATE COMMAND", True, LIGHT_GRAY)
        self.screen.blit(quit_lbl, quit_lbl.get_rect(center=(WIDTH//2, HEIGHT//2 + 140)))

    def draw_paused(self):
        # Draw overlay tint
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        paused_surf = self.title_font.render("TACTICAL PAUSE", True, CYAN)
        self.screen.blit(paused_surf, paused_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))

        resume_surf = self.body_font.render("PRESS [P] TO RESUME ACTION", True, WHITE)
        self.screen.blit(resume_surf, resume_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))

    def run(self):
        running = True
        while running:
            # Locked tick rate
            self.clock.tick(FPS)
            # Draw scrolling background
            if 'background' in self.sprites:
                if self.state == self.STATE_PLAYING:
                    self.bg_scroll_y = (self.bg_scroll_y + 0.8) % HEIGHT
                elif self.state != self.STATE_PAUSED:
                    self.bg_scroll_y = (self.bg_scroll_y + 0.2) % HEIGHT
                
                scroll_y = int(self.bg_scroll_y)
                self.screen.blit(self.sprites['background'], (0, scroll_y))
                self.screen.blit(self.sprites['background'], (0, scroll_y - HEIGHT))
            else:
                self.screen.fill(BG_COLOR)

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if self.state == self.STATE_MENU:
                        if event.key == pygame.K_RETURN:
                            self.start_new_game()
                        elif event.key == pygame.K_c:
                            self.state = self.STATE_SETTINGS
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            
                    elif self.state == self.STATE_SETTINGS:
                        if event.key == pygame.K_RETURN:
                            self.state = self.STATE_MENU
                            
                    elif self.state == self.STATE_PLAYING:
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.STATE_MENU
                        elif event.key == pygame.K_p:
                            self.state = self.STATE_PAUSED
                            
                    elif self.state == self.STATE_PAUSED:
                        if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                            self.state = self.STATE_PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            self.state = self.STATE_MENU
                            
                    elif self.state == self.STATE_GAMEOVER:
                        if event.key == pygame.K_RETURN:
                            self.start_new_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = self.STATE_MENU

            # Update & Render State Machine
            if self.state == self.STATE_PLAYING:
                self.update_physics()

            # Star background (always active, updates only outside pause)
            if self.state != self.STATE_PAUSED:
                for star in self.stars:
                    if self.state != self.STATE_PLAYING:
                        star.update() # static/slowly scrolls on menus

            # Draw Stars
            for star in self.stars:
                star.draw(self.screen)

            # Draw Game entities & handle Screen Shake offsets
            if self.state in [self.STATE_PLAYING, self.STATE_GAMEOVER, self.STATE_PAUSED]:
                # Apply screen shake vector offset
                shake_x = 0
                shake_y = 0
                if self.shake_intensity > 0.0:
                    shake_x = int(random.uniform(-self.shake_intensity, self.shake_intensity))
                    shake_y = int(random.uniform(-self.shake_intensity, self.shake_intensity))

                # Create a temporary surface to draw gameplay (offsetting it for shake)
                game_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                
                # Draw entities
                self.particles.draw(game_surf)
                for laser in self.lasers:
                    laser.draw(game_surf)
                for pu in self.powerups:
                    pu.draw(game_surf)
                for enemy in self.enemies:
                    enemy.draw(game_surf, self.sprites, self.player)
                
                # Only draw player if alive
                if self.player.health > 0:
                    self.player.draw(game_surf, self.sprites)

                for f in self.floaters:
                    f.draw(game_surf)

                # Blit gameplay onto screen with screen shake offset
                self.screen.blit(game_surf, (shake_x, shake_y))

                # Draw UI HUD elements on top (unshaken)
                self.draw_hud()

            # Draw Overlays
            if self.state == self.STATE_MENU:
                self.draw_menu()
            elif self.state == self.STATE_SETTINGS:
                self.draw_settings()
            elif self.state == self.STATE_GAMEOVER:
                self.draw_gameover()
            elif self.state == self.STATE_PAUSED:
                self.draw_paused()

            # Refresh display canvas
            pygame.display.flip()

        pygame.quit()

# ==========================================
# 10. SYSTEM ENTRY POINT
# ==========================================
if __name__ == "__main__":
    game = GameEngine()
    game.run()
