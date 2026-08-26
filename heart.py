import math
import random
import tkinter as tk


class HeartApp:

  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Mathematical Quantum Heart Sandbox")
    self.root.geometry("800x700")
    self.root.configure(bg="#05020a")

    # Canvas for drawing the heart & particles
    self.canvas = tk.Canvas(self.root, bg="#05020a", highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True)

    self.width = 800
    self.height = 700
    self.root.bind("<Configure>", self.on_resize)

    # Heart pulse state
    self.frame = 0
    self.particles = []
    self.heart_points = []
    self.generate_heart_base_points()

    # Create glowing ambient particles
    self.init_particles(80)

    # Start animation loop
    self.animate()

  def on_resize(self, event):
    self.width = event.width
    self.height = event.height

  def generate_heart_base_points(self):
    # Fixed syntax errors: added '*' operator for coefficient multiplication and inside cosine function arguments
    self.heart_points = []
    t = 0
    while t < 2 * math.pi:
      x = 16 * (math.sin(t) ** 3)
      # Invert y because screen coordinates go downwards
      y = -(
          13 * math.cos(t)
          - 5 * math.cos(2 * t)
          - 2 * math.cos(3 * t)
          - math.cos(4 * t)
      )
      self.heart_points.append((x, y))
      t += 0.05

  def init_particles(self, num):
    for _ in range(num):
      self.particles.append({
          'x': random.uniform(0, 800),
          'y': random.uniform(0, 700),
          'vx': random.uniform(-1, 1),
          'vy': random.uniform(-1, 1),
          'size': random.uniform(1, 3.5),
          'color': random.choice(
              ['#ff3366', '#ff66cc', '#ff3399', '#cc33ff', '#ff99ff']
          ),
          'life': random.uniform(0.5, 1.0),
          'decay': random.uniform(0.005, 0.015),
      })

  def draw_glowing_text(self):
    cx, cy = self.width // 2, self.height // 2
    # Draw soft shadow glow
    self.canvas.create_text(
        cx,
        cy + 220,
        text='QUANTUM LUMINOSITY',
        fill='#300a24',
        font=('Courier', 16, 'bold'),
    )
    self.canvas.create_text(
        cx,
        cy + 240,
        text='deterministic chaos & love',
        fill='#ff007f',
        font=('Courier', 11, 'italic'),
    )

  def animate(self):
    self.canvas.delete('all')
    self.frame += 1

    # Center coordinates
    cx = self.width // 2
    cy = self.height // 2 - 30

    # Pulsating scale factor based on sine wave to simulate a realistic heartbeat rhythm
    pulse = math.sin(self.frame * 0.08)
    if pulse > 0:
      scale = 13 + (pulse**2) * 2.8
    else:
      scale = 13 + (pulse**2) * 1.2

    # Draw ambient flowing star particles
    for p in self.particles:
      # Move particle
      p['x'] += p['vx']
      p['y'] += p['vy']

      # Attract particles slightly to center (gravity pull)
      dx = cx - p['x']
      dy = cy - p['y']
      dist = math.sqrt(dx * dx + dy * dy)
      if dist > 50:
        p['vx'] += (dx / dist) * 0.015
        p['vy'] += (dy / dist) * 0.015

      # Fade/decay life
      p['life'] -= p['decay']
      if (
          p['life'] <= 0
          or p['x'] < 0
          or p['x'] > self.width
          or p['y'] < 0
          or p['y'] > self.height
      ):
        p['x'] = cx + random.uniform(-30, 30)
        p['y'] = cy + random.uniform(-30, 30)
        p['vx'] = random.uniform(-2, 2)
        p['vy'] = random.uniform(-2, 2)
        p['life'] = random.uniform(0.8, 1.0)

      # Draw particle
      self.canvas.create_oval(
          p['x'] - p['size'],
          p['y'] - p['size'],
          p['x'] + p['size'],
          p['y'] + p['size'],
          fill=p['color'],
          outline='',
      )

    # Build projected dynamic heart vertices
    projected_points = []
    for x, y in self.heart_points:
      px = cx + x * scale
      py = cy + y * scale
      projected_points.append((px, py))

    # Outer neon glow layers
    for offset in [12, 8, 4]:
      offset_points = []
      for px, py in projected_points:
        dx = px - cx
        dy = py - cy
        opx = cx + dx * (1 + offset * 0.006)
        opy = cy + dy * (1 + offset * 0.006)
        offset_points.append((opx, opy))

      flat_pts = [coord for pt in offset_points for coord in pt]
      glow_color = f'#{int(255 - offset * 15):02x}1a{int(50 + offset * 10):02x}'
      self.canvas.create_polygon(
          flat_pts, outline=glow_color, fill='', width=offset
      )

    # Main crisp pink heart vector ribbon
    flat_main = [coord for pt in projected_points for coord in pt]
    self.canvas.create_polygon(
        flat_main, outline='#ff0066', fill='#18010f', width=3
    )

    # Floating particle sparks radiating from the heart contour
    if self.frame % 3 == 0 and projected_points:
      rand_pt = random.choice(projected_points)
      self.particles.append({
          'x': rand_pt[0],
          'y': rand_pt[1],
          'vx': (rand_pt[0] - cx) * 0.05 + random.uniform(-0.5, 0.5),
          'vy': (rand_pt[1] - cy) * 0.05 + random.uniform(-0.5, 0.5),
          'size': random.uniform(1.5, 3),
          'color': '#ff007f',
          'life': 1.0,
          'decay': 0.02,
      })

    # Draw text
    self.draw_glowing_text()

    # Repeat animation tick
    self.root.after(16, self.animate)

  def run(self):
    self.root.mainloop()


if __name__ == '__main__':
  app = HeartApp()
  app.run()