import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # Gravitational acceleration (m/s^2)
rho_w = 1000  # Water density (kg/m^3)
rho_s = 2650  # Granitic particle density (kg/m^3)
KE_c = 500  # Critical KE for detachment (J/m^2)
K_d = 0.002  # Detachability coefficient (kg/J)
phi = np.radians(37)  # Angle of repose (radians)

# Input parameters
rain_angle = np.radians(30)  # Rainfall angle relative to vertical
slope_angle = np.radians(20)  # Slope angle (radians)
flow_depth = 0.01  # Flow depth (m)
particle_diameter = 0.002  # Particle diameter (m)
rain_intensity = 50  # Rainfall intensity (mm/h converted to m/s)

# Calculations
rain_velocity = np.sqrt(2 * g * flow_depth)  # Approximation for raindrop impact velocity
rain_mass = 0.0001  # Mass of a raindrop (kg)
KE = 0.5 * rain_mass * rain_velocity**2
KE_effective = KE * np.sin(rain_angle - slope_angle)

# Detachment rate
if KE_effective > KE_c:
    D = K_d * (KE_effective - KE_c) * (1 - np.cos(slope_angle))
else:
    D = 0

# Shear stress
tau = rho_w * g * flow_depth * np.sin(slope_angle)

# Transport velocity
v_s = tau / (rho_s * g * particle_diameter * np.tan(phi))

# Displacement over time
time = 3600  # 1 hour in seconds
displacement = v_s * time

# Output results
print(f"Detachment Rate (D): {D:.4f} kg/m^2/s")
print(f"Shear Stress (tau): {tau:.4f} N/m^2")
print(f"Transport Velocity (v_s): {v_s:.4f} m/s")
print(f"Displacement after {time} seconds: {displacement:.2f} m")

# Plot displacement over time
time_steps = np.linspace(0, time, 100)
displacement_steps = v_s * time_steps
plt.plot(time_steps, displacement_steps)
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.title("Displacement of Granitic Particles Over Time")
plt.grid(True)
plt.show()
